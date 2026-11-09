import json
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import game_core as core
import grove
import grove_gallery as gallery
import phone_apps as apps
import social_world


class GroveGalleryTests(unittest.TestCase):
    def test_sylvanis_added_to_version_twenty_eight_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('sylvanis:')}
        self.assertEqual(len(ids), 8)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'daniel')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep the cinema memory.', 4, existing['id'])
        data['grove_archive_version'] = 28
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'sylvanis')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_daniel_added_to_version_twenty_seven_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('daniel:')}
        self.assertEqual(len(ids), 8)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'valentina')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this sailing memory.', 4, existing['id'])
        data['grove_archive_version'] = 27
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'daniel')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_valentina_added_to_version_twenty_six_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('valentina:')}
        self.assertEqual(len(ids), 8)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'ivan')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this family photo.', 4, existing['id'])
        data['grove_archive_version'] = 26
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'valentina')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_rei_emily_school_archive_migrates_from_version_25(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        keys = set()
        for who in ('rei', 'emily'):
            plan = json.loads((gallery.ROOT / f'assets/grove/{who}/high-school-prompts.json').read_text(encoding='utf-8'))
            keys.update(who + ':' + item['file'][:-4] for item in plan['images'])
        added = [p for p in data['grove_archive'] if p.get('archive_key') in keys]
        self.assertEqual(len(added), 8)
        for who in ('rei', 'emily'):
            school = [p for p in added if p['author'] == who]
            self.assertEqual(len(school), 4)
            self.assertEqual({gallery.timestamp(p)[7:11] for p in school}, {'2046', '2047'})
        ids = {p['id'] for p in added}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'emily')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this memory too.', 4, existing['id'])
        data['grove_archive_version'] = 25
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'rei')), 33)
        self.assertEqual(len(gallery.photos(s, 'emily')), 21)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_sophie_groups_migrate_once_with_school_dates(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        plan = json.loads((gallery.ROOT / 'assets/grove/sophie/group-prompts.json').read_text(encoding='utf-8'))
        keys = {'sophie:' + item['file'][:-4] for item in plan['images']}
        added = [p for p in data['grove_archive'] if p.get('archive_key') in keys]
        self.assertEqual(len(added), 8)
        school = [p for p in added if 'school-' in p['archive_key']]
        self.assertEqual({gallery.timestamp(p)[7:11] for p in school}, {'2046', '2047'})
        self.assertTrue(all('marcus' in item['subjects'] for item in plan['images'] if 'school-' in item['file']))
        ids = {p['id'] for p in added}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'sophie')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this memory.', 4, existing['id'])
        data['grove_archive_version'] = 24
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'sophie')), 20)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_tyler_added_to_version_twenty_three_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('tyler:')}
        self.assertEqual(len(ids), 8)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'elliot')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep the wetland photo.', 4, existing['id'])
        data['grove_archive_version'] = 23
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'tyler')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_elliot_added_to_version_twenty_two_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('elliot:')}
        self.assertEqual(len(ids), 8)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'emily')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this memory.', 4, existing['id'])
        data['grove_archive_version'] = 22
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'elliot')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_yuriko_groups_added_to_version_twenty_one_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        plan = json.loads((gallery.ROOT / 'assets/grove/yuriko/group-prompts.json').read_text(encoding='utf-8'))
        keys = {'yuriko:' + item['file'][:-4] for item in plan['images']}
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key') in keys}
        self.assertEqual(len(ids), 7)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'yuriko')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this workshop memory.', 4, existing['id'])
        data['grove_archive_version'] = 21
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'yuriko')), 15)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_emily_groups_added_to_version_twenty_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        plan = json.loads((gallery.ROOT / 'assets/grove/emily/group-prompts.json').read_text(encoding='utf-8'))
        keys = {'emily:' + item['file'][:-4] for item in plan['images']}
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key') in keys}
        self.assertEqual(len(ids), 9)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'emily')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this flower-shop memory.', 4, existing['id'])
        data['grove_archive_version'] = 20
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'emily')), 21)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_minsu_groups_added_to_version_nineteen_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        plan = json.loads((gallery.ROOT / 'assets/grove/minsu/group-prompts.json').read_text(encoding='utf-8'))
        keys = {'minsu:' + item['file'][:-4] for item in plan['images']}
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key') in keys}
        self.assertEqual(len(ids), 9)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'minsu')[0]
        existing['liked_by'] = ['amy']
        reply = apps._append(data, 'amy', 'Keep this bakery memory.', 4, existing['id'])
        data['grove_archive_version'] = 19
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'minsu')), 17)
        self.assertEqual(existing['liked_by'], ['amy'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_ivan_expansion_added_to_version_eighteen_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        plan = json.loads((gallery.ROOT / 'assets/grove/ivan/expansion-prompts.json').read_text(encoding='utf-8'))
        keys = {'ivan:' + item['file'][:-4] for item in plan['images']}
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key') in keys}
        self.assertEqual(len(ids), 10)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'ivan')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this studio memory.', 4, existing['id'])
        data['grove_archive_version'] = 18
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'ivan')), 20)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_garrett_groups_added_to_version_seventeen_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        plan = json.loads((gallery.ROOT / 'assets/grove/garrett/group-prompts.json').read_text())
        keys = {'garrett:' + item['file'][:-4] for item in plan['images']}
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key') in keys}
        self.assertEqual(len(ids), 9)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'garrett')[0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this shared memory.', 4, existing['id'])
        data['grove_archive_version'] = 17
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'garrett')), 17)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_rosa_added_to_version_sixteen_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('rosa:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep the existing reply.', 4, existing['id'])
        data['grove_archive_version'] = 16
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'rosa')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_dev_added_to_version_fourteen_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('dev:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this conversation going.', 4, existing['id'])
        data['grove_archive_version'] = 14
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'dev')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_rei_groups_added_to_version_thirteen_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        keys = {'rei:' + p['file'][:-4] for p in json.loads(
            (gallery.ROOT / 'assets/grove/rei/group-prompts.json').read_text(encoding='utf-8'))}
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key') in keys}
        self.assertEqual(len(ids), 16)
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = gallery.photos(s, 'rei')[0]
        existing['liked_by'] = ['emily']
        reply = apps._append(data, 'emily', 'Keep this memory.', 4, existing['id'])
        data['grove_archive_version'] = 13
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'rei')), 33)
        self.assertEqual(existing['liked_by'], ['emily'])
        self.assertEqual(reply['parent'], existing['id'])
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_celeste_added_to_version_twelve_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('celeste:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this reply too.', 4, existing['id'])
        data['grove_archive_version'] = 12
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'celeste')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_naomi_added_to_version_eleven_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('naomi:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this conversation.', 4, existing['id'])
        data['grove_archive_version'] = 11
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'naomi')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_lena_added_to_version_ten_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('lena:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Keep this reply.', 4, existing['id'])
        data['grove_archive_version'] = 10
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'lena')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_yuriko_added_to_version_nine_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive']
               if p.get('archive_key', '').startswith('yuriko:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        reply = apps._append(data, 'rei', 'Still here.', 4, existing['id'])
        data['grove_archive_version'] = 9
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'yuriko')), 15)
        self.assertEqual(existing['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], existing['id'])
        self.assertEqual(data['grove_archive_version'], gallery.ARCHIVE_VERSION)
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_april_added_to_version_seven_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key', '').startswith('april:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        data['grove_archive_version'] = 7
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'april')), 8)
        self.assertEqual(existing['liked_by'], ['rei'])
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_amy_added_to_version_six_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key', '').startswith('amy:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        data['grove_archive_version'] = 6
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'amy')), 10)
        self.assertEqual(existing['liked_by'], ['rei'])
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_samantha_added_to_existing_save_without_duplicate_posts(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key', '').startswith('samantha:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        data['grove_archive_version'] = 5
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'samantha')), 14)
        self.assertEqual(existing['liked_by'], ['rei'])
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_sophie_added_to_version_three_save_once(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        ids = {p['id'] for p in data['grove_archive'] if p.get('archive_key', '').startswith('sophie:')}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in ids and p.get('parent') not in ids]
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        data['grove_archive_version'] = 3
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'sophie')), 20)
        self.assertEqual(existing['liked_by'], ['rei'])
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_emily_replacement_preserves_existing_reply_targets(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        keys = {'emily:01-flower-shop-morning', 'emily:02-garden-dinner'}
        removed = {p['id'] for p in data['grove_archive']
                   if p.get('archive_key', '').startswith('emily:') and p['archive_key'] not in keys}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in removed and p.get('parent') not in removed]
        post = next(p for p in data['grove_archive'] if p.get('archive_key') == 'emily:02-garden-dinner')
        post.update(image='assets/gallery/emily-evening.png', text='Old caption', liked_by=['rei'])
        reply = apps._append(data, 'rei', 'Saved reply', 4, post['id'])
        data['grove_archive_version'] = 2
        gallery.ensure(data)
        self.assertEqual(len(gallery.photos(s, 'emily')), 21)
        self.assertEqual(post['image'], 'assets/grove/emily/02-cosy-selfie.png')
        self.assertEqual(post['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], post['id'])
        snapshot = json.loads(json.dumps(data))
        gallery.ensure(data)
        self.assertEqual(data, snapshot)

    def test_emily_added_to_existing_archive_without_resetting_engagement(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        emily_ids = {p['id'] for p in data['grove_archive'] if p.get('image') and p['author'] == 'emily'}
        data['grove_archive'] = [p for p in data['grove_archive']
                                 if p['id'] not in emily_ids and p.get('parent') not in emily_ids]
        data['grove_archive_version'] = 1
        existing = data['grove_archive'][0]
        existing['liked_by'] = ['rei']
        gallery.ensure(data)
        self.assertEqual(existing['liked_by'], ['rei'])
        all_photos = gallery.photos(s, 'emily')
        self.assertEqual(len(all_photos), 21)
        photos = [p for p in all_photos if int(Path(p['image']).name[:2]) <= 8]
        self.assertEqual(len(photos), 8)
        self.assertEqual(sorted(p['likes'] for p in photos), [18, 21, 25, 27, 30, 33, 37, 40])
        for post in photos:
            comments = [p for p in apps.grove_posts(s) if p['parent'] == post['id']]
            self.assertEqual(len(comments), 2)
            self.assertTrue(all(c['minute'] > post['minute'] for c in comments))
        restored = json.loads(json.dumps(s))
        self.assertEqual(apps.ensure(restored), data)

    def test_player_photo_publishing_reactions_and_reload(self):
        import camera
        for who in ('minsu', 'rei', 'ivan'):
            s = core.fresh(who)
            record = dict(id='test-photo', path=gallery.catalog()[0]['image'],
                          snapshot=dict(mode='Selfie', detail='A new painting',
                                        subjects=[dict(id=who)], romance='private'))
            with patch.object(camera, 'photos', return_value=[record]), \
                 patch.object(camera, 'photo_path', return_value=gallery.ROOT / record['path']):
                posted = gallery.publish(s, record['id'], '  Finally finished this!  ')
            self.assertEqual(posted['text'], 'Finally finished this!')
            self.assertEqual(posted['likes'], 0)
            self.assertGreaterEqual(posted['likes_target'], round(grove.FOLLOWERS[who] * .025))
            self.assertLessEqual(posted['likes_target'], round(grove.FOLLOWERS[who] * .15))
            self.assertNotIn('romance', posted['photo_context'])
            restored = json.loads(json.dumps(s))
            self.assertIn(posted, gallery.photos(restored, who))
            jobs = apps.ensure(restored)['grove_pending']
            self.assertTrue(jobs)
            self.assertEqual(len({j['author'] for j in jobs}), len(jobs))
            for job in list(jobs):
                self.assertIn(job['author'], apps.contacts(restored))
                self.assertEqual(job['parent'], posted['id'])
                self.assertEqual(grove.context(restored, job)['thread_ancestry'][0]['photo_context']['detail'], 'A new painting')
                answer = dict(text='Love the colours you picked.', parent=posted['id'])
                with patch.object(core, 'request', return_value={'message': {'content': json.dumps(answer)}}):
                    self.assertTrue(apps.commit_grove(restored, job, grove.generate(restored, job)))
            self.assertEqual(len(gallery.unread_comments(restored)), 3)
            gallery.mark_read(restored, posted['id'])
            self.assertFalse(gallery.unread_comments(restored))

    def test_likes_grow_with_story_time_and_survive_reload(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        post = apps._append(data, 'rei', 'Photo', s['world']['minute'])
        post.update(image='photo.png', likes=0, likes_target=1000, liked_by=['rei'])
        start = post['minute']
        previous = 0
        for elapsed in (0, 1, 30, 120, 720, 1440, 2880):
            s['world']['minute'] = start + elapsed
            apps.ensure(s)
            self.assertGreaterEqual(post['likes'], previous)
            self.assertLessEqual(post['likes'], 1000)
            previous = post['likes']
        self.assertEqual(gallery.like_count(post, 'rei'), 1001)
        restored = json.loads(json.dumps(s))
        self.assertEqual(apps.grove_posts(restored)[-1]['likes'], 1000)
        s['world']['minute'] = start
        apps.ensure(s)
        self.assertEqual(post['likes'], 1000)

    def test_notifications_are_scoped_persistent_and_not_duplicated(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        post = apps._append(data, 'rei', 'Photo', s['world']['minute'])
        post['image'] = 'photo.png'
        who = apps.contacts(s)[0]
        apps.queue_grove(s, who, post['id'])
        job = data['grove_pending'][0]
        result = dict(text='Nice photo!', parent=post['id'])
        self.assertTrue(apps.commit_grove(s, job, result))
        self.assertFalse(apps.commit_grove(s, job, result))
        restored = json.loads(json.dumps(s))
        self.assertEqual(len(gallery.unread_comments(restored)), 1)
        gallery.mark_read(restored, -999)
        self.assertEqual(len(gallery.unread_comments(restored)), 1)
        gallery.mark_read(restored, post['id'])
        self.assertFalse(gallery.unread_comments(restored))
        text_post = apps._append(data, 'rei', 'Only text', s['world']['minute'])
        apps.queue_grove(s, who, text_post['id'])
        apps.commit_grove(s, data['grove_pending'][0], dict(text='Hi', parent=text_post['id']))
        self.assertEqual(len(data['grove_notifications']), 2)
        self.assertEqual(data['grove_notifications'][-1]['kind'], 'post_comment')

    def test_invalid_photo_does_not_publish_or_queue_comments(self):
        import camera
        s = core.fresh('rei')
        with patch.object(camera, 'photos', return_value=[]):
            for caption in ('', 'x' * 281, 'Valid caption'):
                with self.assertRaises(ValueError):
                    gallery.publish(s, 'missing', caption)
        self.assertEqual(apps.ensure(s)['posts'], [])
        self.assertEqual(apps.ensure(s)['grove_pending'], [])

    def test_catalog_content_assets_dates_and_known_commenters(self):
        items = gallery.catalog()
        self.assertEqual(len(items), 271)
        self.assertEqual(len({p['caption'] for p in items}), 271)
        comments = [c['text'] for p in items for c in p['comments']]
        self.assertEqual(len(set(comments)), 342)
        for p in items:
            self.assertLess(datetime.fromisoformat(p['published_at']), gallery.EPOCH)
            self.assertLessEqual(len(p['caption']), 280)
            with Image.open(gallery.ROOT / p['image']) as image:
                image.verify()
            for c in p['comments']:
                self.assertIn(c['author'], social_world.speaker_ties(core.fresh('rei'), p['author']))
                self.assertLessEqual(len(c['text']), 280)

    def test_archive_migration_is_idempotent_and_preserves_live_state(self):
        s = core.fresh('rei')
        live = dict(id=42, author='emily', text='Already here.', minute=12, parent=None)
        job = dict(id=7, author='emily', parent=42)
        s['phone_apps'] = dict(posts=[live], next_id=43, grove_pending=[job])
        data = apps.ensure(s)
        self.assertEqual(data['posts'], [live])
        self.assertEqual(data['grove_pending'], [job])
        self.assertEqual(data['next_id'], 43)
        self.assertEqual(len(data['grove_archive']), 613)
        restored = json.loads(json.dumps(s))
        self.assertEqual(apps.ensure(restored), data)
        self.assertEqual(len(apps.grove_posts(restored)), 614)
        self.assertEqual(apps.grove_posts(restored)[-1], live)
        ids = [p['id'] for p in apps.grove_posts(restored)]
        self.assertEqual(len(ids), len(set(ids)))
        data.pop('grove_archive_version')
        gallery.ensure(data)
        self.assertEqual(len(data['grove_archive']), 613)

    def test_engagement_dates_and_persistent_like_toggle(self):
        s = core.fresh('rei')
        photos = [p for p in apps.grove_posts(s) if p.get('image')]
        self.assertEqual(len(photos), 271)
        for p in photos:
            self.assertGreater(p['likes'], grove.FOLLOWERS[p['author']] * .02)
            self.assertLess(p['likes'], grove.FOLLOWERS[p['author']] * .16)
            self.assertLess(p['minute'], 0)
            authored = next(item for item in gallery.catalog() if item['key'] == p['archive_key'])
            self.assertIn(authored['published_at'][:4], gallery.timestamp(p))
        p = photos[0]
        gallery.toggle_like(s, p['id'])
        restored = json.loads(json.dumps(s))
        saved = next(q for q in apps.grove_posts(restored) if q['id'] == p['id'])
        self.assertEqual(gallery.like_count(saved, 'rei'), p['likes'] + 1)
        gallery.toggle_like(restored, p['id'])
        self.assertEqual(gallery.like_count(saved, 'rei'), p['likes'])
        for who, count in [('garrett', 17), ('rei', 33), ('ivan', 20), ('minsu', 17), ('emily', 21), ('sophie', 20), ('samantha', 14), ('amy', 10), ('april', 8), ('yuriko', 15), ('lena', 8), ('naomi', 8), ('celeste', 8), ('dev', 8), ('rosa', 8)]:
            self.assertEqual(len(gallery.photos(s, who)), count)

    def test_reply_to_archive_and_ai_context(self):
        s = core.fresh('rei')
        p = gallery.photos(s, 'garrett')[0]
        apps.post(s, 'How long did getting ready actually take?', p['id'])
        data = apps.ensure(s)
        job = data['grove_pending'][0]
        context = grove.context(s, job)
        self.assertEqual(context['thread_ancestry'][0]['id'], p['id'])
        self.assertEqual(context['thread_ancestry'][0]['image'], p['image'])
        self.assertTrue(context['photo_archive'])
        answer = {'text': 'long enough. worth it.', 'parent': job['parent']}
        with patch.object(core, 'request', return_value={'message': {'content': json.dumps(answer)}}):
            result = grove.generate(s, job)
        self.assertTrue(apps.commit_grove(s, job, result))
        self.assertEqual(data['posts'][-1]['parent'], job['parent'])
        # Direct queued replies to the historical post are valid too.
        apps.queue_grove(s, 'garrett', p['id'])
        self.assertTrue(apps.commit_grove(s, data['grove_pending'][0], dict(text='five, obviously.', parent=p['id'])))


if __name__ == '__main__':
    unittest.main()
