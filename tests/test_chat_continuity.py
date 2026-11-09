import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import game_core as core
import groups
import messages_ui
import town


class ChatContinuityTests(unittest.TestCase):
    def test_solo_hangout_is_separate_and_concluded_history_survives(self):
        s = core.fresh('rei')
        town.summon(s, 'emily')
        gid = s['active_group']
        self.assertEqual(s['groups'][gid]['solo'], 'emily')
        result = dict(narration='Emily smiles.', dialogue='Good to see you.', memory='We met.',
                      choices=['Hello', 'Coffee?', 'Busy?', 'Thanks'])
        groups.commit(s, gid, 'Hello there.', result)
        self.assertTrue(any(m['text'] == 'Good to see you.' for m in s['groups'][gid]['history']))
        self.assertFalse(any(m[1] == 'Good to see you.' for m in messages_ui.text_messages(s)))
        town.end_hangouts(s)
        self.assertFalse(s['groups'][gid]['open'])
        self.assertEqual(s['last_hangout'], gid)
        self.assertIn('Hangout began', s['groups'][gid]['history'][0]['text'])
        self.assertIn('Hangout concluded', s['groups'][gid]['history'][-1]['text'])
        with self.assertRaises(ValueError):
            groups.commit(s, gid, 'Still there?', result)

    def test_character_tab_cannot_generate_an_in_person_transition(self):
        s = core.fresh('rei')
        s['_text_only'] = True
        with self.assertRaisesRegex(ValueError, 'texting only'):
            core.validate_response({'conversation_channel': 'in_person'}, s)
        self.assertIn('exclusively phone texts', core.build_messages(s, 'Meet me now.')[0]['content'])

    def test_local_hangout_actions_and_phone_memories(self):
        s = core.fresh('rei')
        s['world']['npcs'] = ['Maya']
        gid = groups.open_local(s, 'Maya')
        result = dict(narration='Maya waves back.', choices=['Hello', 'Coffee?', 'Busy?', 'Thanks'],
                      lines=[dict(speaker='Maya', text='Good to see you.')])
        groups.commit(s, gid, core.ACTION_PREFIX + 'I wave.', result)
        self.assertTrue(any(line.get('kind') == 'action' for line in s['groups'][gid]['history']))
        self.assertIn('Good to see you.', ' '.join(town.character_memory.recall(s, 'Maya')))

    def test_met_local_can_text_away_from_town_and_join_group(self):
        s = core.fresh('rei')
        s['world']['npcs'] = ['Maya']
        groups.open_local(s, 'Maya')
        s['world']['npcs'] = []
        groups.reconcile(s)
        self.assertIsNone(s['active_group'])
        gid = groups.create_text(s, 'Coffee plans', ['Maya', 'emily'])
        result = dict(narration='A notification.', choices=['Yes', 'No', 'When?', 'Where?'],
                      lines=[dict(speaker='Maya', text='After my shift.'),
                             dict(speaker='Emily Fields', text='See you there.')])
        groups.commit(s, gid, 'Coffee tomorrow?', result)
        self.assertTrue(s['groups']['npc:Maya']['direct'])
        self.assertIn('After my shift.', ' '.join(town.character_memory.recall(s, 'Maya')))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'story.json'
            core.save(s, path)
            loaded = core.load(path)
            self.assertIn('npc:Maya', loaded['groups'])
            self.assertIn('Maya', loaded['npc_chats'])

    def test_hangout_prompt_remembers_plans_per_participant(self):
        s = core.fresh('rei')
        gid = groups.create_text(s, 'Picnic plans', ['emily', 'sophie'])
        s['groups'][gid]['history'] = [dict(speaker='Emily Fields', text='Bring the picnic blanket.', minute=600)]
        s['routes']['emily']['history'] = [dict(role='assistant', channel='text', minute=590,
            content=json.dumps(dict(dialogue='The secret surprise is a cake.')))]
        with patch.object(groups, 'generate_exchange') as generate:
            groups.generate(s, gid, 'What did we plan?')
        # The shared exchange helper adds per-character memories for all channels.
        with patch.object(core, 'request', side_effect=RuntimeError('captured')) as request:
            with self.assertRaises(RuntimeError):
                groups.generate_exchange(['Emily Fields', 'Sophie Parker'], 'Hangout',
                    {'player_input': 'Remember our picnic?'}, state=s, members=['emily', 'sophie'])
        context = json.loads(request.call_args.args[1]['messages'][1]['content'])
        self.assertIn('picnic blanket', ' '.join(context['participant_memories']['sophie']))
        self.assertNotIn('secret surprise', ' '.join(context['participant_memories']['sophie']))
        self.assertIn('secret surprise', ' '.join(context['participant_memories']['emily']))

    def test_text_times_and_spoken_history_are_separate(self):
        s = core.fresh('rei')
        history = s['routes']['emily']['history']
        for minute, channel, text in [(1435, 'text', 'Tonight?'), (1445, 'text', 'Tomorrow!'),
                                      (1500, 'in_person', 'We made it.')]:
            history.extend([dict(role='user', content=text, minute=minute),
                dict(role='assistant', channel=channel, minute=minute,
                     content=json.dumps(dict(dialogue=text, narration='A greeting.')))])
        texts = messages_ui.text_messages(s)
        self.assertEqual([m[4] for m in texts], [1435, 1435, 1445, 1445])
        spoken = core.transcript(s, pane='dialogue')
        self.assertFalse(any('Tonight?' in block[1] for block in spoken))
        self.assertTrue(any('We made it.' in block[1] for block in spoken))

    def test_legacy_met_contact_unlocks_without_remeeting(self):
        s = core.fresh()
        s['discoveries']['lena'].update(met=True, contact=False)
        self.assertTrue(core.hidden.contact(s, 'lena'))
        self.assertIn('lena', s['groups'][groups.create_text(s, 'Friends', ['lena', 'emily'])]['members'])
