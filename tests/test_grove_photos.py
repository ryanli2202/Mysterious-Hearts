import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import Mock, patch

import codex_images
import game_core as core
import grove_photos as photos
import phone_apps as apps
import grove_gallery


class CharacterPhotosTests(unittest.TestCase):
    def test_schedule_is_random_character_specific_persistent_and_bounded(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        unscheduled = json.loads(json.dumps(s))
        photos.schedule(s, data, ['sophie', 'amy'])
        for who in ('sophie', 'amy'):
            delay = data['grove_photo_next'][who] - s['world']['minute']
            low, high = photos.INTERVALS[who]
            self.assertTrue(low <= delay <= high)
        # Unrelated random draws must not change the same saved world's schedule.
        for _ in range(20): photos.random.random()
        photos.schedule(unscheduled, apps.ensure(unscheduled), ['sophie', 'amy'])
        self.assertEqual(data['grove_photo_next'], unscheduled['phone_apps']['grove_photo_next'])
        self.assertLess(data['grove_photo_next']['sophie'], data['grove_photo_next']['amy'])
        restored = json.loads(json.dumps(s))
        data = apps.ensure(restored)
        deadlines = dict(data['grove_photo_next'])
        photos.schedule(restored, data, ['sophie', 'amy'])
        self.assertEqual(deadlines, data['grove_photo_next'])
        restored['world']['minute'] += 50000
        photos.schedule(restored, data, ['sophie', 'amy'])
        photos.schedule(restored, data, ['sophie', 'amy'])
        self.assertEqual(len(data['grove_photo_pending']), 2)

    def test_codex_photo_and_caption_commit_to_feed_and_profile(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        photos.schedule(s, data, ['sophie'])
        s['world']['minute'] = data['grove_photo_next']['sophie']
        photos.schedule(s, data, ['sophie'])
        job = data['grove_photo_pending'][0]
        plan = dict(caption='post-run glow', scene='Solo selfie in running clothes.', selfie=True)
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as tmp:
            path = Path(tmp) / 'image.png'
            path.write_bytes(b'test')
            with patch.object(core, 'request', return_value={'message': {'content': json.dumps(plan)}}), \
                 patch.object(codex_images, 'STORE', Path(tmp)), \
                 patch.object(codex_images, 'generate', return_value={'path': str(path)}) as generate:
                result = photos.generate(s, job, threading.Event())
            self.assertIn('sophie-selection.png', generate.call_args.kwargs['references'][0])
            self.assertEqual(data['posts'], [])  # Background worker never mutates live state.
            self.assertTrue(photos.commit(s, job, result))
            self.assertFalse(photos.commit(s, job, result))
            post = data['posts'][-1]
            self.assertEqual(post['text'], plan['caption'])
            self.assertEqual(post['author'], 'sophie')
            self.assertEqual(post['likes'], 0)
            self.assertIn(post, grove_gallery.photos(s, 'sophie'))
            self.assertGreater(data['grove_photo_next']['sophie'], s['world']['minute'])
            s['world']['minute'] += 60
            apps.ensure(s)
            self.assertGreater(post['likes'], 0)

    def test_public_photos_mix_selfies_and_scenery_with_correct_references(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as tmp:
            path = Path(tmp) / 'image.png'
            path.write_bytes(b'test')
            for index, selfie in enumerate((True, False, True, False)):
                plan = dict(caption='Everyday moment', scene='A casual moment', selfie=selfie)
                with patch.object(core, 'request', return_value={'message': {'content': json.dumps(plan)}}) as request, \
                     patch.object(codex_images, 'STORE', Path(tmp)), \
                     patch.object(codex_images, 'generate', return_value={'path': str(path)}) as generate:
                    result = photos.generate(s, dict(author='sophie', id=index), threading.Event())
                self.assertEqual(request.call_args.args[1]['format']['properties']['selfie']['enum'], [selfie])
                references = generate.call_args.kwargs['references']
                self.assertEqual(bool(references), selfie)
                if selfie: self.assertIn('sophie-selection.png', references[0])
                post = apps._append(data, 'sophie', result['text'], s['world']['minute'])
                post.update(image=result['image'], photo_context=result['photo_context'])
        self.assertTrue(photos.next_public_selfie([{}, {'mode': 'Photo of hobby'}]))

    def test_public_plan_cannot_silently_skip_required_selfie(self):
        plan = dict(caption='A park', scene='Trees', selfie=False)
        with patch.object(core, 'request', return_value={'message': {'content': json.dumps(plan)}}), \
             patch.object(codex_images, 'generate') as generate:
            with self.assertRaises(ValueError):
                photos.generate(core.fresh('rei'), dict(author='sophie', id=1), threading.Event())
            generate.assert_not_called()

    def test_invalid_plan_and_cancellation_do_not_generate_images(self):
        s = core.fresh('rei')
        job = dict(author='sophie', id=1)
        for plan, cancelled in [(dict(caption='', scene='a scene', selfie=True), False),
                                (dict(caption='hello', scene='a scene', selfie=True), True)]:
            cancel = threading.Event()
            if cancelled:
                cancel.set()
            with patch.object(core, 'request', return_value={'message': {'content': json.dumps(plan)}}), \
                 patch.object(codex_images, 'generate') as generate:
                with self.assertRaises(ValueError):
                    photos.generate(s, job, cancel)
                generate.assert_not_called()

    def test_worker_failure_retains_job_and_save_switch_discards_result(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        photos.schedule(s, data, ['sophie'])
        s['world']['minute'] = data['grove_photo_next']['sophie']
        photos.schedule(s, data, ['sophie'])
        job = data['grove_photo_pending'][0]
        game = Mock(state_data=s, in_game=True, busy=True, phone_activity=None)
        pump = photos.PhotoPump(game)
        pump.state = s
        pump.cancel = threading.Event()
        pump.results.put((s, job, None, 'Generator unavailable'))
        pump.tick()
        self.assertIsNotNone(pump.error)
        self.assertIn(job, data['grove_photo_pending'])
        self.assertEqual(data['posts'], [])
        game.state_data = core.fresh('minsu')
        pump.cancel = cancel = threading.Event()
        pump.results.put((s, job, dict(text='A photo', image='photo.png', photo_context={}), None))
        pump.tick()
        self.assertTrue(cancel.is_set())
        self.assertEqual(data['posts'], [])
        self.assertEqual(apps.ensure(game.state_data)['posts'], [])
        game.persist.assert_not_called()


if __name__ == '__main__':
    unittest.main()
