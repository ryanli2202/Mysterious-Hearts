import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import game_core as c

SCENE = {'speaker': 'Emily Fields', 'addressee': 'Garrett Han', 'choices_speaker': 'Garrett Han', 'narration': 'Emily sets down the watering can.', 'dialogue': 'It is good to see you.',
         'choices': ['I wonder how work was.', 'I offer to help.', 'I would like to invite you to dinner.', 'I would love to hear about your flowers.'],
         'memory': 'The player visited Emily at the flower shop.'}

class Tests(unittest.TestCase):
    def test_queued_phone_reply_with_empty_summary_reopens(self):
        import messaging
        state = c.fresh()
        messaging.initiate(state, 'emily', 'Say hello.')
        job = dict(key='emily', who='emily', group=False, ids=[], text='',
                   reason=messaging.thread(state, 'emily')['reason'])
        self.assertTrue(messaging.apply(state, job, dict(
            bubbles=['hello!'], moment='none', pause_minutes=0)))
        self.assertEqual(state['routes']['emily']['memory'], '')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'story.json'
            c.save(state, path)
            restored = c.load(path)
        for field in ('history', 'dialogue', 'scene', 'memory', 'choices', 'unread'):
            self.assertEqual(restored['routes']['emily'][field], state['routes']['emily'][field])
        self.assertIn('hello!', str(c.transcript(restored)))

    def test_empty_summary_is_valid_but_missing_scene_content_is_not(self):
        c.validate_response({**SCENE, 'memory': ''})
        for field in ('narration', 'dialogue', 'memory'):
            invalid_values = [None, 42] + (['', '   '] if field != 'memory' else [])
            for value in invalid_values:
                with self.subTest(field=field, value=value), self.assertRaisesRegex(ValueError, field):
                    c.validate_response({**SCENE, field: value})
            incomplete = dict(SCENE)
            del incomplete[field]
            with self.assertRaisesRegex(ValueError, field):
                c.validate_response(incomplete)

    def setUp(self):
        self.provider_patch = patch.object(c.chatgpt_provider, 'settings', return_value={'provider':'ollama','model':''})
        self.provider_patch.start()
        self.addCleanup(self.provider_patch.stop)
    def test_text_openings_and_legacy_conversations(self):
        for player in c.playable_cast.ORIGINAL:
            for who in c.PEOPLE:
                state = c.fresh(player); state['active'] = who
                c.hidden.mark_met(state, who)
                if who in c.hidden.CAST: c.hidden.add_contact(state, who)
                messages = c.build_messages(state, c.INCOMING_TEXT)
                self.assertTrue(c.is_texting(state))
                self.assertIn(c.TEXT_STYLES[who], messages[0]['content'])
                self.assertEqual(json.loads(messages[-1]['content'])['kind'], 'scene_direction')
        state = c.fresh()
        c.commit(state, c.INCOMING_TEXT, SCENE)
        blocks = c.transcript(state)
        self.assertNotIn('Garrett Han (You)', [b[0] for b in blocks])
        self.assertNotIn(c.INCOMING_TEXT, str(blocks))
        self.assertIn('Emily Fields', [b[0] for b in blocks])
        del state['routes']['emily']['channel']
        self.assertFalse(c.is_texting(state))
        state['active'] = 'sophie'
        del state['routes']['sophie']['channel']
        self.assertTrue(c.is_texting(state))

    def test_meeting_established_in_conversation_switches_mode(self):
        state = c.fresh()
        c.town.travel(state, 'flowers'); c.town.finish_drive(state)
        c.commit(state, 'I open the door and greet Emily.',
                 {**SCENE, 'conversation_channel': 'in_person'})
        self.assertFalse(c.is_texting(state))
        self.assertIn('In-person conversation', c.transcript(state)[0][1])
        self.assertIn(SCENE['narration'], str(c.transcript(state, pane='dialogue')))
        self.assertNotIn(SCENE['narration'], str(c.transcript(state, pane='actions')))

    def test_hangout_transition_and_action_history(self):
        state = c.fresh()
        c.commit(state, c.INCOMING_TEXT, SCENE)
        c.town.travel(state, 'flowers'); c.town.finish_drive(state)
        c.town.meet(state, 'emily')
        self.assertFalse(c.is_texting(state))
        self.assertEqual(state['routes']['emily']['choices'], [])
        self.assertIn('In-person conversation', c.transcript(state)[-1][1])
        c.town.meet(state, 'emily')
        self.assertEqual(sum(m['role'] == 'status' for m in state['routes']['emily']['history']), 1)
        action = c.ACTION_PREFIX + 'I offer to help water the flowers.'
        c.commit(state, action, SCENE)
        self.assertEqual(c.player_message(state, action)['kind'], 'player_action')
        self.assertIn('I offer to help', str(c.transcript(state, pane='actions')))
        self.assertIn(SCENE['narration'], str(c.transcript(state, pane='dialogue')[-2:]))
        messages = c.build_messages(state, action)
        self.assertNotIn('status', [m['role'] for m in messages])
        self.assertIn('IN-PERSON MODE', messages[0]['content'])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'story.json'
            c.save(state, path)
            self.assertEqual(c.load(path), state)
        c.town.travel(state, 'home'); c.town.finish_drive(state); c.town.rest(state)
        self.assertTrue(c.is_texting(state))
        self.assertIn('Back to phone texts', str(c.transcript(state)))

    def test_texting_styles_and_spoken_mode(self):
        for who in c.CONTACTS:
            state = c.fresh(); state['active'] = who
            c.hidden.mark_met(state, who)
            if who in c.hidden.CAST: c.hidden.add_contact(state, who)
            prompt = c.build_messages(state, 'Hello')[0]['content']
            self.assertIn(c.TEXT_STYLES[who], prompt)
        self.assertIn('kaomoji', c.TEXT_STYLES['emily'])
        self.assertIn('lowercase', c.TEXT_STYLES['emily'])
        self.assertIn('Proper capitalization', c.TEXT_STYLES['april'])
        state = c.fresh(); c.town.travel(state, 'flowers'); c.town.finish_drive(state); c.town.meet(state, 'emily')
        prompt = c.build_messages(state, 'Hello')[0]['content']
        self.assertIn('no emoji, kaomoji', prompt)
        self.assertNotIn(c.TEXT_STYLES['emily'], prompt)

    def test_generated_actions_on_first_in_person_turn(self):
        state = c.fresh()
        c.town.travel(state, 'flowers'); c.town.finish_drive(state)
        actions = ['I wave hello.', 'I set my phone aside to listen.', 'I salute the watering can.', 'I wink at Emily.']
        scene = {**SCENE, 'conversation_channel': 'in_person'}
        response = {'choices_speaker': 'Garrett Han', 'choices': SCENE['choices'], 'action_choices': actions,
                    'personal_choices': c.personal_choices(state, {})}
        with patch.object(c, 'request', return_value={'message': {'content': json.dumps(response)}}) as req:
            result = c.generate_player_choices(state, 'I open the door.', scene)
        body = req.call_args.args[1]
        self.assertIn('action_choices', body['format']['required'])
        self.assertIn('1 friendly, 2 sincere, 3 funny, 4 flirtatious', body['messages'][0]['content'])
        self.assertIn(c.ACTION_GUIDE, body['messages'][0]['content'])
        self.assertNotIn('These are short phone text replies', body['messages'][0]['content'])
        c.commit(state, 'I open the door.', result)
        self.assertEqual(c.action_choices(state), actions)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'story.json'; c.save(state, path)
            self.assertEqual(c.action_choices(c.load(path)), actions)
        for bad in [[], ['same'] * 4, ['a', 'b', 'c', None]]:
            with self.assertRaises(ValueError): c.validate_response({**SCENE, 'action_choices': bad})
        c.town.travel(state, 'square'); c.town.finish_drive(state)
        self.assertEqual(c.action_choices(state), [])

    def test_action_tones_on_resuming_a_hangout_and_selecting_a_gesture(self):
        for player, who, tones in [('rei', 'yuriko', c.SIBLING_TONES), ('ivan', 'valentina', c.SIBLING_TONES),
                                   ('ivan', 'sylvanis', c.HOSTILE_TONES), ('minsu', 'yuriko', c.REPLY_TONES)]:
            with self.subTest(player=player, who=who):
                state = c.fresh(player)
                state['active'] = who
                route = state['routes'][who]
                route.update(channel='in_person', ordered_tones=True, action_choices=['old gesture'] * 4)
                self.assertEqual(c.choice_tones(state), tones)
                self.assertIn('4 ' + tones[3].lower(), c.tone_guide(state))
                actions = c.action_choices(state)
                self.assertEqual(len(set(actions)), 4)
                self.assertNotIn('old gesture', actions)
                with patch.object(c.town, 'social_event') as event:
                    c.commit(state, c.ACTION_PREFIX + actions[3], SCENE)
                self.assertEqual(event.call_args.args[2], 'flirt' if tones == c.REPLY_TONES else 'none')

    def test_routes_and_save_roundtrip(self):
        state = c.fresh('rei')
        c.commit(state, 'Hello', SCENE)
        self.assertEqual(state['turn'], 1)
        self.assertEqual(state['routes']['sophie']['history'], [])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'save.json'
            c.save(state, path)
            self.assertEqual(c.load(path), state)
            path.write_text('{bad json', encoding='utf-8')
            with self.assertRaises(ValueError): c.load(path)

    def test_invalid_model_output_never_committed(self):
        state = c.fresh()
        for choices in [[], ['same'] * 4, ['one', 'two', 'three', None]]:
            with self.assertRaises(ValueError): c.commit(state, 'Hello', {**SCENE, 'choices': choices})
        self.assertEqual(state['turn'], 0)
        self.assertEqual(state['routes']['emily']['history'], [])

    def test_feelings_follow_people_across_chats_and_saves(self):
        state = c.fresh('rei')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'story.json'
            del state['emotions']  # An existing save from before feelings were tracked.
            c.save(state, path)
            state = c.load(path)
            self.assertEqual(c.feeling_labels(state, ['emily']),
                             [('Rei Takamura (You)', 'content'), ('Emily Fields', 'content')])
            c.commit(state, 'I miss everyone.', dict(SCENE, emotions={'rei':'lonely', 'emily':'grateful'}))
            state['active'] = 'amy'
            c.commit(state, c.INCOMING_TEXT, dict(SCENE, emotions={'rei':'flirty', 'amy':'inspired'}))
            state['nicknames'] = {'amy': 'Ames'}
            self.assertEqual(c.feeling_labels(state, ['amy', 'emily']),
                             [('Rei Takamura (You)', 'lonely'), ('Ames', 'inspired'), ('Emily Fields', 'grateful')])
            c.save(state, path)
            self.assertEqual(c.load(path)['emotions'], state['emotions'])

    def test_reject_invalid_feelings_before_recording_a_turn(self):
        state = c.fresh()
        for report in (None, {'garrett': 'happy'}, {'garrett': 'happy', 'emily': 'unknown'},
                       {'garrett': 'happy', 'emily': 'content', 'amy': 'angry'}):
            with self.subTest(report=report), self.assertRaises(ValueError):
                c.commit(state, 'Hello', dict(SCENE, emotions=report))
        self.assertFalse(state['emotions'])
        self.assertEqual(state['turn'], 0)
        self.assertFalse(state['routes']['emily']['history'])

    def test_context_is_correct_for_every_pair(self):
        for player in c.playable_cast.ORIGINAL:
            for who in c.PEOPLE:
                state = c.fresh(player); state['active'] = who
                c.hidden.mark_met(state, who)
                if who in c.hidden.CAST: c.hidden.add_contact(state, who)
                messages = c.build_messages(state, 'Hello')
                self.assertIn(c.PLAYERS[player], messages[0]['content'])
                self.assertIn(c.PEOPLE[who][0], messages[0]['content'])
                styles = json.loads((c.ROOT / 'dialogue_styles.json').read_text(encoding='utf-8'))
                self.assertIn(styles[who], messages[0]['content'])
                self.assertIn(styles[player + '_player'], messages[0]['content'])
                self.assertIn((c.ROOT / 'ai_directions.txt').read_text(encoding='utf-8'), messages[0]['content'])
                for other in c.PEOPLE:
                    if other != who:
                        self.assertNotIn(styles[other], messages[0]['content'])
                self.assertEqual(json.loads(messages[-1]['content']), {'kind': 'player_reply', 'speaker': c.PLAYERS[player], 'addressee': c.PEOPLE[who][0], 'text': 'Hello'})

    def test_wrong_speaker_is_rejected(self):
        state = c.fresh()
        c.validate_response(SCENE, state)
        for field in ('speaker', 'addressee', 'choices_speaker'):
            with self.assertRaises(ValueError):
                c.validate_response({**SCENE, field: 'Rei Takamura'}, state)
        with self.assertRaises(ValueError):
            c.validate_response({**SCENE, 'dialogue': 'Hello.\nGarrett: I love you.'}, state)

    def test_named_transcript_and_scene_controls(self):
        state = c.fresh()
        c.town.travel(state, 'flowers'); c.town.finish_drive(state); c.town.meet(state, 'emily')
        state['routes']['emily']['history'].clear()
        c.commit(state, c.SCENE_DIRECTIONS[0], SCENE)
        c.commit(state, 'How are you?', SCENE)
        blocks = c.transcript(state, 'Would you like dinner?')
        self.assertEqual(blocks[0][0], 'Scene direction')
        self.assertEqual(blocks[1][0], 'Narrator')
        self.assertEqual(blocks[2][0], 'Emily Fields')
        self.assertEqual(blocks[3][0], 'Garrett Han (You)')
        self.assertIn('awaiting response', blocks[-1][0])
        self.assertEqual(c.player_message(state, c.SCENE_DIRECTIONS[0])['kind'], 'scene_direction')

    def test_player_voice_pass_keeps_scene_and_accepts_natural_questions(self):
        for player in c.playable_cast.ORIGINAL:
            state = c.fresh(player)
            state['active'] = 'emily'
            scene = {**SCENE, 'addressee': c.PLAYERS[player], 'choices_speaker': c.PLAYERS[player]}
            choices = ['Long day?', 'Dinner after work?', 'Show me what you made.', 'I can stay a little longer.']
            suggestions = dict(choices_speaker=c.PLAYERS[player], choices=choices, personal_choices=c.personal_choices(state, {}))
            with patch.object(c, 'request', return_value={'message': {'content': json.dumps(suggestions)}}) as req:
                result = c.generate_player_choices(state, 'Hello', scene)
                self.assertEqual(result['dialogue'], scene['dialogue'])
                self.assertEqual(result['narration'], scene['narration'])
                self.assertEqual(result['choices'], choices)
                prompt = req.call_args.args[1]['messages'][0]['content']
                styles = json.loads((c.ROOT / 'dialogue_styles.json').read_text(encoding='utf-8'))
                self.assertIn(styles[player + '_player'], prompt)
                self.assertNotIn(styles['emily'], prompt)

    def test_http_integration(self):
        captured = {}
        scene = dict(SCENE, input_tone='Friendly', emotions={'garrett': 'curious', 'emily': 'happy'}, bond_moments={'emily':'none'})
        scene['personal_choices'] = c.personal_choices(c.fresh(), {})
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_POST(self):
                captured.update(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                self.send_response(200); self.end_headers()
                self.wfile.write(json.dumps({'message': {'content': json.dumps(scene)}}).encode())
        server = HTTPServer(('127.0.0.1', 0), Handler)
        worker = threading.Thread(target=server.serve_forever, daemon=True); worker.start()
        try:
            with patch.object(c, 'ENDPOINT', f'http://127.0.0.1:{server.server_port}'):
                result=c.generate(c.fresh(), 'Hello')
                self.assertEqual(result['dialogue'], scene['dialogue'])
                self.assertEqual(result['choices'], [])
                self.assertTrue(result['suggestions_deferred'])
            self.assertEqual(captured['model'], c.MODEL)
            self.assertFalse(captured['stream'])
            self.assertNotIn('choices',captured['format']['properties'])
        finally: server.shutdown(); server.server_close(); worker.join()

if __name__ == '__main__': unittest.main()
