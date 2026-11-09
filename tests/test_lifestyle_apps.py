import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from datetime import timedelta
from PIL import Image

import camera
import codex_images
import game_core as core
import lifestyle_apps as apps
import phone_apps
import story_calendar
import town


class LifestyleTests(unittest.TestCase):
    def setUp(self):
        self.s = core.fresh('rei')
        self.s['world']['money'] = 1000

    def test_playlist_snapshot_and_privacy_survive_save(self):
        p = apps.save_playlist(self.s, 'River walk', 'First song — Someone\nSecond song — Else', 'Rainy afternoon')
        apps.share_playlist(self.s, p['id'], 'emily')
        p['tracks'].append('Later addition')
        restored = json.loads(json.dumps(self.s))
        self.assertEqual(len(apps.context(restored, ['emily'])['shared_items'][0]['content']['tracks']), 2)
        self.assertEqual(apps.context(restored, ['sophie'])['shared_items'], [])
        self.assertIn('lifestyle', phone_apps.conversation_context(restored, ['emily']))
        with self.assertRaises(ValueError): apps.share_playlist(self.s, p['id'], 'unknown')

    def test_booking_validation_refund_and_no_double_refund(self):
        tomorrow = (story_calendar.story_date(self.s['world']['minute'])+timedelta(days=1)).isoformat()
        item = apps.book(self.s, 'Cinema for two', tomorrow, '17:00', 'emily')
        self.assertEqual(self.s['world']['money'], 976)
        event = self.s['scheduled_events'][-1]
        self.assertEqual(event['venue'], 'cinema')
        with self.assertRaises(ValueError): apps.book(self.s, 'Cinema for two', tomorrow, '17:00', 'emily')
        self.assertEqual(self.s['world']['money'], 976)
        apps.cancel_booking(self.s, item['id'])
        self.assertTrue(event['cancelled'])
        self.assertEqual(self.s['world']['money'], 1000)
        with self.assertRaises(ValueError): apps.cancel_booking(self.s, item['id'])

    def test_wallet_split_and_insufficient_funds(self):
        apps.split_bill(self.s, 41, 3, 'Dinner')
        self.assertEqual(self.s['world']['money'], 986)
        self.s['world']['money'] = 0
        with self.assertRaises(ValueError): apps.split_bill(self.s, 20, 2, 'Lunch')
        self.assertEqual(len(apps.ensure(self.s)['receipts']), 1)
        with self.assertRaises(ValueError): apps.split_bill(self.s, -10, 2, 'Invalid')

    def test_exchange_collection_requires_arrival_and_is_once(self):
        listing = apps.listings(self.s)[0]
        item = apps.buy_listing(self.s, listing['id'])
        with self.assertRaises(ValueError): apps.buy_listing(self.s, listing['id'])
        with self.assertRaises(ValueError): apps.collect(self.s, item['id'])
        self.s['world']['location'] = listing['venue']
        self.s['world']['cast']['rei']['journey'] = None
        apps.collect(self.s, item['id'])
        with self.assertRaises(ValueError): apps.collect(self.s, item['id'])
        self.s['world']['minute'] += 1440
        with self.assertRaises(ValueError): apps.buy_listing(self.s, listing['id'])
        self.assertEqual(self.s['world']['inventory']['exchange:'+listing['id']], 1)
        self.assertIn('exchange:'+listing['id'], phone_apps.gift_options(self.s))

    def test_cooking_and_campus_require_actual_location(self):
        self.s['world']['location'] = 'library'
        with self.assertRaises(ValueError): apps.cook(self.s, 'Honey toast')
        self.s['world']['location'] = town.HOMES['rei']
        apps.cook(self.s, 'Honey toast')
        self.assertEqual(self.s['world']['money'], 995)
        self.assertEqual(self.s['world']['camera_activity']['text'], 'Honey toast')
        apps.join_club(self.s, 'Reading circle')
        with self.assertRaises(ValueError): apps.complete_assignment(self.s, 'Reading circle')
        self.s['world']['location'] = 'library'
        self.s['world']['cast']['rei']['journey'] = None
        apps.complete_assignment(self.s, 'Reading circle')
        with self.assertRaises(ValueError): apps.complete_assignment(self.s, 'Reading circle')

    def test_design_reference_commit_camera_and_wearing(self):
        request = apps.design_request(self.s, 'Evening blue', 'Navy suit and white shirt')
        self.assertTrue(request['references'])
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as folder:
            path = Path(folder)/'image.png'
            Image.new('RGB', (20, 30), 'navy').save(path)
            with patch.object(codex_images, 'STORE', Path(folder)):
                generated = dict(id='test-design', path=str(path))
                item = apps.commit_design(self.s, request, generated)
                apps.commit_design(self.s, request, generated)
                self.assertEqual(len(apps.ensure(self.s)['designs']), 1)
                self.assertEqual(camera.outfits(self.s, 'rei')[item['label']], str(path.resolve()))
                apps.wear(self.s, item['label'])
                self.assertEqual(camera.default_outfit(self.s, 'rei', camera.scene(self.s)), item['label'])
                restored = json.loads(json.dumps(self.s))
                self.assertIn(item['label'], camera.outfits(restored, 'rei'))
        with self.assertRaises(ValueError): apps.wear(self.s, item['label'])

    def test_postcard_has_photo_message_and_private_share(self):
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as folder:
            path = Path(folder)/'image.png'
            Image.new('RGB', (20, 30)).save(path)
            photo = dict(id='photo1', path=str(path), date='2026-01-01', location='Park', mode='Selfie')
            with patch.object(camera, 'photos', return_value=[photo]), patch.object(codex_images, 'STORE', Path(folder)):
                apps.send_postcard(self.s, 'photo1', 'emily', 'Remember our walk?')
            last = self.s['routes']['emily']['history'][-1]
            self.assertEqual(last['photo']['id'], 'photo1')
            self.assertEqual(last['channel'], 'text')
            self.assertEqual(apps.context(self.s, ['sophie'])['shared_items'], [])

    def test_courses_and_new_apps_survive_real_save_load(self):
        apps.enroll(self.s, 'Design fundamentals')
        apps.submit_assignment(self.s, 'Design fundamentals', 'Wool coat with satin lapels.')
        with self.assertRaises(ValueError):
            apps.submit_assignment(self.s, 'Design fundamentals', 'Duplicate submission.')
        apps.save_playlist(self.s, 'Evening', 'A song — An artist')
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as folder:
            path = Path(folder)/'story.json'
            core.save(self.s, path)
            restored = core.load(path)
            self.assertEqual(apps.ensure(self.s), apps.ensure(restored))


if __name__ == '__main__': unittest.main()
