import copy
import json
import unittest
from unittest.mock import patch

import character_types as types
import game_core as core
import town
import groups
import dating
import meet_cute
import phone_apps
import town_npc_system


class CharacterTypeTests(unittest.TestCase):
    def test_all_existing_characters_have_exactly_one_type(self):
        self.assertEqual(set(core.CONTACTS), set(types.MAJOR_CHARACTERS))
        for who in ('neo', 'alyssa', 'rosa', 'sylvanis', *town.hidden.CAST):
            self.assertEqual(types.kind(who), types.MAJOR)
        locals_ = [p[0] for p in (*town.NPCS, *town.VENUE_STAFF.values(), town.HQ_EXECUTIVE)]
        for who in locals_:
            self.assertEqual(types.kind(who), types.TOWN)
            for player in core.PLAYERS:
                state = core.fresh(player)
                self.assertFalse(town.romanceable(state, who))
                self.assertFalse(meet_cute.eligible(state, who))
                self.assertNotIn(who, phone_apps.contacts(state))
            with self.assertRaises(ValueError): phone_apps.queue_grove(state, who)
            with self.assertRaises(ValueError): meet_cute.public_profile(state, who)

    def test_legacy_romance_is_archived_once_and_chat_retained(self):
        state = core.fresh('ivan')
        history = [{'speaker':'Theo','text':'We talked about books.'}]
        state['npc_chats'] = {'Theo':dict(history=copy.deepcopy(history), connection=dict(
            status='dating', attraction=90, trust=80, closeness=70, jealousy=25))}
        state['relationships']['Theo'] = dict(status='dating', attraction=90, trust=80, closeness=70)
        state['date_session'] = dict(partner='Theo', started=True)
        meet_cute.ensure(state)['matches']['Theo'] = dict(dates=[99])
        state.setdefault('scheduled_events', []).append(dict(id=99, cancelled=False))
        town.ensure(state)
        self.assertEqual(state['npc_chats']['Theo']['history'], history)
        self.assertNotIn('Theo', state['relationships'])
        self.assertNotIn('date_session', state)
        self.assertNotIn('attraction', state['npc_chats']['Theo']['connection'])
        self.assertIn('Theo', state['meet_cute']['legacy_town_matches'])
        self.assertTrue(state['scheduled_events'][-1]['cancelled'])
        before = copy.deepcopy(state)
        town.ensure(state)
        self.assertEqual(state, before)

    def test_simple_exchange_uses_small_schema_and_no_romance_progression(self):
        state = core.fresh('ivan')
        state['world']['npcs'] = ['Theo']
        data = dict(narration='Theo closes his book.', lines=[dict(speaker='Theo',text='What have you been reading?')],
                    emotions={'ivan':'curious','Theo':'happy'})
        with patch.object(core, 'request', return_value={'message':{'content':json.dumps(data)}}) as request:
            result = town.generate_npc(state, 'Theo', 'Any recommendations?')
        schema = request.call_args.args[1]['format']
        self.assertEqual(set(schema['properties']), {'narration','lines','emotions'})
        town.commit_npc(state, 'Theo', 'Any recommendations?', result)
        for day in (1, 2):
            state['world']['minute'] = day*1440+600
            town.commit_npc(state, 'Theo', 'Good morning.', result)
        self.assertEqual(state['npc_chats']['Theo']['connection']['status'], 'familiar face')
        self.assertNotIn('Theo', state['relationships'])
        self.assertNotIn('Theo', state.get('relationship_dynamics', {}).get('people', {}))
        town.social_event(state, 'Theo', 'returned_flirt')
        self.assertNotIn('Theo', state['relationships'])
        invalid = dict(result, kissed_contact='Theo')
        with self.assertRaises(ValueError): town.commit_npc(state,'Theo','A kiss?',invalid)

    def test_local_text_keeps_history_and_simple_identity(self):
        state = core.fresh()
        state['npc_chats'] = {'Maya': {'history':[]}}
        groups.sync_contacts(state)
        data = dict(narration='A message arrives.', lines=[dict(speaker='Maya',text='See you around.')],
            emotions={state['player']:'happy','Maya':'happy'}, choices=[], suggestions_deferred=True)
        groups.commit(state, 'npc:Maya', 'Thanks!', data)
        self.assertEqual(state['groups']['npc:Maya']['history'], state['npc_chats']['Maya']['history'])
        self.assertNotIn('Maya', state['relationships'])
        self.assertFalse(dating.begin(state,'Maya'))

    def test_old_grove_jobs_cannot_publish_as_town_npcs(self):
        state = core.fresh()
        data = phone_apps.ensure(state)
        data['grove_pending'].append(dict(id=999, author='Maya',parent=None))
        data['posts'].append(dict(id=999,author='Maya',text='Legacy post',minute=0,parent=None))
        self.assertNotIn('Maya', [p['author'] for p in phone_apps.grove_posts(state)])
        self.assertNotIn('Maya', [p['author'] for p in data['grove_pending']])


if __name__ == '__main__': unittest.main()
