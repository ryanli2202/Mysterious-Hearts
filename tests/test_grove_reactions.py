import json
import unittest
from unittest.mock import Mock, patch
import game_core as core
import grove
import grove_reactions as reactions
import phone_apps as apps


class PhotoReactionsTests(unittest.TestCase):
    def test_delays_reload_relationship_context_and_player_reply(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        post = apps._append(data, 'sophie', 'Training done.', s['world']['minute'])
        post.update(image='photo.png', photo_context={'detail': 'Track selfie'})
        s['bond_details']['emily:sophie'] = dict(trust=30, tension=80, closeness=10)
        with patch.object(apps, 'contacts', return_value=['sophie', 'emily', 'amy']), \
             patch('social_world.speaker_ties', return_value={'sophie': ('Friends', '')}):
            reactions.sync(s, data)
            self.assertNotIn('liked_by', post)
            self.assertEqual(data['grove_pending'], [])
            self.assertEqual(len(data['grove_reactions']), 4)
            s = json.loads(json.dumps(s))
            data = apps.ensure(s)
            post = data['posts'][0]
            s['world']['minute'] += 1000
            reactions.sync(s, data)
            reactions.sync(s, data)
            self.assertEqual(post['liked_by'], ['amy'])
            self.assertEqual(len(data['grove_pending']), 2)
            job = next(j for j in data['grove_pending'] if j['author'] == 'emily')
            context = grove.context(s, job)
            self.assertEqual(context['thread_ancestry'][0]['photo_context']['detail'], 'Track selfie')
            self.assertEqual(context['voice'], core.TEXT_STYLES['emily'])
            self.assertEqual(next(r for r in context['relationships'] if r['with'] == 'sophie')['current_state']['tension'], 80)
            result = dict(text='Hope training went well.', parent=post['id'])
            with patch.object(core, 'request', return_value={'message': {'content': json.dumps(result)}}):
                apps.commit_grove(s, job, grove.generate(s, job))
            comment = data['posts'][-1]
            apps.post(s, 'Did you train together?', comment['id'])
            reply = data['posts'][-1]
            followup = next(j for j in data['grove_pending'] if j['parent'] == reply['id'])
            self.assertEqual(followup['author'], 'emily')
            self.assertEqual([p['id'] for p in grove.context(s, followup)['thread_ancestry']],
                             [post['id'], comment['id'], reply['id']])
            reactions.sync(s, data)
            self.assertEqual(post['liked_by'], ['amy'])
            self.assertTrue(all(r['kind'] == 'reply' for r in data['grove_reactions']))

    def test_character_conversation_delays_and_stops_at_budget(self):
        s = core.fresh('rei')
        data = apps.ensure(s)
        root = apps._append(data, 'sophie', 'How was training?', s['world']['minute'])
        job = apps.queue_grove(s, 'emily', root['id'])
        rng = Mock()
        rng.random.return_value = 0
        rng.randint.return_value = 3
        with patch.object(reactions.random, 'Random', return_value=rng):
            apps.commit_grove(s, job, dict(text='Hard work today!', parent=root['id']))
            first = data['posts'][-1]
            self.assertEqual(data['grove_pending'], [])
            self.assertEqual(data['grove_reactions'][0]['author'], 'sophie')
            s = json.loads(json.dumps(s))
            data = apps.ensure(s)
            for depth in range(1, 5):
                s['world']['minute'] += 3
                reactions.sync(s, data)
                job = data['grove_pending'][0]
                self.assertEqual(job['auto_reply_depth'], depth)
                self.assertNotEqual(job['author'], data['posts'][-1]['author'])
                apps.commit_grove(s, job, dict(text=f'Follow-up {depth}', parent=job['parent']))
                self.assertFalse(apps.commit_grove(s, job, dict(text='Duplicate', parent=job['parent'])))
            self.assertEqual(data['grove_reactions'], [])
            self.assertEqual(data['grove_pending'], [])
            self.assertEqual(len(data['posts']), 6)

    def test_reply_notification_on_someone_elses_photo(self):
        import grove_gallery as gallery
        s = core.fresh('rei')
        data = apps.ensure(s)
        root = apps._append(data, 'sophie', 'Photo!', s['world']['minute'])
        root['image'] = 'photo.png'
        apps.post(s, 'Where did you get those shoes?', root['id'])
        player_comment = data['posts'][-1]
        job = data['grove_pending'][0]
        result = dict(text='The sports shop downtown.', parent=player_comment['id'])
        apps.commit_grove(s, job, result)
        self.assertFalse(apps.commit_grove(s, job, result))
        restored = json.loads(json.dumps(s))
        notices = gallery.unread_comments(restored)
        self.assertEqual(len(notices), 1)
        self.assertEqual(notices[0]['kind'], 'reply')
        self.assertEqual(notices[0]['post_id'], root['id'])
        gallery.mark_read(restored, root['id'])
        self.assertEqual(gallery.unread_comments(restored), [])
        # Replies to another NPC do not notify the player just for participating.
        npc = apps._append(data, 'emily', 'Nice shoes', s['world']['minute'], root['id'])
        job = apps.queue_grove(s, 'sophie', npc['id'])
        apps.commit_grove(s, job, dict(text='Thanks!', parent=npc['id']))
        self.assertEqual(len(data['grove_notifications']), 1)

    def test_no_player_self_or_unintroduced_character_reactions(self):
        s = core.fresh('rei')
        s['bond_details'] = {}
        data = apps.ensure(s)
        post = apps._append(data, 'sophie', 'Photo', s['world']['minute'])
        post['image'] = 'photo.png'
        with patch('social_world.speaker_ties', return_value={}), \
             patch.object(apps, 'contacts', return_value=['sophie', 'emily']):
            reactions.sync(s, data)
        self.assertEqual(data['grove_reactions'], [])


if __name__ == '__main__':
    unittest.main()
