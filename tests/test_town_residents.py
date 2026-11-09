import copy
import unittest
from unittest.mock import patch

import game_core
import groups
import phone_numbers
import town
import town_residents as residents


class ResidentTests(unittest.TestCase):
    def test_roster_has_valid_locations_and_stable_contact_numbers(self):
        self.assertEqual(len(residents.RESIDENTS), 26)
        for name, person in residents.RESIDENTS.items():
            self.assertIn(name, phone_numbers.NUMBERS)
            for place in (*person['places'], *person['weekend']):
                self.assertIn(place, town.LOCATIONS)
        self.assertEqual(phone_numbers.NUMBERS['alyssa'], '12025550131')

    @patch('town_residents.weather.shelter', return_value=False)
    def test_routines_change_by_time_weekend_and_weather(self, _):
        # 1 January 2050 is Saturday; the third day is Monday.
        self.assertEqual(residents.routine('Priya Shah', 9*60), 'public_park')
        self.assertEqual(residents.routine('Priya Shah', 2*1440+9*60), 'library')
        self.assertEqual(residents.routine('Priya Shah', 18*60), 'chess')
        self.assertIsNone(residents.routine('Priya Shah', 23*60))
        with patch('town_residents.weather.shelter', return_value=True):
            self.assertEqual(residents.routine('Priya Shah', 9*60), 'library')

    def test_old_save_refresh_preserves_history_and_private_locations(self):
        state = game_core.fresh()
        state['world'].update(location='library', minute=2*1440+9*60, npcs=['Theo'])
        state['npc_chats'] = {'Priya Shah': {'history': [{'speaker': 'Priya Shah', 'text': 'Hello.'}]}}
        before = copy.deepcopy(state['npc_chats'])
        town.ensure(state)
        self.assertIn('Priya Shah', state['world']['npcs'])
        self.assertIn('Theo', state['world']['npcs'])
        self.assertEqual(town.npc_details(state, 'Priya Shah')[1], 'public librarian')
        town.ensure(state)
        self.assertEqual(state['world']['npcs'].count('Priya Shah'), 1)
        state['world']['location'] = town.HOMES[state['player']]
        residents.refresh(state)
        self.assertFalse(set(residents.RESIDENTS) & set(state['world']['npcs']))
        self.assertEqual(state['npc_chats'], before)

    def test_clock_moves_residents_and_closes_local_hangout(self):
        state = game_core.fresh()
        state['world'].update(location='library', minute=2*1440+17*60-1, npcs=[])
        state['world']['cast'][state['player']].update(location='library', journey=None)
        town.ensure(state)
        groups.open_local(state, 'Priya Shah')
        town.wait(state, 1)
        self.assertNotIn('Priya Shah', state['world']['npcs'])
        self.assertFalse(state['groups']['local:Priya Shah']['open'])

    def test_new_contact_can_be_saved_without_unlocking_other_residents(self):
        state = game_core.fresh()
        phone_numbers.add(state, phone_numbers.NUMBERS['Priya Shah'])
        self.assertIn('npc:Priya Shah', state['groups'])
        self.assertNotIn('Otis Bell', state['phone_numbers']['contacts'])
        self.assertIn('no-pressure reading circle', residents.profile('Priya Shah')[2])
        self.assertNotEqual(residents.context('Priya Shah', 0), residents.context('Priya Shah', 1440))

    def test_every_resident_has_a_conversation_reference(self):
        import social_world
        state = game_core.fresh()
        for name in residents.RESIDENTS:
            reference = social_world.reference_for(state, name, [state['player']], '', texting=True)
            self.assertIn(str(residents.RESIDENTS[name]['age']), reference['Public life'])
            self.assertNotIn('Confidence', reference)


if __name__ == '__main__':
    unittest.main()
