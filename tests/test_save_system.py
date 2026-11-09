import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import game_core as core
import save_system as saves


class SaveSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.active = self.root / 'saves' / 'story.json'
        self.state = core.fresh('rei')

    def write(self, state=None):
        saves.write(state or self.state, self.active, self.active)

    def test_stories_have_separate_autosaves_and_checkpoints(self):
        self.write()
        first = self.state['story_id']
        self.state['turn'] = 1; self.write()
        other = core.fresh('garrett'); self.write(other)
        base = self.active.parent / 'stories'
        self.assertEqual(json.loads((base/first/'autosave.json').read_text(encoding='utf-8'))['player'], 'rei')
        self.assertFalse((base/other['story_id']/'recent').exists())
        self.assertEqual(len(list((base/first/'recent').glob('*.json'))), 1)
        for n in range(2, 8): self.state['turn'] = n; self.write()
        self.assertEqual(len(list((base/first/'recent').glob('*.json'))), 1)
        self.assertEqual(len(list((base/first/'daily').glob('*.json'))), 1)

    def test_selected_deletion_preserves_other_story(self):
        self.write(); path = self.active.parent/'stories'/self.state['story_id']/'autosave.json'
        other = core.fresh('ivan'); self.write(other)
        saves.delete(self.active.parent, path)
        self.assertFalse(path.exists())
        self.assertEqual(json.loads(self.active.read_text(encoding='utf-8'))['player'], 'ivan')
        saves.delete(self.active.parent)
        self.assertEqual(saves.entries(self.active.parent), [])

    def test_failed_replace_keeps_original_and_cleans_temporary(self):
        self.write(); original = self.active.read_bytes()
        with patch('save_system.os.replace', side_effect=OSError('disk error')):
            with self.assertRaises(OSError): saves.atomic(self.active, b'new')
        self.assertEqual(self.active.read_bytes(), original)
        self.assertEqual(list(self.active.parent.glob('*.tmp')), [])

    def test_checkpoint_retention_keeps_only_newest_entries(self):
        self.write()
        folder = self.active.parent / 'stories' / self.state['story_id']
        recent = folder / 'recent'; daily = folder / 'daily'
        recent.mkdir(); daily.mkdir()
        for n in range(20):
            (recent / f'{n:02}.json').write_text('{}')
            (daily / f'2000-01-{n+1:02}.json').write_text('{}')
        saves.checkpoints(folder / 'autosave.json')
        self.assertEqual(len(list(recent.glob('*.json'))), 12)
        self.assertEqual(len(list(daily.glob('*.json'))), 14)
        self.assertFalse((recent / '00.json').exists())

    def test_deleting_damaged_checkpoint_removes_whole_story(self):
        self.write(); self.state['turn'] = 1; self.write()
        folder = self.active.parent / 'stories' / self.state['story_id']
        checkpoint = next((folder / 'recent').glob('*.json'))
        checkpoint.write_text('{damaged')
        saves.delete(self.active.parent, checkpoint)
        self.assertEqual(saves.entries(self.active.parent), [])

    def test_concurrent_writers_leave_complete_json(self):
        from concurrent.futures import ThreadPoolExecutor
        import copy
        self.write()
        states = [dict(copy.deepcopy(self.state), turn=n) for n in range(12)]
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(self.write, states))
        result = json.loads(self.active.read_text(encoding='utf-8'))
        self.assertIn(result['turn'], range(12))
        self.assertEqual(self.active.read_bytes(),
                         (self.active.parent/'stories'/self.state['story_id']/'autosave.json').read_bytes())
        self.assertFalse(list(self.active.parent.rglob('*.tmp')))

    def test_bundle_roundtrip_with_photo_and_album(self):
        self.write()
        asset = self.root/'assets/generated/photo.png'; asset.parent.mkdir(parents=True); asset.write_bytes(b'photo')
        self.state['test_photo'] = 'assets/generated/photo.png'
        album_id = 'a'*32; self.state['camera'] = {'album': album_id}
        manifest = self.root/'assets/generated/camera-albums'/album_id/'photos.json'
        manifest.parent.mkdir(parents=True); manifest.write_text('[]')
        bundle = self.root/'export.zip'; saves.export_story(self.state, bundle, self.root)
        destination = self.root/'destination'
        imported = saves.import_story(bundle, destination, destination/'saves')
        state = core.load(imported)
        self.assertEqual(state['player'], 'rei')
        self.assertNotEqual(state['story_id'], self.state['story_id'])
        self.assertEqual((destination/'assets/generated/photo.png').read_bytes(), b'photo')
        self.assertTrue((destination/manifest.relative_to(self.root)).exists())

    def test_import_rejects_traversal_before_writing(self):
        bundle = self.root/'bad.zip'
        with zipfile.ZipFile(bundle, 'w') as z:
            z.writestr('story.json', json.dumps(self.state))
            z.writestr('assets/generated/../../escape.txt', 'bad')
        with self.assertRaises(ValueError): saves.import_story(bundle, self.root, self.active.parent)
        self.assertFalse((self.root/'assets/escape.txt').exists())

    def test_corrupt_save_remains_visible(self):
        self.write(); self.active.write_text('{broken')
        self.assertIn(self.active, saves.entries(self.active.parent))
        self.assertTrue(saves.recovery(self.active.parent))

if __name__ == '__main__': unittest.main()
