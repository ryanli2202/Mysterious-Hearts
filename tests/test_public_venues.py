import json
import unittest
from unittest.mock import patch

import game_core as core
import leisure
import living_world
import phone_apps
import phone_map
import public_venues
import scheduled_events
import story_calendar
import town
import world_loop


class PublicVenueTests(unittest.TestCase):
    def test_travel_party_map_and_restored_state(self):
        s = core.fresh('rei')
        town.ensure(s)
        s['world']['party'] = ['emily']
        s['world']['cast']['emily'].update(location=s['world']['location'], journey=None)
        for venue in public_venues.VENUES:
            with self.subTest(venue=venue):
                town.travel(s, venue)
                self.assertEqual(s['world']['location'], venue)
                self.assertEqual(s['world']['cast']['emily']['location'], venue)
                self.assertIn(venue, phone_map.places(s))
                self.assertIn(venue, phone_apps.location_people(s))
                self.assertEqual(s['world']['journeys'][-1]['destination'], venue)
                s = json.loads(json.dumps(s))
                town.ensure(s)
                self.assertEqual(s['world']['location'], venue)

    def test_each_venue_has_activity_cost_memory_and_camera_context(self):
        for venue, data in public_venues.VENUES.items():
            with self.subTest(venue=venue), patch('weather.shelter', return_value=False):
                s = core.fresh('rei')
                s['world']['minute'] = 21*60
                town.travel(s, venue)
                before = s['world']['money']
                living_world.visit(s)
                self.assertEqual(s['world']['money'], before-data[4])
                self.assertEqual(s['world']['camera_activity']['location'], venue)
                self.assertIn(venue, s['living_world']['visits'])
                with self.assertRaises(ValueError):
                    living_world.visit(s)

    def test_every_new_venue_is_selected_and_nightlife_stays_in_evening(self):
        chosen = set()
        with patch('weather.shelter', return_value=False):
            for who in leisure.PREFERENCES:
                for day in range(28):
                    for hour in (11, 14, 17, 20, 21):
                        venue = leisure.choose(who, day*1440+hour*60)
                        chosen.add(venue)
                        self.assertTrue(public_venues.suitable(venue, hour*60))
        self.assertTrue(public_venues.VENUES.keys() <= chosen)

    def test_outdoor_activities_respect_weather(self):
        with patch('weather.shelter', return_value=True):
            for venue in public_venues.OUTDOORS:
                s = core.fresh('rei')
                town.travel(s, venue)
                with self.assertRaises(ValueError):
                    living_world.visit(s)
            for who in leisure.PREFERENCES:
                self.assertNotIn(leisure.choose(who, 14*60), public_venues.OUTDOORS)

    def test_calendar_and_simulation_arrive_at_each_new_venue(self):
        for venue in public_venues.VENUES:
            with self.subTest(venue=venue):
                s = core.fresh('rei')
                s['world']['minute'] = 20*60-1
                event = scheduled_events.create(s, 'Meet up', story_calendar.START.isoformat(),
                                                '20:00', venue, ['emily'])
                world_loop.advance(s, 1)
                self.assertEqual(s['world']['cast']['emily']['location'], venue)
                self.assertEqual(event['venue'], venue)

    def test_evening_schedule_returns_home(self):
        # Story day zero is Saturday.
        self.assertEqual(world_loop.appointment('sophie', 20*60)[0], 20)
        self.assertNotEqual(world_loop.appointment('sophie', 20*60)[1], 'sophie_home')
        self.assertEqual(world_loop.appointment('sophie', 22*60)[1], 'sophie_home')


if __name__ == '__main__':
    unittest.main()
