import tempfile
import unittest
from pathlib import Path

import game_core as core
import hidden_cast as hidden
import town
import world_loop
import conversation_lore as lore
import contact_profiles
import grove
import phone_map
import meet_cute
import phone_numbers


class AlyssaTests(unittest.TestCase):
    def test_shared_home_does_not_introduce_partner(self):
        for resident, partner in [('alyssa', 'neo'), ('neo', 'alyssa')]:
            s = core.fresh('rei')
            self.assertFalse(hidden.known(s, resident))
            self.assertNotIn('neo_home', phone_map.places(s))
            self.assertEqual(world_loop.HOUSES['alyssa'], world_loop.HOUSES['neo'])
            self.assertNotIn('alyssa_home', town.LOCATIONS)
            hidden.mark_met(s, resident)
            with self.assertRaises(ValueError):
                hidden.discover_home(s, resident)
            s['friendships'][resident]['closeness'] = 6
            hidden.discover_home(s, resident)
            self.assertIn('neo_home', phone_map.places(s))
            self.assertFalse(hidden.known(s, partner))
            self.assertFalse(town.romanceable(s, resident))
            self.assertIsNone(core.flirt_target(s, [resident]))
            self.assertNotIn(resident, meet_cute.HOOKS)
        for _, place, _ in world_loop.SCHEDULES['alyssa']:
            self.assertIn(place, town.LOCATIONS)

    def test_existing_save_gains_alyssa_without_resetting_neo(self):
        s = core.fresh('rei')
        hidden.mark_met(s, 'neo')
        s['friendships']['neo']['closeness'] = 42
        hidden.discover_home(s, 'neo')
        for rows in (s['routes'], s['friendships'], s['world']['cast'],
                     s['discoveries'], s['contact_profiles']['people']):
            rows.pop('alyssa')
        s['bond_details'].pop('alyssa:neo')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'save.json'
            core.save(s, path)
            loaded = core.load(path)
            core.save(loaded, path)
            self.assertEqual(core.load(path), loaded)
        self.assertIn('alyssa', loaded['routes'])
        self.assertFalse(hidden.known(loaded, 'alyssa'))
        self.assertTrue(hidden.visible_place(loaded, 'neo_home'))
        self.assertEqual(loaded['friendships']['neo']['closeness'], 42)
        self.assertIn('Committed partners', loaded['bond_details']['alyssa:neo']['type'])

    def test_profiles_and_dialogue(self):
        s = core.fresh('rei')
        p = contact_profiles.public(s, 'alyssa', 'rei')
        self.assertEqual(p['Status'], 'In a relationship with Neo')
        self.assertIn('bookbinding', p['Hobbies'])
        self.assertEqual(grove.HANDLES['alyssa'], 'alyssa.betweenpages')
        hidden.mark_met(s, 'alyssa')
        self.assertIsNotNone(phone_numbers.saved_number(s, 'alyssa') or phone_numbers.number(s, 'alyssa'))
        s['active'] = 'alyssa'
        self.assertTrue(core.build_messages(s, 'Tell me about your bookbinding.'))
        self.assertEqual(grove.context(s, {'author': 'alyssa'})['author'], 'alyssa')
        reference = lore.speaker_reference('alyssa', ['neo'], 0, 'our home')
        self.assertIn('Blisk', reference['Public life'])
        self.assertNotIn('Confidence', reference)
        self.assertIn('neo', reference['Everyday shared memories with people present'])
