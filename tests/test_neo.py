import tempfile
import unittest
from pathlib import Path

import game_core as core
import hidden_cast
import town
import world_loop
import grove
import contact_profiles
import conversation_lore
import phone_map
import meet_cute


class NeoTests(unittest.TestCase):
    def test_discovery_home_and_platonic_boundary(self):
        s = core.fresh('rei')
        self.assertFalse(hidden_cast.known(s, 'neo'))
        self.assertNotIn('neo_home', phone_map.places(s))
        self.assertFalse(town.romanceable(s, 'neo'))
        self.assertNotIn('neo', meet_cute.HOOKS)
        hidden_cast.mark_met(s, 'neo')
        self.assertTrue(hidden_cast.contact(s, 'neo'))
        with self.assertRaises(ValueError):
            hidden_cast.discover_home(s, 'neo')
        s['friendships']['neo']['closeness'] = 6
        hidden_cast.discover_home(s, 'neo')
        self.assertIn('neo_home', phone_map.places(s))
        for event in ('returned_flirt', 'welcomed_flirt'):
            town.social_event(s, 'neo', event)
        self.assertEqual(s['friendships']['neo']['attraction'], 0)
        self.assertIsNone(core.flirt_target(s, ['neo']))
        self.assertIn('alyssa', s['world']['cast'])
        self.assertFalse(hidden_cast.known(s, 'alyssa'))

    def test_old_save_migrates_once_and_preserves_bonds(self):
        s = core.fresh('rei')
        s['routes'].pop('neo')
        s['friendships'].pop('neo')
        s['world']['cast'].pop('neo')
        s['discoveries'].pop('neo')
        s['contact_profiles']['people'].pop('neo')
        s['bond_details'].pop('neo:tyler')
        s['bond_details']['neo:daniel']['trust'] = 27
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'save.json'
            core.save(s, path)
            loaded = core.load(path)
        self.assertIn('neo', loaded['routes'])
        self.assertEqual(loaded['bond_details']['neo:tyler']['trust'], 95)
        self.assertEqual(loaded['bond_details']['neo:daniel']['trust'], 27)
        self.assertFalse(hidden_cast.known(loaded, 'neo'))
        self.assertEqual(contact_profiles.public(loaded, 'neo', 'rei')['Status'], 'In a relationship with Alyssa')

    def test_reference_schedule_and_assets(self):
        for level in range(4):
            reference = conversation_lore.speaker_reference('neo', ['rei'], level, 'your family')
            self.assertEqual('Confidence' in reference, level == 3)
        for who in ('tyler', 'daniel'):
            self.assertIn('best friends', conversation_lore.speaker_reference(who, ['neo'], 0, 'school')['Everyday shared memories with people present']['neo'])
        self.assertEqual(grove.HANDLES['neo'], 'neo.onstandby')
        for _, place, _ in world_loop.SCHEDULES['neo']:
            self.assertIn(place, town.LOCATIONS)
        for folder, filename in [('portraits', 'neo-selection.png'), ('profiles', 'neo.png')]:
            self.assertTrue((core.ROOT / 'assets' / folder / filename).is_file())


if __name__ == '__main__':
    unittest.main()
