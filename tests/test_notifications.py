import copy
import json
import unittest
from unittest.mock import Mock

import game_core as core
import phone_apps as apps
from notifications_ui import NotificationPopups


class NotificationTests(unittest.TestCase):
    def setUp(self):
        self.state = core.fresh('rei')
        self.popups = NotificationPopups(Mock())
        self.popups.show_next = Mock()
        self.popups.observe(self.state)

    def test_new_messages_even_when_read_and_no_replay_on_load(self):
        route = self.state['routes']['emily']
        route['history'].append(dict(role='assistant', channel='text',
                                     content=json.dumps({'dialogue': 'Hello!'})))
        route['unread'] = 0
        self.popups.observe(self.state)
        self.assertEqual(len(self.popups.pending), 1)
        self.assertEqual(self.popups.pending[0][1], 'Hello!')
        self.popups.observe(self.state)
        self.assertEqual(len(self.popups.pending), 1)
        self.popups.observe(copy.deepcopy(self.state))
        self.assertFalse(self.popups.pending)

    def test_group_messages_exclude_player_and_narrator(self):
        self.state['groups']['test'] = dict(channel='text', name='Friends', history=[
            dict(speaker='Rei (You)', text='Hey'), dict(speaker='Narrator', text='Arrived'),
            dict(speaker='Emily', text='Hi'), dict(speaker='Sophie', text='Hello')])
        self.popups.observe(self.state)
        self.assertEqual([p[1] for p in self.popups.pending], ['Emily: Hi', 'Sophie: Hello'])

    def test_text_post_comments_and_replies(self):
        data = apps.ensure(self.state)
        post = apps._append(data, 'rei', 'My day', 0)
        job = apps.queue_grove(self.state, 'emily', post['id'])
        apps.commit_grove(self.state, job, dict(text='Lovely!', parent=post['id']))
        other = apps._append(data, 'sophie', 'A day out', 0)
        comment = apps._append(data, 'rei', 'Where?', 0, other['id'])
        job = apps.queue_grove(self.state, 'sophie', comment['id'])
        apps.commit_grove(self.state, job, dict(text='The park', parent=comment['id']))
        self.popups.observe(self.state)
        self.assertEqual([n['kind'] for n in data['grove_notifications']], ['post_comment', 'reply'])
        self.assertEqual(len(self.popups.pending), 2)
        self.assertIn('commented on your post', self.popups.pending[0][0])
        self.assertIn('replied to your comment', self.popups.pending[1][0])
        self.popups.observe(self.state)
        self.assertEqual(len(self.popups.pending), 2)

    def test_meet_cute_notices_name_sender_without_replaying_on_reload(self):
        import meet_cute
        meet_cute.notice(self.state,'lena','Liked your prompt.')
        self.popups.observe(self.state)
        self.assertEqual(self.popups.pending[0],('Meet-Cute','Lena Ortiz: Liked your prompt.'))
        self.popups.observe(self.state)
        self.assertEqual(len(self.popups.pending),1)
        self.popups.observe(copy.deepcopy(self.state))
        self.assertFalse(self.popups.pending)


if __name__ == '__main__':
    unittest.main()
