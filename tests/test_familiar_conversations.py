import json
import copy
import unittest
from unittest.mock import patch

import game_core as core
import social_world as social
import contact_profiles as profiles
import memory_store
import suggestions
import messaging
import groups


class FamiliarConversationTests(unittest.TestCase):
    def test_both_speakers_remember_favourites_and_shared_history(self):
        s = core.fresh('rei')
        for speaker, listener, title in [('rei', 'emily', 'Kiki’s Delivery Service'),
                                         ('emily', 'rei', 'In the Mood for Love')]:
            known = social.conversation_knowledge(s, speaker, [listener])[listener]
            self.assertEqual(known['known_favourites']['Movie']['value'], title)
            self.assertTrue(any('greenhouse' in line.lower() for line in known['shared_history']))
        s['relationships']['emily'].update(trust=0, closeness=0)
        self.assertIn('Movie', social.conversation_knowledge(s, 'rei', ['emily'])['emily']['known_favourites'])

    def test_direct_text_and_in_person_prompts_include_continuity(self):
        s = core.fresh('rei')
        for channel in ('text', 'in_person'):
            s['routes']['emily']['channel'] = channel
            prompt = core.build_messages(s, 'What shall we watch?')[0]['content']
            self.assertIn('ESTABLISHED FAMILIARITY', prompt)
            self.assertIn('In the Mood for Love', prompt)
            self.assertIn('greenhouse', prompt)

    def test_strangers_do_not_inherit_favourites(self):
        s = core.fresh('minsu')
        self.assertEqual(social.conversation_knowledge(s, 'minsu', ['emily'])['emily']['known_favourites'], {})

    def test_delivered_change_overrides_old_preference_only_for_witnesses(self):
        s = core.fresh('rei')
        memory_store.utterance(s, 'new-movie', 'My favorite movie is Arrival.', 'emily', ['emily', 'rei'], 500)
        known = social.conversation_knowledge(s, 'rei', ['emily'])['emily']['known_favourites']
        self.assertEqual(known['Movie']['value'], 'Arrival')
        self.assertEqual(social.conversation_knowledge(s, 'sophie', ['emily'])['emily']['known_favourites']['Movie']['value'], 'Kiki’s Delivery Service')
        memory_store.utterance(s, 'rei-movie', 'My favorite movie is Paddington 2.', 'rei', ['emily', 'rei'], 510)
        self.assertEqual(profiles.view(s, 'emily', 'rei')['favourites']['Movie']['value'], 'Arrival')

    def test_group_history_excludes_private_pair_reference(self):
        s = core.fresh('rei')
        with patch.dict(core.lore.character_tables()['emily'], {'With Rei': 'PRIVATE_PAIR_SENTINEL', 'In company with Rei': 'PUBLIC_MEMORY_SENTINEL'}):
            known = social.conversation_knowledge(s, 'emily', ['rei', 'amy'])
            self.assertIn('PUBLIC_MEMORY_SENTINEL', json.dumps(known))
            self.assertNotIn('PRIVATE_PAIR_SENTINEL', json.dumps(known))

    def test_manual_suggestions_receive_player_knowledge(self):
        s = core.fresh('rei'); s['routes']['emily']['dialogue'] = 'A movie sounds nice.'
        result = {'choices_speaker': core.PLAYERS['rei'], 'choices': ['Your usual film tonight?', 'Want to try something new?', 'Tea first?', 'Shall we make dinner?']}
        with patch.object(core, 'request', return_value={'message': {'content': json.dumps(result)}}) as request:
            suggestions.generate(s, ('route', 'emily'))
        messages = request.call_args.args[1]['messages']
        self.assertIn('ESTABLISHED FAMILIARITY', messages[0]['content'])
        knowledge = json.loads(messages[1]['content'])['player_established_familiarity']['emily']
        self.assertEqual(knowledge['known_favourites']['Movie']['value'], 'Kiki’s Delivery Service')

    def test_queued_group_text_receives_speakers_own_knowledge(self):
        s = core.fresh('rei')
        s['groups']['familiar-test'] = dict(channel='text', name='Friends', members=['emily', 'sophie'], history=[])
        job = dict(who='emily', group=True, key='familiar-test', text='Movie tonight?', ids=[], reason=None)
        with patch.object(core, 'request', side_effect=RuntimeError('capture only')) as request:
            with self.assertRaisesRegex(RuntimeError, 'capture only'): messaging.generate(s, job)
        prompt = request.call_args.args[1]['messages'][0]['content']
        self.assertIn('ESTABLISHED FAMILIARITY', prompt)
        self.assertIn('In the Mood for Love', prompt)
        self.assertIn('Bend It Like Beckham', prompt)

    def test_local_listener_without_contact_profile_is_supported(self):
        s = core.fresh('rei')
        self.assertEqual(social.conversation_knowledge(s, 'rei', ['Maya'])['Maya']['known_favourites'], {})

    def test_prompt_knowledge_does_not_mutate_saved_state(self):
        s = core.fresh('rei'); before = copy.deepcopy(s)
        social.conversation_knowledge(s, 'rei', ['emily', 'sophie'])
        self.assertEqual(s, before)


if __name__ == '__main__': unittest.main()
