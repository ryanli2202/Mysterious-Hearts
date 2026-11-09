import json
import unittest
from PIL import Image
import game_core as core
from messages_ui import text_messages, PROFILE_DIR


class MessageProfilesTests(unittest.TestCase):
    def test_all_message_characters_have_new_profile_art(self):
        for who in set(core.CONTACTS) | set(core.PLAYERS):
            with self.subTest(character=who), Image.open(PROFILE_DIR / f'{who}.png') as image:
                self.assertEqual(image.width, image.height)
                self.assertGreaterEqual(image.width, 512)

    def test_direct_messages_keep_identity_and_exclude_spoken_exchange(self):
        state = core.fresh('rei')
        state['routes'][state['active']]['history'] = [
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'channel': 'in_person', 'content': json.dumps({'dialogue': 'Hi'})},
            {'role': 'user', 'content': 'Coffee?'},
            {'role': 'assistant', 'channel': 'text', 'content': json.dumps({'dialogue': 'yes!'})},
        ]
        messages = text_messages(state, 'At six?')
        self.assertEqual([m[3] for m in messages], ['rei', state['active'], 'rei'])
        self.assertEqual([m[1] for m in messages], ['Coffee?', 'yes!', 'At six?'])

    def test_group_avatar_identity_does_not_depend_on_contact_nickname(self):
        state = core.fresh('garrett')
        group = {'members': ['amy', 'sophie'], 'history': [
            {'speaker': 'Garrett Han (You)', 'text': 'Hey'},
            {'speaker': 'Amy Hansen', 'text': 'hello'},
            {'speaker': 'Sophie Parker', 'text': 'hey!'},
        ]}
        from unittest.mock import patch
        with patch.object(core, 'contact_name', return_value='Same nickname'):
            messages = text_messages(state, group=group)
        self.assertEqual([m[3] for m in messages], ['garrett', 'amy', 'sophie'])
        self.assertEqual([m[2] for m in messages], ['out', 'in', 'in'])
