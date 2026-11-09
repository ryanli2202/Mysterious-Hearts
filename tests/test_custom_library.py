import json
from pathlib import Path
import tempfile
import unittest
import custom_library as library
import custom_protagonist as custom
import save_system
from test_custom_protagonist import PROFILE


class LibraryTests(unittest.TestCase):
    def test_save_delete_and_legacy_recovery(self):
        with tempfile.TemporaryDirectory(dir=custom.ROOT / '.test-tmp') as folder:
            root = Path(folder) / 'saves'
            active = root / 'story.json'
            state = {'player': 'custom_' + 'a'*32, 'custom_protagonist': PROFILE | {
                'portrait': 'assets/generated/example.png'}, 'routes': {}}
            save_system.write(state, active, active)
            self.assertEqual(len(library.profiles(root)), 1)
            # A different playthrough of the same profile does not add duplicates.
            state['player'] = 'custom_' + 'b'*32
            save_system.write(state, active, active)
            save_system.delete(root)
            self.assertEqual(len(library.profiles(root)), 1)
            self.assertFalse(list(root.rglob('*.json')))
            for path in (root.parent / 'custom_characters').glob('*.json'): path.unlink()
            active.write_text(json.dumps(state), encoding='utf-8')
            save_system.delete(root, active)
            self.assertEqual(library.profiles(root)[0]['name'], PROFILE['name'])

    def test_legacy_menu_migration(self):
        with tempfile.TemporaryDirectory(dir=custom.ROOT / '.test-tmp') as folder:
            root = Path(folder) / 'saves'
            root.mkdir()
            (root / 'legacy.json').write_text(json.dumps({
                'player': 'custom_' + 'a'*32, 'custom_protagonist': PROFILE | {
                    'portrait': 'assets/generated/example.png'}}), encoding='utf-8')
            self.assertEqual(len(library.profiles(root)), 1)
            self.assertTrue((root / 'legacy.json').exists())
