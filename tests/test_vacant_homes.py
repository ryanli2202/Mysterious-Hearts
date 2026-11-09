import tempfile
import unittest
from pathlib import Path

import game_core as core
import phone_map
import town
import vacant_homes


class VacantHomeTests(unittest.TestCase):
    def test_visit_save_and_leave_each_unassigned_home(self):
        state = core.fresh('rei')
        original_cast = set(state['world']['cast'])
        for key in vacant_homes.HOMES:
            with self.subTest(home=key):
                self.assertIn(key, phone_map.places(state, 'vacant', 'Homes'))
                self.assertNotIn(key, town.HOMES.values())
                town.travel(state, key)
                self.assertEqual(state['world']['location'], key)
                self.assertEqual(state['world']['npcs'], [])
                self.assertEqual(set(state['world']['cast']), original_cast)
                self.assertIn(vacant_homes.STATUS, town.context(state))
                with self.assertRaises(ValueError):
                    town.rest(state)
                with tempfile.TemporaryDirectory() as folder:
                    path = Path(folder) / 'story.json'
                    core.save(state, path)
                    state = core.load(path)
                self.assertEqual(state['world']['location'], key)
                town.travel(state, 'home')
                self.assertEqual(state['world']['location'], town.HOMES['rei'])
