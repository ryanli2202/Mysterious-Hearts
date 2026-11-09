from date_fixtures import next_morning
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as c
import town
import groups
import world_loop as w

SCENE={'narration':'A phone lights up.','dialogue':'hi there','memory':'A brief greeting.', 'choices':['Hi!','How are you?','Busy?','Talk later?']}

class ActivityTests(unittest.TestCase):
    def arrive(self,s,where):
        town.travel(s,where); town.finish_drive(s)
    def party(self):
        s=c.fresh(); self.arrive(s,'flowers'); town.meet(s,'emily')
        town.travel(s,'track','emily'); town.finish_drive(s)
        groups.form(s, ['emily', 'sophie'])
        return s

    def test_elapsed_ticks_roll_the_calendar_automatically(self):
        s=c.fresh(); start=s['world']['minute']
        for _ in range(5): c.commit(s,'Hi',SCENE)
        self.assertEqual(s['world']['minute'],start)
        c.commit(s,'Hi',SCENE); self.assertEqual(s['world']['minute'],start)
        c.commit(s,'[Action] I water the plants.',SCENE)
        self.assertEqual(s['world']['minute'],start)
        before=s['world']['minute']; w.advance(s,2000); self.assertEqual(s['world']['minute'],before+2000)
        w.advance(s,60); self.assertEqual(s['world']['minute'],before+2060)
        expected=(s['world']['minute']//1440+1)*1440+480
        next_morning(s); self.assertEqual(s['world']['minute'],expected)

    def test_idle_followup_does_not_change_day_or_schedules(self):
        s=c.fresh(); c.commit(s,c.INCOMING_TEXT,SCENE)
        start=s['world']['minute']; cast=copy.deepcopy(s['world']['cast'])
        for _ in range(6): w.idle_messages(s)
        self.assertEqual(s['world']['minute'],start)
        self.assertEqual(s['world']['cast'],cast)
        self.assertFalse(s['routes']['emily']['followup_sent'])
        self.assertNotIn('Narrator',[b[0] for b in c.transcript(s)])

    def test_night_venue_and_career_windows(self):
        for player in c.PLAYERS:
            from date_fixtures import afternoon_state
            s=afternoon_state(player)
            with self.assertRaises(ValueError): town.travel(s,'iron_circle')
            if not town.CAREERS[player]: continue
            day_place=town.CAREERS[player][0][0]
            self.arrive(s,day_place); money=s['world']['money']
            town.career_work(s,0)
            self.assertEqual(s['world']['money'],money+town.CAREERS[player][0][2])
            before=copy.deepcopy(s)
            with self.assertRaises(ValueError): town.career_work(s,0)
            self.assertEqual(s,before)
            night_place=town.CAREERS[player][1][0]
            w.advance(s,20*60-s['world']['minute'])
            self.arrive(s,night_place); money=s['world']['money']
            town.career_work(s,1)
            # Iron Circle preparation is unpaid; prize money requires a completed bout.
            self.assertEqual(s['world']['money'],money+(0 if player=='rei' else town.CAREERS[player][1][2]))
            self.assertEqual(w.appointment(player,2*1440+20*60)[1],night_place)

    def test_home_actions_require_own_home(self):
        s=c.fresh('rei')
        with self.assertRaises(ValueError): town.home_action(s,'Paint')
        self.arrive(s,'rei_home'); minute=s['world']['minute']
        town.home_action(s,town.HOME_ACTIONS['rei'][0])
        self.assertEqual(s['world']['minute'],minute)
        self.assertIn('Paint',s['world']['home_journal'][-1])
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json'; c.save(s,path)
            self.assertEqual(c.load(path),s)

    def test_selected_group_travels_without_adding_nearby_contacts(self):
        s=self.party(); gid=s['active_group']
        self.assertEqual(set(s['groups'][gid]['members']),{'emily','sophie'})
        self.assertEqual(s['groups'][gid]['location'],'track')
        self.assertFalse(any('Group conversation' in m['content'] for m in s['routes']['emily']['history']))
        town.travel(s,'cafe')
        self.assertEqual(s['world']['cast']['emily']['location'],'cafe')
        self.assertEqual(s['world']['cast']['sophie']['location'],'cafe')
        self.assertEqual(s['groups'][s['active_group']]['location'],'cafe')
        self.assertEqual(next(j for j in reversed(s['world']['journeys']) if j['driver']=='garrett')['vehicle'],town.loop.GROUP_VAN)
        town.finish_drive(s)
        self.assertNotIn('amy',s['groups'][s['active_group']]['members'])
        self.assertEqual(s['active_group'],gid)
        self.assertTrue(s['groups'][gid]['open'])

    def test_one_on_one_stays_private_near_other_contacts(self):
        s=c.fresh(); self.arrive(s,'flowers'); town.meet(s,'emily')
        town.travel(s,'track','emily'); town.finish_drive(s)
        self.assertTrue(w.together(s, 'sophie'))
        groups.reconcile(s)
        self.assertEqual(s['groups'][s['active_group']]['members'], ['emily'])
        self.assertEqual(s['world']['party'], ['emily'])

    def test_reselecting_companions_removes_others_and_end_stays_ended(self):
        s=self.party()
        groups.form(s, ['emily'])
        groups.reconcile(s)
        self.assertEqual(s['groups'][s['active_group']]['members'], ['emily'])
        self.assertEqual(s['routes']['sophie']['channel'], 'text')
        self.assertEqual(s['world']['party'], ['emily'])
        town.end_hangouts(s)
        groups.reconcile(s)
        self.assertIsNone(s['active_group'])
        self.assertEqual(s['world']['party'], [])

    def test_group_reply_speakers_and_save_roundtrip(self):
        s=self.party(); gid=s['active_group']
        data={'narration':'The three settle beside the track.', 'lines':[{'speaker':'Emily Fields','text':'It is nice out here.'},{'speaker':'Sophie Parker','text':'Want to watch practice?'}], 'choices':['We can stay.','How was practice?','Nice afternoon.','Want a break?']}
        data['action_choices'] = ['I wave to the runners.', 'I give Sophie my full attention.',
                                  'I mime a false start.', 'I blow Emily a kiss.']
        data['emotions'] = {'garrett': 'curious', 'emily': 'content', 'sophie': 'playful'}
        data['input_tone'] = 'Friendly'
        data['bond_moments'] = {'emily': 'none', 'sophie': 'none'}
        data['personal_choices'] = c.personal_choices(s, {})
        private=copy.deepcopy(s['routes'])
        with patch.object(c,'request',return_value={'message':{'content':json.dumps(data)}}) as request:
            result=groups.generate(s,gid,'Hey, everyone.')
            self.assertEqual(result['lines'],data['lines'])
            self.assertEqual(result['choices'],[])
        self.assertIn('Emily Fields',request.call_args.args[1]['messages'][0]['content'])
        self.assertNotIn('action_choices', request.call_args.args[1]['format']['required'])
        self.assertIn(c.ACTION_GUIDE, request.call_args.args[1]['messages'][0]['content'])
        groups.commit(s,gid,'Hey, everyone.',data)
        self.assertEqual(s['emotions'], data['emotions'])
        self.assertEqual(c.action_choices(s, s['groups'][gid]), data['action_choices'])
        self.assertEqual(s['routes'],private)
        self.assertEqual(s['groups'][gid]['history'][-1]['speaker'],'Sophie Parker')
        before=copy.deepcopy(s)
        invalid=copy.deepcopy(data); invalid['lines'][0]['speaker']='Garrett Han'
        with self.assertRaises(ValueError): groups.commit(s,gid,'Hello',invalid)
        self.assertEqual(s,before)
        with self.assertRaises(ValueError):
            groups.commit(s, gid, 'Hello', dict(data, action_choices=['wave'] * 4))
        self.assertEqual(s, before)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json'; c.save(s,path); self.assertEqual(c.load(path),s)

    def test_group_stays_across_appointment_until_disband(self):
        s=self.party()
        s['world']['minute'] += 2*1440  # Monday's work schedule
        w.advance(s,17*60-s['world']['minute']%1440)
        self.assertTrue(s['groups'][s['active_group']]['open'])
        self.assertTrue({'emily', 'sophie'}.issubset(s['world']['party']))
        self.assertEqual(s['world']['cast']['emily']['activity'], 'Hanging out')
        groups.disband(s); self.assertIsNone(s['active_group']); self.assertEqual(s['world']['party'],[])
        w.advance(s, 1)
        self.assertEqual(s['world']['cast']['emily']['location'], 'cafe')
        with self.assertRaises(ValueError): groups.form(s,['amy'])

    def test_named_text_groups_persist_independently(self):
        s = c.fresh()
        members = ['emily', 'sophie']
        gid = groups.create_text(s, 'Track friends', members)
        other = groups.create_text(s, 'Weekend plans', members)
        data = dict(narration='New messages.', choices=SCENE['choices'],
                    lines=[dict(speaker=c.CONTACTS[m][0], text='Hi!') for m in members])
        groups.commit(s, gid, 'Hey everyone!', data)
        next_morning(s)
        self.assertIsNone(s['active_group'])
        self.assertFalse(s['world']['party'])
        self.assertFalse(s['groups'][other]['history'])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'story.json'
            c.save(s, path)
            saved = c.load(path)['groups'][gid]
        self.assertEqual(saved['name'], 'Track friends')
        self.assertEqual(saved['history'][0]['text'], 'Hey everyone!')

    def test_group_text_prompt_uses_each_senders_private_text_style(self):
        s = c.fresh('rei')
        members = ['emily', 'april']
        gid = groups.create_text(s, 'Weekend plans', members)
        data = dict(narration='New messages.', choices=SCENE['choices'],
                    lines=[dict(speaker='Emily Fields', text='i can bring flowers (｡･ω･｡)'),
                           dict(speaker='April Xu', text='I’ll bring the board.')])
        data['emotions'] = {'rei': 'content', 'emily': 'happy', 'april': 'focused'}
        data['input_tone'] = 'Other'
        data['bond_moments'] = {'emily': 'none', 'april': 'none'}
        data['personal_choices'] = c.personal_choices(s, {})
        with patch.object(c, 'request', return_value={'message': {'content': json.dumps(data)}}) as request:
            result=groups.generate(s, gid, 'saturday?')
            self.assertEqual(result['lines'],data['lines'])
            self.assertEqual(result['choices'],[])
        prompt = request.call_args.args[1]['messages'][0]['content']
        for who in [*members, s['player']]:
            self.assertIn(c.TEXT_STYLES[who], prompt)
        self.assertNotIn('No texting emojis', prompt)
        self.assertNotIn('action_choices', request.call_args.args[1]['format']['properties'])
        self.assertEqual(c.action_choices(s, s['groups'][gid]), [])

    def test_group_fourth_action_respects_sibling_and_hostile_contacts(self):
        for player, sibling in [('rei', 'yuriko'), ('ivan', 'valentina')]:
            state = c.fresh(player)
            group = {'members': [sibling, 'sylvanis']}
            self.assertEqual(c.choice_tones(state, group), c.SIBLING_TONES)
            self.assertIn(sibling.title(), c.action_choices(state, group)[3])
            group['members'].append('amy')
            self.assertEqual(c.choice_tones(state, group), c.REPLY_TONES)
            self.assertIn('Amy', c.action_choices(state, group)[3])

    def test_summoning_brings_contacts_into_a_persistent_hangout(self):
        s = c.fresh('rei')
        wld = s['world']
        start = wld['minute']
        town.summon(s, 'emily')
        self.assertEqual(wld['minute'], start)
        trip=next(j for j in reversed(wld['journeys']) if j['driver']=='emily')
        self.assertEqual(trip['status'], 'arrived')
        self.assertEqual(wld['location'], 'square')
        self.assertEqual(s['routes']['emily']['channel'], 'in_person')
        town.summon(s, 'sophie')
        w.advance(s, 17*60 - wld['minute'])
        self.assertTrue({'emily', 'sophie'}.issubset(s['groups'][s['active_group']]['members']))
        self.assertTrue(w.together(s, 'emily'))
        self.assertTrue(w.together(s, 'sophie'))

    def test_summon_requires_contact_and_stationary_player(self):
        s = c.fresh('rei')
        for who in ('rei', next(iter(town.hidden.CAST))):
            with self.assertRaises(ValueError):
                town.summon(s, who)
        town.travel(s, 'track')
        before = s['world']['minute']
        town.summon(s, 'emily')
        self.assertTrue(w.together(s,'emily'))
        self.assertEqual(s['world']['minute'],before)

    def test_emily_can_accept_early_hangout_by_text(self):
        s = c.fresh('rei')
        c.commit(s, 'Can you leave work early? I can pick you up.',
                 dict(SCENE, dialogue='Yes, pick me up at the shop.', hangout_decision='accepted'))
        w.advance(s, 17*60 - s['world']['minute'])
        self.assertEqual(s['world']['cast']['emily']['location'], 'flowers')
        self.arrive(s, 'flowers')
        town.meet(s, 'emily')
        self.assertIn('emily', s['world']['party'])
        self.arrive(s, 'track')
        self.assertTrue(w.together(s, 'emily'))

    def test_end_day_clears_group_and_night_drive_cannot_get_stuck(self):
        s=self.party(); gid=s['active_group']; next_morning(s)
        self.assertIsNone(s['active_group']); self.assertFalse(s['groups'][gid]['open'])
        s['world']['minute']=2*1440-5
        town.travel(s,'cafe'); town.finish_drive(s)
        self.assertEqual(s['world']['minute'],2*1440-5)
        self.assertEqual(s['world']['location'],'cafe')

if __name__=='__main__': unittest.main()
