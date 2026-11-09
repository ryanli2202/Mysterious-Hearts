import copy
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import game_core as core
import hidden_cast as hidden
import four_aces
import phone_apps
import phone_numbers
import crime_sites
import crime_operations as ops
import social_world
import character_appearance
import camera


class SyndicateCastTests(unittest.TestCase):
    def test_player_ivan_changes_at_headquarters_and_restores_saved_outfit(self):
        s = core.fresh('ivan')
        s['world']['player_outfit'] = 'Gym tank and shorts'
        core.town.travel(s, hidden.HQ)
        self.assertTrue(four_aces.uniform_at('ivan', s['world']['cast']['ivan']['location']))
        context = camera.scene(s)
        self.assertEqual(camera.default_outfit(s, 'ivan', context), 'Syndicate uniform')
        shot = camera.request(s, {'mode': 'Selfie', 'people': {'ivan': {'outfit': 'Gym tank and shorts'}}})
        self.assertEqual(shot['snapshot']['subjects'][0]['outfit'], 'Syndicate uniform')
        self.assertTrue(any(str(path).endswith('ivan-syndicate.png') for path in shot['references']))
        visible = social_world.appearance_reference(s, 'ivan', ['sylvanis'], '', texting=False)['People']['ivan']
        self.assertIn('Black ceremonial coat', visible['Current visible uniform'])
        self.assertNotIn('Selected outfit in this in-person scene', visible)
        self.assertEqual(s['world']['player_outfit'], 'Gym tank and shorts')
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as directory:
            path = Path(directory) / 'ivan.json'
            core.save(s, path)
            loaded = core.load(path)
        self.assertTrue(four_aces.uniform_at('ivan', loaded['world']['location']))
        core.town.travel(loaded, 'studio')
        self.assertFalse(four_aces.uniform_at('ivan', loaded['world']['location']))
        self.assertEqual(camera.default_outfit(loaded, 'ivan', camera.scene(loaded)), 'Gym tank and shorts')
        self.assertEqual(loaded['world']['player_outfit'], 'Gym tank and shorts')

    def test_exact_initial_roster(self):
        s = core.fresh('ivan')
        self.assertEqual(set(phone_apps.contacts(s)), set(hidden.IVAN_STARTING_CONTACTS))
        self.assertEqual(set(phone_numbers.ensure(s)['contacts']), {'ivan', *hidden.IVAN_STARTING_CONTACTS})
        self.assertTrue(hidden.contact(s, 'sylvanis'))
        for who in ('emily', 'neo', 'lena', 'yuriko'):
            self.assertFalse(hidden.known(s, who))
            self.assertEqual(core.town.character_stats(s, who)['status'], 'strangers')

    def test_legacy_seed_cleanup_preserves_earned_connections(self):
        s = core.fresh('ivan')
        s.pop('ivan_contact_seed_v2')
        for who in ('emily', 'neo', 'lena', 'yuriko', 'alyssa'):
            s['discoveries'][who] = dict(met=True, contact=True, home=False)
        phone_numbers.ensure(s)
        # An actual meeting, an explicit number exchange, and a conversation survive.
        s['routes']['neo']['history'].append(dict(role='status', content='Phone texts → In-person conversation · Neo'))
        s['phone_numbers']['contacts']['lena'] = dict(number=phone_numbers.NUMBERS['lena'], source='Meet-Cute', minute=500)
        s['routes']['yuriko']['history'].append(dict(role='user', content='Hello Yuriko'))
        s['routes']['alyssa']['history'].append(dict(role='user', content=core.INCOMING_TEXT))
        s.pop('ivan_contact_seed_v2', None)
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as directory:
            path = Path(directory) / 'legacy.json'
            core.save(s, path)
            loaded = core.load(path)
        for who in ('neo', 'lena', 'yuriko'):
            self.assertTrue(hidden.contact(loaded, who))
        for who in ('emily', 'alyssa'):
            self.assertFalse(hidden.contact(loaded, who))
            self.assertIsNone(phone_numbers.saved_number(loaded, who))
        hidden.mark_met(loaded, 'emily')
        self.assertTrue(hidden.contact(loaded, 'emily'))
        before = copy.deepcopy(loaded['discoveries'])
        hidden.ensure(loaded)
        self.assertEqual(before, loaded['discoveries'])

    def test_business_focus_and_mixed_group_secrecy(self):
        for who in (*four_aces.IDS, 'sylvanis'):
            context = four_aces.private_context(who, ['ivan'])
            self.assertIn('Primarily discuss Syndicate business', context['Working relationship with Ivan'])
            self.assertNotIn('Working relationship with Ivan', four_aces.private_context(who, ['rei']))
            mixed = four_aces.private_context(who, ['ivan', 'rei'])
            self.assertNotIn('Shared Ace working history', mixed)
            self.assertIn('outsiders', mixed['Working relationship with Ivan'])

    def test_all_affiliate_interiors_without_command_or_guest_transfer(self):
        s = core.fresh('ivan')
        for who in four_aces.IDS:
            for site, spec in crime_sites.SITES.items():
                self.assertEqual(ops.permitted(s, who, site), spec['faction'] == 'Syndicate')
                self.assertFalse(ops.authority(who, site))
                s['world']['cast'][who].update(location=site+'_reception', journey=None)
                self.assertEqual(ops.can_enter(s, who, site+'_briefing'), spec['faction'] == 'Syndicate')
            s['world']['cast']['rei'].update(location='site_07_reception', journey=None)
            s['world']['cast'][who].update(location='site_07_reception', journey=None)
            with self.assertRaises(ValueError):
                ops.check_trip(s, who, 'site_07_briefing', ['rei'])

    def test_uniform_visibility_and_alpha(self):
        s = core.fresh('ivan')
        s['world']['location'] = hidden.HQ
        for who in four_aces.UNIFORM_IDS:
            s['world']['cast'][who]['location'] = hidden.HQ
            visible = social_world.appearance_reference(s, who, ['ivan'], '', texting=False)['People'][who]
            self.assertIn('Current visible uniform', visible)
            self.assertNotIn('Recognisable features', visible)
            remote = social_world.appearance_reference(s, who, ['ivan'], '', texting=True)['People'][who]
            self.assertNotIn('Current visible uniform', remote)
            self.assertNotIn('Headquarters uniform (private operational styling)', character_appearance.reference(who))
            self.assertFalse(four_aces.uniform_at(who, 'studio'))
            with Image.open(core.ROOT / 'assets/portraits' / (who+'-syndicate.png')) as im:
                self.assertEqual(im.mode, 'RGBA')
                self.assertEqual(im.getchannel('A').getextrema(), (0, 255))


if __name__ == '__main__':
    unittest.main()
