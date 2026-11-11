import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import patch_notes as notes


class PatchNotesTests(unittest.TestCase):
    def setUp(self): self.entries = notes.load()

    def test_archive_coverage_and_sources(self):
        import re
        snapshot = (notes.ROOT/'patch_notes/README-at-archive.md').read_text(encoding='utf-8')
        titles = re.findall(r'^#{2,3} (.+)$', snapshot, re.M)
        self.assertTrue(set(titles) <= {r['title'] for r in self.entries})
        self.assertGreaterEqual(len(self.entries), 240)
        self.assertTrue(any('first playable' in r['title'] for r in self.entries))
        for item in self.entries:
            if item['kind'] == 'Development report': continue
            for source in item['sources']:
                self.assertTrue((notes.ROOT/source.split(' — ')[0]).exists(), source)

    def test_bad_schema_duplicates_and_dates_rejected(self):
        original = dict(schema_version=1, releases=[self.entries[0]])
        for field,value in [('id',''),('date','2026-19-99'),('sources',[]),('kind','Unreleased')]:
            data = copy.deepcopy(original); data['releases'][0][field] = value
            with self.assertRaises(ValueError): notes.validate(data)
        with self.assertRaises(ValueError): notes.validate(dict(schema_version=2))
        with self.assertRaises(ValueError): notes.validate(dict(schema_version=1,releases=['bad']))
        with self.assertRaises(ValueError): notes.validate(dict(schema_version=1,releases=[self.entries[0]]*2))

    def test_search_filters_and_date_order(self):
        found = notes.select(self.entries, query='CANONICAL compatibility')
        self.assertIn('history-sexuality', [r['id'] for r in found])
        self.assertFalse(notes.select(self.entries, query='nonexistent-qqqqqq'))
        self.assertFalse(any(r['kind']=='Development report' for r in notes.select(self.entries)))
        self.assertTrue(notes.select(self.entries,kind='Development report',reports=True))
        self.assertTrue(all(r['category']=='Saves' for r in notes.select(self.entries,category='Saves')))
        dated = notes.select(self.entries, order='Dated first')
        first_unknown = next(i for i,r in enumerate(dated) if r['date'] is None)
        self.assertTrue(all(r['date'] is None for r in dated[first_unknown:]))

    def test_preferences_roundtrip_and_revision_unread(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'prefs.json'; prefs=notes.preferences(path)
            # Default reader filters exclude staged Development reports.
            item=notes.select(self.entries)[0]
            prefs['read'][item['id']]=notes.revision(item); prefs['bookmarks']=[item['id']]
            notes.save_preferences(prefs,path)
            self.assertEqual(notes.preferences(path),prefs)
            self.assertFalse(notes.unread(item,prefs))
            modified=dict(item,body=item['body']+'\nCorrection.')
            self.assertTrue(notes.unread(modified,prefs))
            self.assertEqual(notes.select(self.entries,status='Bookmarked',prefs=prefs),[item])
            self.assertNotIn(item, notes.select(self.entries,status='Unread',prefs=prefs))
            for damaged in ('{broken','[]','{"read": 123}','{"bookmarks": "bad"}'):
                path.write_text(damaged)
                self.assertEqual(notes.preferences(path),{'read':{},'bookmarks':[]})

    def test_atomic_failure_preserves_prior_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'prefs.json'; path.write_text('previous')
            with patch.object(notes.os,'replace',side_effect=OSError('read only')):
                with self.assertRaises(OSError): notes.atomic_write(path,'replacement')
            self.assertEqual(path.read_text(),'previous')
            self.assertEqual(list(Path(folder).iterdir()),[path])

    def test_export_selected_only_and_provenance(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'out.md'
            notes.export([self.entries[0]],path)
            text=path.read_text(encoding='utf-8')
            self.assertIn(notes.NOTICE,text)
            self.assertIn(self.entries[0]['title'],text)
            self.assertNotIn(self.entries[1]['title'],text)
            self.assertIn('Save compatibility',text)


if __name__ == '__main__': unittest.main()
