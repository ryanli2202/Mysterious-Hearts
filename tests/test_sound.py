import unittest
from unittest.mock import Mock, patch

from sound import SoundSystem


class TextSoundTests(unittest.TestCase):
    def setUp(self):
        with patch('sound.sys.platform', 'test'):
            self.sounds = SoundSystem()
        self.sounds.play = Mock()
        self.state = {'routes': {'amy': {'history': [
            {'role': 'assistant', 'channel': 'text'}]}}, 'groups': {}}
        self.sounds.observe(self.state)

    def test_history_and_spoken_dialogue_are_silent(self):
        self.sounds.observe(self.state)
        self.state['routes']['amy']['history'].append({'role': 'assistant', 'channel': 'in_person'})
        self.sounds.observe(self.state)
        self.sounds.play.assert_not_called()

    def test_new_text_notifies_once(self):
        self.state['routes']['amy']['history'].append({'role': 'assistant', 'channel': 'text'})
        self.sounds.observe(self.state)
        self.sounds.observe(self.state)
        self.sounds.play.assert_called_once_with('received')

    def test_loading_another_save_is_silent(self):
        import copy
        other = copy.deepcopy(self.state)
        other['routes']['amy']['history'] *= 4
        self.sounds.observe(other)
        self.sounds.play.assert_not_called()

    def test_contact_tone_and_silent_contact(self):
        self.state['phone_personalization']={'tones':{'amy':'Silent'}}
        self.state['routes']['amy']['history'].append({'role':'assistant','channel':'text'})
        self.sounds.observe(self.state); self.sounds.play.assert_not_called()
        self.state['phone_personalization']['tones']['amy']='Chime'
        self.state['routes']['amy']['history'].append({'role':'assistant','channel':'text'})
        self.sounds.observe(self.state); self.sounds.play.assert_called_once_with('tone_chime')

    def test_group_text_only(self):
        self.state['groups']['friends'] = {'channel': 'in_person', 'history': [{'speaker': 'Amy'}]}
        self.sounds.observe(self.state)
        self.sounds.play.assert_not_called()
        self.state['groups']['texts'] = {'channel': 'text', 'history': [{'speaker': 'Rei (You)'}]}
        self.sounds.observe(self.state)
        self.sounds.play.assert_not_called()
        self.state['groups']['texts']['history'].extend([{'speaker': 'Amy'}, {'speaker': 'Emily'}])
        self.sounds.observe(self.state)
        self.sounds.play.assert_called_once_with('received')

    def test_typing_loops_and_resumes_only_while_generating(self):
        sounds = self.sounds
        sounds._mci = Mock(return_value=0)
        sounds._aliases = {'typing': 'test_typing'}
        sounds.set_typing(True)
        sounds._mci.assert_any_call('setaudio test_typing volume to 500', None, 0, None)
        sounds._mci.assert_called_with('play test_typing from 0 repeat', None, 0, None)
        sounds.set_typing(True)
        self.assertEqual(sounds._mci.call_count, 2)
        sounds.toggle()
        sounds._mci.assert_called_with('stop test_typing', None, 0, None)
        sounds.toggle()
        sounds._mci.assert_called_with('play test_typing from 0 repeat', None, 0, None)
        sounds.toggle()
        sounds.set_typing(False)
        sounds._mci.reset_mock()
        sounds.toggle()
        sounds._mci.assert_not_called()
        sounds.set_typing(True)
        sounds.set_typing(False)
        sounds._mci.assert_called_with('stop test_typing', None, 0, None)
        sounds.close()
        self.assertFalse(sounds._typing)

    def test_mute_and_cleanup(self):
        with patch('sound.sys.platform', 'test'):
            sounds = SoundSystem()
        sounds._mci = Mock(return_value=0)
        sounds._aliases = {'sent': 'test_sent'}
        sounds.toggle()
        sounds.play('sent')
        sounds._mci.assert_called_once_with('stop test_sent', None, 0, None)
        sounds.toggle()
        sounds.play('sent')
        sounds._mci.assert_called_with('play test_sent from 0', None, 0, None)
        sounds.close()
        sounds._mci.assert_called_with('close test_sent', None, 0, None)

    def test_voicemail_switch_mute_and_cleanup(self):
        sounds = self.sounds
        sounds._mci = Mock(return_value=0)
        sounds.play_voicemail('april')
        first = sounds._voicemail
        sounds.play_voicemail('rei')
        self.assertIn(((f'close {first}', None, 0, None),),
                      [tuple(call)[:1] for call in sounds._mci.call_args_list])
        self.assertFalse(sounds.voicemail_playing('april'))
        self.assertEqual(sounds._voicemail_character, 'rei')
        sounds.toggle()
        self.assertIsNone(sounds._voicemail)
        with self.assertRaisesRegex(ValueError, 'Turn sound on'):
            sounds.play_voicemail('rei')
        sounds.toggle()
        sounds.play_voicemail('garrett')
        sounds.close()
        self.assertIsNone(sounds._voicemail)

    def test_voicemail_files_and_errors(self):
        sounds = self.sounds
        for who in ('april', 'garrett', 'ivan', 'rei', 'yuriko'):
            self.assertTrue(sounds.voicemail_path(who).is_file())
        self.assertIsNone(sounds.voicemail_path('../typing'))
        with self.assertRaisesRegex(ValueError, 'No voicemail'):
            sounds.play_voicemail('missing')
        sounds._mci = Mock(side_effect=[0, 0, 1, 0])
        with self.assertRaisesRegex(ValueError, 'Could not play'):
            sounds.play_voicemail('rei')
        self.assertIsNone(sounds._voicemail)

    def test_voicemail_completion_releases_audio(self):
        sounds = self.sounds
        sounds._mci = Mock(return_value=0)
        sounds.play_voicemail('ivan')
        # Empty/non-playing mode signals completion.
        self.assertFalse(sounds.voicemail_playing('ivan'))
        self.assertIsNone(sounds._voicemail)


if __name__ == '__main__':
    unittest.main()
