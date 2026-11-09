"""Scene projection must not mix phone history, sessions, actions or speakers."""
import unittest
import game_core as core
from hangout_ui import current_exchange, text_pages


class HangoutSceneTests(unittest.TestCase):
    def setUp(self):
        self.state = core.fresh('rei')
        self.group = {'members': ['emily', 'sophie'], 'history': []}

    def add(self, speaker, text, **kw):
        self.group['history'].append(dict(speaker=speaker, text=text, **kw))

    def test_latest_exchange_keeps_speaker_order_and_player(self):
        self.add('Rei Takamura (You)', 'Hello both of you.')
        self.add('Narrator', 'The rain stops.')
        self.add('Sophie Parker', 'Hello!')
        self.add('Emily Fields', 'Shall we walk?')
        scene = current_exchange(self.state, self.group)
        self.assertEqual(scene.player, 'Hello both of you.')
        self.assertEqual(scene.narration, 'The rain stops.')
        self.assertEqual(scene.speeches, [('sophie', 'Hello!'), ('emily', 'Shall we walk?')])

    def test_actions_are_narration_and_pending_replies_are_immediate(self):
        self.add('Rei Takamura (You)', 'I wave.', kind='action')
        self.assertEqual(current_exchange(self.state, self.group).player, '')
        self.assertEqual(current_exchange(self.state, self.group).narration, 'I wave.')
        self.add('Emily Fields', 'Hello!')
        pending = current_exchange(self.state, self.group, 'How are you?')
        self.assertEqual((pending.player, pending.speeches), ('How are you?', []))
        action = current_exchange(self.state, self.group, core.ACTION_PREFIX+'I smile.')
        self.assertEqual((action.player, action.narration), ('', 'I smile.'))
        self.assertFalse(current_exchange(self.state, self.group, core.SCENE_DIRECTIONS[0]).player)

    def test_new_session_never_replays_previous_hangout_or_phone_text(self):
        self.add('Emily Fields', 'Old hangout.')
        self.group['journal_offset'] = 1
        self.add('Status update', 'Hangout began')
        self.add('Emily Fields', 'A private phone message.', channel='text')
        self.add('Unknown person', 'Not present.')
        self.assertEqual(current_exchange(self.state, self.group).speeches, [])

    def test_continuation_replaces_old_response_and_player_bubble(self):
        self.add('Rei Takamura (You)', 'Good morning.')
        self.add('Narrator', 'Sunlight falls on the table.')
        self.add('Emily Fields', 'Morning!')
        self.add('Narrator', 'She leans forward.')
        self.add('Emily Fields', 'One more thing…')
        scene = current_exchange(self.state, self.group)
        self.assertEqual(scene.player, '')
        self.assertEqual(scene.speeches, [('emily', 'One more thing…')])

    def test_paging_preserves_all_text_even_unbroken_unicode(self):
        source = ('A very long speech with punctuation…\n\n' + '花'*120 + '\n') * 8
        pages = text_pages(source, len, 30, 4)
        self.assertGreater(len(pages), 1)
        self.assertEqual(''.join(''.join(pages).split()), ''.join(source.split()))
        self.assertTrue(all(len(line) <= 30 for page in pages for line in page.split('\n')))
        self.assertTrue(all(len(page.split('\n')) <= 4 for page in pages))


if __name__ == '__main__':
    unittest.main()
