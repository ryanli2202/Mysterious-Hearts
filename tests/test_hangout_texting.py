import unittest
from unittest.mock import patch
import game_core as core
import groups


class HangoutTextingTests(unittest.TestCase):
    def test_direct_text_blocked_before_ai_and_commit(self):
        s = core.fresh('rei')
        groups.open_solo(s, 'emily')
        s['active'] = 'emily'
        s['routes']['emily']['channel'] = 'text'
        with patch.object(core, 'request') as request:
            with self.assertRaisesRegex(ValueError, 'hanging out'): core.build_messages(s, 'Hello')
            with self.assertRaisesRegex(ValueError, 'hanging out'): core.commit(s, 'Hello', {})
            request.assert_not_called()
        groups.require_text_available(s, ['garrett'])
        groups.close_active(s, 'Finished')
        groups.require_text_available(s, ['emily'])

    def test_group_cannot_bypass_active_hangout(self):
        s = core.fresh('rei')
        gid = groups.create_text(s, 'Friends', ['emily', 'garrett'])
        groups.open_solo(s, 'emily')
        with self.assertRaisesRegex(ValueError, 'hanging out'): groups.generate(s, gid, 'Hello')
        with self.assertRaisesRegex(ValueError, 'hanging out'): groups.commit(s, gid, 'Hello', {})
        self.assertEqual(s['groups'][gid]['history'], [])

    def test_merely_sharing_location_does_not_block_texts(self):
        s = core.fresh('rei')
        s['world']['cast']['emily']['location'] = s['world']['location']
        groups.require_text_available(s, ['emily'])
