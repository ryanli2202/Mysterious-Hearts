import copy
import json
import unittest
from unittest.mock import patch

import dialogue_craft as craft
import game_core as core
import groups
import town_npc_system


class DialogueCraftTests(unittest.TestCase):
    def test_repetition_is_speaker_specific_bounded_and_ignores_texts(self):
        history = [dict(speaker='Amy', text='That makes sense. Rei, how are you?') for _ in range(3)]
        history += [dict(speaker='Rei', text='Okay.', channel='text') for _ in range(3)]
        before = copy.deepcopy(history)
        notes = craft.repetition_notes(history, ['Amy', 'Rei'])
        self.assertTrue(any('frequent questions' in n for n in notes))
        self.assertTrue(any('repeated reassurance' in n for n in notes))
        self.assertTrue(any('sentence openings' in n for n in notes))
        self.assertTrue(any('repeated names' in n for n in notes))
        self.assertFalse(any(n.startswith('Rei:') for n in notes))
        self.assertEqual(history, before)
        self.assertEqual(craft.repetition_notes(history + [{}] * 24, ['Amy']), [])

    def test_route_history_and_narration_patterns(self):
        history = [dict(role='assistant', channel='in_person', content=json.dumps(
            dict(speaker='Emily Fields', dialogue='Well, yes.', narration='Emily nods.'))) for _ in range(3)]
        notes = craft.repetition_notes(history, ['Emily Fields'])
        self.assertTrue(any('sentence openings' in n for n in notes))
        self.assertTrue(any('gesture' in n for n in notes))
        for entry in history: entry['channel'] = 'text'
        self.assertEqual(craft.repetition_notes(history, ['Emily Fields']), [])
        self.assertEqual(craft.repetition_notes([dict(role='assistant', content='broken')], ['Emily']), [])

    def test_spoken_group_accepts_silence_and_returning_speaker_but_text_does_not(self):
        names = ['Emily Fields', 'Sophie Parker']
        data = dict(narration='Sophie listens.', choices=[], suggestions_deferred=True,
                    lines=[dict(speaker=names[0], text='Just tea.')])
        groups.validate(data, names, flexible=True)
        with self.assertRaises(ValueError): groups.validate(data, names)
        data['lines'] += [dict(speaker=names[1], text='Again?'), dict(speaker=names[0], text='Yes. Again.')]
        groups.validate(data, names, flexible=True)
        self.assertEqual(craft.spoken_by(data['lines'])[names[0]], 'Just tea.\nYes. Again.')
        with self.assertRaises(ValueError): groups.validate(data, names)
        for lines in ([], [dict(speaker='Intruder', text='Hi.')], [dict(speaker=names[0], text='')], data['lines'] * 2):
            with self.subTest(lines=lines), self.assertRaises(ValueError):
                groups.validate(dict(data, lines=lines), names, flexible=True)

    def test_direct_guide_uses_existing_request_and_leaves_text_prompt_alone(self):
        state = core.fresh('rei')
        state['routes']['emily']['channel'] = 'in_person'
        with patch.object(core, 'request') as request:
            prompt = core.build_messages(state, 'Tea?')[0]['content']
        request.assert_not_called()
        self.assertIn(craft.INTENT, prompt)
        state['routes']['emily']['channel'] = 'text'
        self.assertNotIn(craft.INTENT, core.build_messages(state, 'Tea?')[0]['content'])

    def test_group_generation_and_commit_keep_all_returning_speaker_lines(self):
        state = core.fresh('rei')
        core.town.summon(state, 'emily')
        core.town.summon(state, 'sophie')
        gid = state['active_group']
        self.assertEqual(set(state['groups'][gid]['members']), {'emily', 'sophie'})
        data = dict(narration='Sophie listens.', choices=[], suggestions_deferred=True,
                    lines=[dict(speaker='Emily Fields', text='Tea sounds good.')],
                    emotions={'rei':'content', 'emily':'content', 'sophie':'content'},
                    input_tone='Other', bond_moments={'emily':'none', 'sophie':'none'},
                    social_target='none', social_event='none', kissed_contact='none')
        with patch.object(core, 'request', return_value={'message': {'content': json.dumps(data)}}) as request:
            generated = groups.generate(state, gid, 'Tea?')
        self.assertEqual(request.call_count, 1)
        body = request.call_args.args[1]
        self.assertEqual(body['format']['properties']['lines']['minItems'], 1)
        self.assertIn(craft.GROUP, body['messages'][0]['content'])
        before = copy.deepcopy(state['relationships']['sophie'])
        groups.commit(state, gid, 'Tea?', generated)
        self.assertEqual(state['relationships']['sophie'], before)
        generated['lines'] += [dict(speaker='Sophie Parker', text='No coffee?'), dict(speaker='Emily Fields', text='Not tonight.')]
        with patch.object(core.social_world, 'record_notes') as record:
            groups.commit(state, gid, 'Anything else?', generated)
        self.assertEqual(record.call_args.args[2]['emily'], 'Tea sounds good.\nNot tonight.')
        self.assertEqual([m['text'] for m in state['groups'][gid]['history'][-3:]],
                         ['Tea sounds good.', 'No coffee?', 'Not tonight.'])

    def test_local_group_silent_richter_does_not_create_disclosure(self):
        state = core.fresh('rei')
        names = ['Maya', core.town.RICHTER]
        data = dict(narration='Richter checks the time.', choices=[], suggestions_deferred=True,
                    lines=[dict(speaker='Maya', text='Hello.')],
                    emotions={'rei':'content', 'Maya':'content', core.town.RICHTER:'irritated'})
        with patch.object(core, 'request', return_value={'message': {'content': json.dumps(data)}}) as request:
            generated = town_npc_system.generate(state, names, {'player_reply':'Hello.'})
        self.assertEqual(request.call_count, 1)
        with patch.object(core.town, 'npc_details'), patch.object(core.town.loop, 'together', return_value=True):
            state['world']['party'] = ['emily']
            before = copy.deepcopy(state.get('shared_events', []))
            town_npc_system.commit(state, names, 'Hello.', generated)
        self.assertEqual(state.get('shared_events', []), before)
        with self.assertRaises(ValueError): town_npc_system.validate(state, names, generated, texting=True)

    def test_text_generation_preserves_full_participation_contract(self):
        state = core.fresh('rei')
        for local in (False, True):
            with self.subTest(local=local), patch.object(core, 'request', side_effect=RuntimeError('captured')) as request:
                with self.assertRaisesRegex(RuntimeError, 'captured'):
                    if local:
                        town_npc_system.generate(state, ['Maya', core.town.RICHTER], {}, texting=True)
                    else:
                        groups.generate_exchange(['Emily Fields', 'Sophie Parker'], 'Phone group', {},
                                                 state=state, members=['emily', 'sophie'], texting=True)
            body = request.call_args.args[1]
            self.assertEqual(body['format']['properties']['lines']['minItems'], 2)
            self.assertEqual(body['format']['properties']['lines']['maxItems'], 2)
            self.assertNotIn(craft.INTENT, body['messages'][0]['content'])
            self.assertNotIn(craft.GROUP, body['messages'][0]['content'])


if __name__ == '__main__': unittest.main()
