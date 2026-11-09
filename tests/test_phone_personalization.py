import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as core
import phone_personalization as p


class PhonePersonalizationTests(unittest.TestCase):
    def test_original_protagonists_have_distinct_defaults_and_three_visible_pins(self):
        pin_sets = []
        for player in core.playable_cast.ORIGINAL:
            s = core.fresh(player)
            d = p.ensure(s)
            self.assertEqual(len(d['pins']), 3)
            self.assertTrue(set(d['pins']) <= {r['id'] for r in p.records(s)})
            self.assertTrue(p.wallpaper_path(s).is_file())
            pin_sets.append(tuple(d['pins']))
        self.assertEqual(len(set(pin_sets)), len(core.playable_cast.ORIGINAL))

    def test_old_save_migration_is_idempotent_and_preserves_history(self):
        s = core.fresh('rei'); original = copy.deepcopy(s['routes'])
        d = p.ensure(s); p.unpin(s, d['pins'][0]); d['notes'] = 'My theory'
        p.rename(s, 'emily', 'Flower friend')
        restored = json.loads(json.dumps(s))
        self.assertEqual(p.ensure(restored), d)
        self.assertEqual(restored['routes'], original)
        self.assertEqual(core.contact_name(s, 'emily'), 'Emily Fields')
        self.assertEqual(p.name(s, 'emily'), 'Flower friend')

    def test_pin_cap_duplicates_unpin_and_persistence(self):
        s = core.fresh('rei'); d = p.ensure(s)
        s['routes']['emily']['history'].append(dict(role='assistant', channel='text', minute=500, content=json.dumps({'dialogue':'Keep this message'})))
        ident = next(r['id'] for r in p.records(s) if r['text'] == 'Keep this message')
        with self.assertRaisesRegex(ValueError, 'three'): p.pin(s, ident)
        p.unpin(s, d['pins'][0]); p.pin(s, ident); p.pin(s, ident)
        self.assertEqual(len(d['pins']), 3)
        for pin in d['pins'][:]: p.unpin(s, pin)
        self.assertEqual(p.ensure(json.loads(json.dumps(s)))['pins'], [])

    def test_ids_survive_rename_and_repeated_texts_remain_distinct(self):
        s = core.fresh('minsu')
        message = dict(role='assistant', channel='text', minute=500, content=json.dumps({'dialogue':'Hello'}))
        s['routes']['amy']['history'] = [message, copy.deepcopy(message)]
        before = [r['id'] for r in p.records(s) if r['text']=='Hello']
        self.assertEqual(len(set(before)), 2)
        p.rename(s, 'amy', 'Same name'); p.rename(s, 'sophie', 'Same name')
        self.assertEqual(before, [r['id'] for r in p.records(s) if r['text']=='Hello'])

    def test_search_records_exclude_spoken_and_hidden_messages(self):
        s = core.fresh('minsu')
        s['routes']['amy']['history'] = [dict(role='assistant', channel='in_person', content=json.dumps({'dialogue':'Spoken only'}))]
        self.assertNotIn('Spoken only', [r['text'] for r in p.records(s)])
        with self.assertRaises(ValueError): p.pin(s, 'forged')

    def test_names_validate_and_cosmetic_reset_keeps_notes_and_pins(self):
        s = core.fresh(); d = p.ensure(s); d['notes']='Keep'
        for invalid in ('', 'a'*41, 'a\nb'):
            with self.assertRaises(ValueError): p.rename(s, 'april', invalid)
        p.rename(s, 'april', 'Test'); p.unpin(s, d['pins'][0]); pins=d['pins'][:]
        p.reset(s)
        self.assertEqual(d['notes'], 'Keep'); self.assertEqual(d['pins'], pins)
        self.assertNotEqual(p.name(s,'april'), 'Test')

    def test_device_ratio_and_screen_fit(self):
        for width, height in [(1920,1080), (1366,768), (1024,600)]:
            for mode, ratio in [('Phone',(9,16)), ('Tablet',(3,4))]:
                for scale in (60,100,120):
                    w,h=p.size(width,height,mode,scale)
                    self.assertEqual(w*ratio[1],h*ratio[0])
                    self.assertLessEqual(h,height-90); self.assertLessEqual(w,width-40)

    def test_preferences_are_global_not_save_data(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(p,'PREFERENCES',Path(folder)/'prefs.json'), patch.object(p,'_preferences',None):
            p.save_preferences({'text_size':18,'device':'Tablet'})
            p._preferences=None
            self.assertEqual(p.preferences()['text_size'],18)
            self.assertNotIn('text_size',p.ensure(core.fresh()))

    def test_group_message_can_be_pinned_and_spoken_groups_cannot(self):
        import groups
        s=core.fresh('rei')
        gid=groups.create_text(s,'Study',['amy','sophie'])
        s['groups'][gid]['history']=[{'speaker':'Amy Hansen','text':'Bring your notes','minute':500}]
        row=next(r for r in p.records(s) if r['text']=='Bring your notes')
        self.assertTrue(row['group'])
        d=p.ensure(s); p.unpin(s,d['pins'][0]); p.pin(s,row['id'])
        self.assertIn(row['id'],p.ensure(json.loads(json.dumps(s)))['pins'])
        s['groups'][gid]['channel']='in_person'
        self.assertNotIn(row['id'],[r['id'] for r in p.records(s)])

    def test_legacy_contact_alias_is_preserved(self):
        s=core.fresh('rei'); s['nicknames']={'emily':'My old custom name'}
        self.assertEqual(p.name(s,'emily'),'My old custom name')


if __name__ == '__main__': unittest.main()
