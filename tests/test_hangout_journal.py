import json
import unittest
import game_core as core
import groups


class HangoutJournalTests(unittest.TestCase):
    def test_separate_sessions_preserve_their_own_transcripts(self):
        s = core.fresh('rei')
        gid = groups.open_solo(s, 'emily')
        s['groups'][gid]['history'].append({'speaker': 'Emily', 'text': 'First visit.'})
        groups.close_active(s, 'Goodbye')
        s['world']['minute'] += 60
        groups.open_solo(s, 'emily')
        s['groups'][gid]['history'].append({'speaker': 'Emily', 'text': 'Second visit.'})
        groups.close_active(s, 'See you later')
        entries = s['hangout_journal']
        self.assertEqual(len(entries), 2)
        self.assertIn('First visit.', str(entries[0]['history']))
        self.assertNotIn('Second visit.', str(entries[0]['history']))
        self.assertNotIn('First visit.', str(entries[1]['history']))
        self.assertGreater(entries[1]['started'], entries[0]['started'])
        self.assertEqual(json.loads(json.dumps(entries)), entries)
        groups.close_active(s, 'Already closed')
        self.assertEqual(len(entries), 2)

    def test_text_messages_are_not_hangouts(self):
        s = core.fresh('rei')
        gid = groups.create_text(s, 'Friends', ['emily', 'garrett'])
        s['groups'][gid]['history'].append({'speaker': 'Emily', 'text': 'A text.'})
        self.assertFalse(s.get('hangout_journal'))
