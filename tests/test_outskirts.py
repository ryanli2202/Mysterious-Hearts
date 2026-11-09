import copy
import unittest
from unittest.mock import patch

import game_core
import outskirts
import phone_map
import phone_numbers
import town
import town_residents


class OutskirtsTests(unittest.TestCase):
    def test_all_new_places_extend_old_playable_bounds_and_fit_compact_map(self):
        state = game_core.fresh('rei')
        cx, cy, zoom = phone_map.fit_camera(state, 480, 180)
        for key, data in outskirts.VENUES.items():
            x, y = data[1]
            self.assertFalse(0 <= x <= 1400 and 0 <= y <= 1100)
            self.assertIn(key, phone_map.places(state, data[0]))
        for key in phone_map.places(state):
            x, y = phone_map.POINTS[key]
            self.assertLessEqual(abs(x-cx)*zoom, 240)
            self.assertLessEqual(abs(y-cy)*zoom, 90)

    @patch('town_residents.weather.shelter', return_value=False)
    def test_new_residents_can_be_met_and_saved_without_losing_existing_history(self, _):
        state = game_core.fresh('rei')
        state['npc_chats'] = {'Theo': {'history': [{'speaker': 'Theo', 'text': 'Hello'}]}}
        old_chat = copy.deepcopy(state['npc_chats']['Theo'])
        self.assertEqual(phone_numbers.NUMBERS['Samir Dutta'], '12025550143')
        for name, person in outskirts.RESIDENTS.items():
            state['world']['minute'] = 2*1440+9*60
            town.travel(state, person['places'][0])
            self.assertIn(name, state['world']['npcs'])
            self.assertEqual(town.npc_details(state, name)[1], person['role'])
            phone_numbers.add(state, phone_numbers.NUMBERS[name])
            self.assertIn('npc:'+name, state['groups'])
            self.assertIsNone(town_residents.routine(name, 23*60))
        self.assertEqual(state['npc_chats']['Theo'], old_chat)

    @patch('town_residents.weather.shelter', return_value=True)
    def test_outdoor_residents_shelter_and_indoor_hosts_remain(self, _):
        for name, person in outskirts.RESIDENTS.items():
            for day in (0, 2):
                for hour in (9, 14, 19):
                    self.assertNotIn(town_residents.routine(name, day*1440+hour*60), outskirts.OUTDOORS)
        self.assertEqual(town_residents.routine('Euan Marsh', 9*60), 'hill_tea_room')


if __name__ == '__main__':
    unittest.main()
