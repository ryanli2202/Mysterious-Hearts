import json
import unittest
from pathlib import Path
from PIL import Image

import game_core as core
import grove_gallery as gallery
import phone_apps as apps


class CoupleGalleryTests(unittest.TestCase):
    def test_upgrade_preserves_existing_engagement_and_live_posts(self):
        s = core.fresh('rei')
        d = apps.ensure(s)
        new_ids = {p['id'] for p in d['grove_archive'] if p.get('archive_key', '').split(':')[0] in ('neo', 'alyssa')}
        d['grove_archive'] = [p for p in d['grove_archive'] if p['id'] not in new_ids and p.get('parent') not in new_ids]
        old = gallery.photos(s, 'daniel')[0]
        old['liked_by'] = ['rei']
        reply = apps._append(d, 'rei', 'Keeping this old conversation.', 10, old['id'])
        d['grove_archive_version'] = 29
        gallery.ensure(d)
        for who in ('neo', 'alyssa'):
            self.assertEqual(len(gallery.photos(s, who)), 8)
        self.assertEqual(old['liked_by'], ['rei'])
        self.assertEqual(reply['parent'], old['id'])
        snapshot = json.loads(json.dumps(d))
        gallery.ensure(d)
        self.assertEqual(d, snapshot)

    def test_gallery_assets_and_authored_content(self):
        for who in ('neo', 'alyssa'):
            posts = [p for p in gallery.catalog() if p['author'] == who]
            self.assertEqual(len(posts), 8)
            self.assertEqual(len({p['image'] for p in posts}), 8)
            for post in posts:
                with Image.open(core.ROOT / post['image']) as image:
                    self.assertEqual(image.width, image.height)
                    image.verify()
                self.assertLessEqual(len(post['caption']), 280)
                self.assertTrue(post['comments'])
        manifests = {who: json.loads((core.ROOT / f'assets/grove/{who}/generation-prompts.json').read_text(encoding='utf-8')) for who in ('neo', 'alyssa')}
        neo_prompts = ' '.join(p['prompt'] for p in manifests['neo']['images'])
        self.assertIn('Neo, Tyler and Daniel', neo_prompts)
        self.assertIn('Alyssa', neo_prompts)
