import json
from pathlib import Path
import unittest
from unittest.mock import patch
import test_custom_protagonist as fixture
import game_core as core
import grove
import grove_accounts as accounts
import grove_gallery as gallery
import phone_apps as apps


class GroveAccountTests(unittest.TestCase):
    setUp = fixture.CustomTests.setUp
    create = fixture.CustomTests.create

    def test_requires_explicit_account_and_validates_atomically(self):
        s = self.create()
        with self.assertRaisesRegex(ValueError, 'Create your Grove'):
            apps.post(s, 'Hello')
        with self.assertRaisesRegex(ValueError, 'Create your Grove'):
            gallery.publish(s, 'missing', 'Hello')
        for handle, bio in [('ab', 'bio'), ('bad handle', 'bio'), ('secretvampire', 'bio'), ('new.person', ''), ('new.person', 'x'*281)]:
            with self.assertRaises(ValueError): accounts.save(s, handle, bio)
            self.assertNotIn('grove_account', s)
        accounts.save(s, ' @Alex.Art ', '  New around here.  ')
        self.assertEqual(apps.handle(s['player'], s), '@alex.art')
        self.assertEqual(grove.profile(s, s['player'])['bio'], 'New around here.')
        self.assertEqual(accounts.account(s)['followers'], 0)
        self.assertEqual(apps.contacts(s), [])

    def test_gradual_growth_is_idempotent_after_reload_and_clock_rewind(self):
        s = self.create()
        accounts.save(s, 'alex.art', 'New to Winterfield.')
        apps.post(s, 'My first sketch in the new apartment.')
        self.assertEqual(grove.profile(s, s['player'])['followers'], 0)
        s['world']['minute'] += 720
        self.assertEqual(grove.profile(s, s['player'])['followers'], 2)
        for _ in range(5): apps.ensure(s)
        self.assertEqual(accounts.account(s)['followers'], 2)
        path = Path(self.temp.name)/'grove.json'
        core.save(s, path)
        s = core.load(path)
        s['world']['minute'] += 720
        self.assertEqual(grove.profile(s, s['player'])['followers'], 4)
        s['world']['minute'] -= 1440
        self.assertEqual(grove.profile(s, s['player'])['followers'], 4)
        s['world']['minute'] += 100*1440
        self.assertEqual(grove.profile(s, s['player'])['followers'], 4)
        self.assertEqual(apps.contacts(s), [])

    def test_activity_limits_deduplication_and_no_self_reply_credit(self):
        s = self.create()
        accounts.save(s, 'alex.art', 'Sketches.')
        for text in ('First', ' first ', 'Second', 'Third', 'Fourth'):
            apps.post(s, text)
        own = s['phone_apps']['posts'][0]
        apps.post(s, 'Talking to myself', own['id'])
        other = apps._append(apps.ensure(s), 'emily', 'A new bouquet.', s['world']['minute'])
        for index in range(8): apps.post(s, f'Reply {index}', other['id'])
        self.assertEqual(len(accounts.account(s)['events']), 8)
        s['world']['minute'] += 1440
        self.assertEqual(grove.profile(s, s['player'])['followers'], 17)
        apps.post(s, 'First')
        self.assertEqual(accounts.pending(s), 0)
        apps.post(s, 'A new day, a new drawing.')
        self.assertEqual(accounts.pending(s), 4)

    def test_photos_earn_growth_and_use_current_audience(self):
        s = self.create()
        accounts.save(s, 'alex.art', 'Photos.')
        record = dict(id='test', path=self.relative, snapshot={'mode': 'Selfie'})
        with patch('camera.photos', return_value=[record]), patch('camera.photo_path', return_value=self.image):
            gallery.publish(s, 'test', 'A day at the beach.')
        self.assertEqual(accounts.pending(s), 6)
        s['world']['minute'] += 1440
        self.assertEqual(grove.profile(s, s['player'])['followers'], 6)
        self.assertEqual(apps.contacts(s), [])

    def test_edits_preserve_growth_and_profiles_are_save_scoped(self):
        first, second = self.create(), self.create(name='Jamie')
        accounts.save(first, 'alex.art', 'Sketches.')
        accounts.save(second, 'jamie.cooks', 'Recipes.')
        apps.post(first, 'A new piece.')
        first['world']['minute'] += 1440
        accounts.update(first)
        accounts.save(first, 'alex.draws', 'More sketches.')
        self.assertEqual(grove.profile(first, first['player'])['followers'], 4)
        self.assertEqual(apps.handle(second['player'], second), '@jamie.cooks')
        self.assertEqual(grove.profile(second, second['player'])['followers'], 0)
        with self.assertRaises(ValueError): accounts.save(first, 'itsjustemily', 'Oops')
        self.assertEqual(apps.handle(first['player'], first), '@alex.draws')
        self.assertEqual(grove.profile(first, 'emily')['followers'], grove.FOLLOWERS['emily'])

    def test_old_custom_posts_are_preserved_without_retroactive_growth(self):
        s = self.create()
        old = apps._append(apps.ensure(s), s['player'], 'An older post.', s['world']['minute'])
        s['world']['minute'] += 1440
        accounts.save(s, 'alex.art', 'Back online.')
        self.assertIn(old, apps.grove_posts(s))
        self.assertEqual(accounts.pending(s), 0)

    def test_context_uses_chosen_handle_and_authored_profiles_stay_fixed(self):
        s = self.create()
        accounts.save(s, 'alex.art', 'Public sketchbook.')
        apps.post(s, 'Hello Winterfield!')
        payload = grove.context(s, dict(author='emily', parent=1))
        self.assertEqual(payload['participant_handles'][s['player']], '@alex.art')
        self.assertEqual(apps.conversation_context(s, ['emily'])['speaker_handles'][s['player']], '@alex.art')
        old = core.fresh('rei')
        apps.post(old, 'A new sketch.')
        old['world']['minute'] += 1440
        apps.ensure(old)
        self.assertEqual(grove.profile(old, 'rei')['followers'], grove.FOLLOWERS['rei'])
