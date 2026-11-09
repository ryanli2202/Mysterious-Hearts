import copy
import json
from pathlib import Path
import tempfile
import unittest
from PIL import Image
import game_core as core
import playable_cast
import world_loop
import town
import phone_personalization as personal
import bubblegram_roles as roles
import job_apps as jobs
import crime_diplomacy as diplomacy
import crime_operations


class ProtagonistExpansionTests(unittest.TestCase):
    def test_named_vehicle_selection_and_saved_journeys(self):
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as folder:
            for who in core.PLAYERS:
                with self.subTest(player=who):
                    s = core.fresh(who)
                    garage = world_loop.player_garage(s)
                    self.assertTrue(garage)
                    self.assertNotIn('Town car', garage)
                    for model, (seats, _) in garage.items():
                        town.select_car(s, model)
                        self.assertEqual(world_loop.trip_vehicle(s, who, 0), model)
                        self.assertEqual(world_loop.trip_vehicle(s, who, seats), world_loop.GROUP_VAN)
                    chosen = next(iter(garage))
                    town.select_car(s, chosen)
                    town.travel(s, 'park')
                    trip = [t for t in s['world']['journeys'] if t['driver'] == who][-1]
                    self.assertEqual(trip['vehicle'], chosen)
                    path = Path(folder) / (who + '.json')
                    core.save(s, path); loaded = core.load(path)
                    self.assertEqual(world_loop.selected_car(loaded, who), chosen)
                    trip = [t for t in loaded['world']['journeys'] if t['driver'] == who][-1]
                    self.assertEqual(trip['vehicle'], chosen)

    def test_all_wallpapers_and_charles_contact(self):
        paths = []
        for who in core.PLAYERS:
            s = core.fresh(who)
            path = personal.wallpaper_path(s)
            self.assertTrue(path.is_file(), who)
            paths.append(path)
            with Image.open(path) as image:
                self.assertGreater(image.height, image.width)
                self.assertGreaterEqual(image.height, 1000)
                pixels = list(image.convert('RGB').resize((32, 32)).getdata())
                self.assertLess(sum(sum(p)/3 for p in pixels)/len(pixels), 85, who)
            personal.ensure(s)['wallpaper'] = 'photo:missing'
            self.assertEqual(personal.wallpaper_path(s).name, 'missing-wallpaper')
        self.assertEqual(len(set(paths)), len(core.PLAYERS))
        with Image.open(core.ROOT / 'assets/profiles/charles-contact-v3.png') as image:
            self.assertEqual(image.width, image.height)

    def test_established_desks_migrate_once_without_resetting_losses(self):
        for who, spec in roles.ROLES.items():
            with self.subTest(player=who):
                s = core.fresh(who)
                d = jobs.ensure(s)
                self.assertEqual(d['story_membership']['authority'], spec['authority'])
                self.assertIsNone(d['membership'])
                self.assertEqual(diplomacy.mandate(s)[0], spec['key'])
                b = diplomacy.ensure(s)
                b['treasury'] -= 1234; b['influence'] = 1
                b['relations']['syndicate'] = 20
                d['reputation'] = 50; d['heat'] = 12
                saved = copy.deepcopy((d, b))
                jobs.ensure(s); diplomacy.ensure(s)
                self.assertEqual((d, b), saved)
                loaded = json.loads(json.dumps(s))
                self.assertEqual(diplomacy.ensure(loaded)['treasury'], spec['budget'] - 1234)
                self.assertEqual(jobs.ensure(loaded)['reputation'], 50)
                with self.assertRaises(ValueError): jobs.sponsor(s, 'Clubs')
                with self.assertRaises(ValueError): jobs.accept(s, 'syndicate')
                if who in core.hidden.four_aces.IDS:
                    self.assertFalse(any(crime_operations.authority(who, site) for site in ('site_04', 'site_05', 'site_06', 'site_08')))
        self.assertTrue(crime_operations.authority('valentina', 'site_04'))
        self.assertFalse(crime_operations.authority('valentina', 'site_05'))

    def test_role_contracts_and_mandates(self):
        for who, spec in roles.ROLES.items():
            with self.subTest(player=who):
                s = core.fresh(who)
                d = jobs.ensure(s)
                jobs.accept(s, 'leadership')
                self.assertEqual(d['pending']['venue'], spec['venue'])
                self.assertEqual(d['pending']['brief'], spec['brief'])
                with self.assertRaises(ValueError): jobs.resolve(s, 0)
                for _ in range(3):
                    if s['world']['location'] == spec['venue']: break
                    jobs.travel(s, spec['venue'])
                balance = s['world']['money']
                jobs.resolve(s, 0)
                self.assertIsNone(d['pending'])
                self.assertGreater(s['world']['money'], balance)
                self.assertIn(spec['title'], d['history'][-1]['text'])
                with self.assertRaises(ValueError): jobs.accept(s, 'leadership')
                b = diplomacy.ensure(s)
                before = core.town.loop.GARAGES.copy()
                diplomacy.request(s, 'waterfront')
                self.assertTrue(b['meetings'])
                self.assertEqual(core.town.loop.GARAGES, before)

    def test_legacy_sponsorship_is_archived_not_lost(self):
        s = core.fresh('camila'); d = jobs.ensure(s)
        d.pop('playable_syndicate_role_v1')
        old = dict(faction='Syndicate', branch='Diamonds', rank=2, assignments=8, strikes=1)
        d['membership'] = dict(old)
        d['pending'] = dict(kind='faction', key='Diamonds', venue='site_06_reception', started=0, deadline=1440)
        jobs.ensure(s)
        self.assertEqual(d['prior_sponsorships'][-1], old)
        self.assertEqual(d['prior_assignments'][-1]['kind'], 'faction')
        self.assertIsNone(d['pending'])
        self.assertIsNone(d['membership'])


if __name__ == '__main__': unittest.main()
