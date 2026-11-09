from date_fixtures import next_morning
import json
import unittest
from unittest.mock import patch

import game_core as core
import groups
import town


REPLIES = ['Want company?', 'I meant what I said.', 'That pot had one job.', 'Keep smiling at me like that.']
GESTURES = ['I wave.', 'I put my phone away.', 'I bow to the watering can.', 'I wink at Emily.']


def opening(channel='text'):
    state = core.fresh('rei')
    if channel == 'in_person':
        town.summon(state, 'emily')
    state['routes']['emily'].update(choices=REPLIES, ordered_tones=True,
                                    action_choices=GESTURES, ordered_action_tones=True)
    return state


def scene(feeling='content', **extra):
    return dict(speaker='Emily Fields', addressee='Rei Takamura', choices_speaker='Rei Takamura',
                narration='Emily puts down her phone.', dialogue='wait, what was i saying again?',
                choices=REPLIES, memory='They talked about the flower shop.',
                emotions={'rei': 'content', 'emily': feeling}, bond_moments={'emily':'none'}, **extra)


def response(data):
    return {'message': {'content': json.dumps(dict(data, personal_choices=core.personal_choices({'player':'rei'}, {})))}}


class ReactionTests(unittest.TestCase):
    def test_four_tones_reach_scene_and_affect_the_recipient_for_text_speech_and_gestures(self):
        for channel, choices in [('text', REPLIES), ('in_person', REPLIES), ('in_person', GESTURES)]:
            for i, expected in enumerate(('happy', 'grateful', 'playful', 'flustered')):
                with self.subTest(channel=channel, choice=choices[i]):
                    state = opening(channel)
                    action = (core.ACTION_PREFIX if choices is GESTURES else '') + choices[i]
                    messages = core.build_messages(state, action)
                    self.assertEqual(json.loads(messages[-1]['content'])['submitted_tone'], core.REPLY_TONES[i])
                    self.assertIn('message they type' if channel == 'text' else 'observable gesture', messages[0]['content'])
                    core.commit(state, action, scene())
                    self.assertEqual(state['emotions']['emily'], expected)

    def test_generation_repairs_flat_emily_scene_before_committing_reply(self):
        state = opening()
        action = REPLIES[3]
        with patch.object(core, 'request', side_effect=[response(scene()), response(scene('flustered')),
                          response({'choices_speaker':'Rei Takamura', 'choices':REPLIES})]) as request:
            result = core.generate(state, action)
        schema = request.call_args_list[0].args[1]['format']['properties']['emotions']
        self.assertEqual(schema['properties']['emily']['enum'], ['flustered'])
        self.assertFalse(state['emotions'])
        core.commit(state, action, result)
        self.assertEqual(state['emotions'], {'rei':'flirty', 'emily':'flustered'})
        self.assertIn(result['dialogue'], str(core.transcript(state)))

    def test_context_can_change_how_the_same_move_lands(self):
        state = opening()
        state['relationships']['emily']['status'] = 'strained'
        core.commit(state, REPLIES[3], scene())
        self.assertEqual(state['emotions']['emily'], 'guarded')
        core.commit(state, REPLIES[1], scene('disappointed'))
        self.assertEqual(state['emotions']['emily'], 'disappointed')
        # An anxious friend can feel relief at the same joke that usually makes her playful.
        state = opening()
        state['emotions']['emily'] = 'anxious'
        self.assertEqual(core.emotions.likely_reaction(state, 'emily', 'Funny'), 'relieved')
        core.commit(state, REPLIES[2], scene('relieved'))
        self.assertEqual(state['emotions']['emily'], 'relieved')

    def test_custom_flirt_and_unordered_legacy_choice(self):
        state = opening()
        state['routes']['emily']['ordered_tones'] = False
        move = json.loads(core.build_messages(state, REPLIES[3])[-1]['content'])
        self.assertNotIn('submitted_tone', move)
        core.commit(state, 'There’s that smile I came for.', scene('flustered', social_event='flirt'))
        self.assertEqual(state['emotions']['emily'], 'flustered')
        next_morning(state)
        self.assertEqual(state['emotions']['emily'], 'content')

    def test_freeform_actions_take_their_tone_from_the_conversation(self):
        state = opening('in_person')
        action = core.ACTION_PREFIX + 'I give the watering can a solemn little salute.'
        with patch.object(core, 'request', side_effect=[response(scene(input_tone='Funny')),
                          response({'choices_speaker':'Rei Takamura', 'choices':REPLIES, 'action_choices':GESTURES})]) as request:
            result = core.generate(state, action)
        self.assertIn('input_tone', request.call_args_list[0].args[1]['format']['required'])
        core.commit(state, action, result)
        self.assertEqual(state['emotions'], {'rei':'playful', 'emily':'playful'})

    def test_group_flirt_only_applies_to_the_recipient(self):
        for recipient, emily in [('sophie', 'curious'), ('emily', 'flustered')]:
            with self.subTest(recipient=recipient):
                state = opening()
                gid = groups.create_text(state, 'After practice', ['emily', 'sophie'])
                choices = [*REPLIES[:3], f'{recipient.title()}, keep smiling at me like that.']
                state['groups'][gid].update(choices=choices, ordered_tones=True)
                data = dict(narration='Two messages arrive.', choices=choices,
                            lines=[{'speaker':'Sophie Parker', 'text':'hey!'}, {'speaker':'Emily Fields', 'text':'oh…'}],
                            social_target=recipient, social_event='flirt', bond_moments={'emily':'none', 'sophie':'none'},
                            emotions={'rei':'flirty', 'emily':emily, 'sophie':'playful'})
                with patch.object(core, 'request', return_value=response(data)) as request:
                    result = groups.generate(state, gid, choices[3])
                context = json.loads(request.call_args.args[1]['messages'][-1]['content'])
                self.assertEqual(context['submitted_tone'], 'Flirtatious')
                groups.commit(state, gid, choices[3], result)
                self.assertEqual(state['emotions']['emily'], emily)

    def test_town_npc_preserves_generated_moods_without_major_character_tone_effects(self):
        state = opening()
        state['world']['npcs'] = ['Maya']
        state['npc_chats'] = {'Maya': {'history': [], 'choices': REPLIES, 'ordered_tones': True}}
        data = dict(narration='Maya looks up.',
                    lines=[{'speaker':'Maya', 'text':'Okay, that got me.'}],
                    emotions={'Maya':'amused', 'rei':'content'})
        with patch.object(core, 'request', return_value={'message': {'content': json.dumps(data)}}) as request:
            result = town.generate_npc(state, 'Maya', REPLIES[2])
        payload = request.call_args.args[1]
        context = json.loads(payload['messages'][-1]['content'])
        self.assertEqual(context['player_reply'], REPLIES[2])
        self.assertNotIn('submitted_tone', context)
        self.assertEqual(set(payload['format']['properties']), {'narration', 'lines', 'emotions'})
        self.assertEqual(result['choices'], [])
        self.assertTrue(result['suggestions_deferred'])
        town.commit_npc(state, 'Maya', REPLIES[2], result)
        self.assertEqual(core.feeling_labels(state, ['Maya']), [('Rei Takamura (You)', 'content'), ('Maya', 'amused')])
        self.assertEqual(state['npc_chats']['Maya']['connection']['status'], 'acquaintances')
        self.assertNotIn('Maya', state['relationships'])
        self.assertNotIn('Maya', state.get('relationship_dynamics', {}).get('people', {}))
