import copy
import json
import unittest
from unittest.mock import patch
import game_core as core
import autonomy as a
import messaging as m
import world_loop as w
import town
import memory_store


class AutonomyTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('rei'); a.ensure(self.s)

    def home(self,who):
        self.s['world']['cast'][who].update(location=w.HOUSES[who][0],journey=None,activity='Quiet evening')
        if who==self.s['player']: self.s['world']['location']=w.HOUSES[who][0]

    def test_sleep_crosses_midnight_and_restores_energy(self):
        self.home('rei'); self.s['world']['minute']=23*60+30
        a.person(self.s,'rei')['energy']=10
        a.advance_player(self.s,'sleep')
        self.assertEqual(self.s['world']['minute'],1410)
        self.assertEqual(a.status(self.s,'rei'),'Asleep')
        w.advance(self.s,480)
        self.assertEqual(self.s['world']['minute'],1890)
        self.assertGreater(a.person(self.s,'rei')['energy'],90)
        self.assertNotEqual(a.status(self.s,'rei'),'Asleep')

    def test_wait_does_not_restore_sleep(self):
        self.home('rei'); before=a.person(self.s,'rei')['energy']
        w.advance(self.s,10)
        self.assertLess(a.person(self.s,'rei')['energy'],before)

    def test_sleeping_contact_reads_after_waking(self):
        self.s['world']['minute']=23*60; self.home('emily')
        a.control(self.s,'emily')
        m.send(self.s,'emily','Are you free tomorrow?')
        for _ in range(12): self.s['world']['minute']+=1; m.tick(self.s)
        self.assertEqual(m.thread(self.s,'emily')['pending'][0]['read_by'],[])
        self.assertIsNone(m.next_job(self.s))
        self.s['world']['minute']=1440+7*60
        a.control(self.s,'emily')
        for _ in range(15): self.s['world']['minute']+=1; m.tick(self.s)
        self.assertIn('emily',m.thread(self.s,'emily')['pending'][0]['read_by'])
        self.assertEqual(m.next_job(self.s)['who'],'emily')

    def test_unread_text_is_not_owned_memory(self):
        self.home('emily'); self.s['world']['minute']=23*60; a.control(self.s,'emily')
        m.send(self.s,'emily','I promise to bring an emerald kite.')
        memory_store.sync(self.s)
        records=memory_store.ensure(self.s)['records'].values()
        self.assertFalse(any('emerald kite' in r['text'] and 'emily' in r['owners'] for r in records))

    def test_multiple_chats_bursts_and_new_message_during_generation(self):
        self.home('emily'); self.home('sophie')
        m.send(self.s,'emily','Hello'); m.send(self.s,'emily','One more thing')
        m.send(self.s,'sophie','How was training?')
        self.s['world']['minute']+=20; m.tick(self.s)
        for _ in range(15): self.s['world']['minute']+=1; m.tick(self.s)
        job=m.next_job(self.s)
        self.assertEqual(len(job['ids']),2)
        m.send(self.s,'emily','And a later thought')
        self.s['active']='sophie'
        result=dict(bubbles=['hello!','what’s up?'],moment='none',pause_minutes=0)
        self.assertTrue(m.apply(self.s,job,result))
        self.assertEqual(self.s['active'],'sophie')
        self.assertEqual(len(m.thread(self.s,'emily')['pending']),1)
        self.assertEqual(len(m.thread(self.s,'sophie')['pending']),1)
        self.assertEqual(self.s['routes']['emily']['unread'],2)
        self.assertFalse(m.apply(self.s,job,result))

    def test_new_acquaintance_requires_sustained_public_presence(self):
        for who in ('emily','valentina'):
            self.s['world']['cast'][who].update(location='cafe',journey=None,activity='Free time')
            a.person(self.s,who)['next_decision']=999999
        for i in range(4): self.s['world']['minute']+=5; a.tick(self.s)
        self.assertIn('valentina',a.person(self.s,'emily')['relationships'])
        self.assertIn('emily',a.person(self.s,'valentina')['relationships'])
        self.assertTrue(any(set(e['owners'])=={'emily','valentina'} for e in a.ensure(self.s)['events']))
        self.assertFalse(any(self.s['player'] in e['owners'] for e in a.ensure(self.s)['events']))

    def test_overnight_requires_acceptance_and_is_separate_sleep(self):
        self.home('rei'); self.s['world']['minute']=22*60
        self.s['world']['cast']['emily'].update(location=w.HOUSES['rei'][0],journey=None,activity='Hanging out')
        offer=a.request(self.s,'emily','overnight','A separate sleeping place')
        self.assertIsNone(a.person(self.s,'emily')['plan'])
        a.respond(self.s,offer['id'],'accept'); a.control(self.s,'emily')
        self.assertEqual(a.status(self.s,'emily'),'Asleep')
        self.assertEqual(self.s['world']['cast']['emily']['location'],w.HOUSES['rei'][0])
        self.assertIn('not consent',a.ensure(self.s)['events'][-1]['text'])

    def test_late_party_member_leaves_without_permission(self):
        self.s['world']['minute']=23*60+15
        self.s['world']['party']=['emily']
        self.s['world']['cast']['emily'].update(location=self.s['world']['location'],journey=None,activity='Hanging out')
        a.control(self.s,'emily')
        self.assertNotIn('emily',self.s['world']['party'])
        self.assertEqual(self.s['world']['cast']['emily']['location'],'emily_home')

    def test_queue_and_plans_survive_json_roundtrip(self):
        m.send(self.s,'emily','Hello')
        restored=json.loads(json.dumps(self.s)); a.ensure(restored)
        self.assertEqual(m.thread(restored,'emily'),m.thread(self.s,'emily'))

    def test_generation_has_no_canned_delay_reply_and_accepts_bursts(self):
        self.home('emily'); m.send(self.s,'emily','Hello')
        job=dict(key='emily',group=False,who='emily',ids=[1],text='Hello',reason=None,revision=1)
        answer=dict(bubbles=['hi','how did your painting go?'],moment='none',pause_minutes=0)
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(answer)}}) as request:
            self.assertEqual(m.generate(copy.deepcopy(self.s),job),answer)
        prompt=request.call_args.args[1]['messages'][0]['content']
        self.assertIn('Do not automatically apologise',prompt)
        self.assertNotIn('Are you still looking for somewhere to eat?',prompt)

    def test_group_reads_independently_without_leaking_to_sleeping_member(self):
        import groups
        gid=groups.create_text(self.s,'Friends',['emily','sophie'])
        self.home('emily'); self.home('sophie')
        self.s['world']['cast']['sophie']['activity']='Sleep'
        m.send(self.s,gid,'I promise to bring a purple kite',True)
        for _ in range(20): self.s['world']['minute']+=1; m.tick(self.s)
        memory_store.sync(self.s)
        records=[r for r in memory_store.ensure(self.s)['records'].values() if 'purple kite' in r['text']]
        self.assertTrue(any('emily' in r['owners'] for r in records))
        self.assertFalse(any('sophie' in r['owners'] for r in records))
        job=m.next_job(self.s); self.assertEqual(job['who'],'emily')
        m.apply(self.s,job,dict(bubbles=['great'],moment='none',pause_minutes=0))
        self.assertEqual(len(m.thread(self.s,gid,True)['pending']),1)

    def test_invitation_does_not_enter_home_until_welcomed(self):
        self.home('rei'); self.s['world']['cast']['emily'].update(location=w.HOUSES['rei'][0],journey=None,activity='Arrived')
        a.person(self.s,'emily')['plan']=dict(kind='visit',venue=w.HOUSES['rei'][0],until=1000,target='rei',accepted=False)
        self.assertFalse(w.together(self.s,'emily'))
        a.control(self.s,'emily')
        self.assertNotEqual(self.s['routes']['emily']['channel'],'in_person')

    def test_overnight_departure_returns_to_schedule_instantly(self):
        self.home('rei'); self.s['world']['minute']=9*60
        self.s['world']['cast']['emily'].update(location=w.HOUSES['rei'][0],journey=None,activity='Breakfast')
        a.person(self.s,'emily')['plan']=dict(kind='overnight',venue=w.HOUSES['rei'][0],until=9*60,target='rei')
        a.control(self.s,'emily')
        self.assertIsNone(self.s['world']['cast']['emily']['journey'])
        self.assertEqual(self.s['world']['cast']['emily']['location'],w.appointment('emily',self.s['world']['minute'])[1])

    def test_project_progress_requires_work_not_clock_jump(self):
        import living_world
        first=living_world.project(self.s,'emily')['stage']
        self.s['world']['minute']+=1440
        self.assertEqual(living_world.project(self.s,'emily')['stage'],first)
        self.s['world']['cast']['emily'].update(location='flowers',journey=None,activity='Working on project')
        before=living_world.ensure(self.s)['projects']['emily']['work_minutes']
        a.tick(self.s)
        self.assertEqual(living_world.ensure(self.s)['projects']['emily']['work_minutes'],before+5)

    def test_requested_quiet_period_suppresses_followup(self):
        self.home('emily'); t=m.thread(self.s,'emily'); t['last_reply']=0
        t['muted_until']=self.s['world']['minute']+1440
        with patch.object(a,'chance',return_value=0): m.tick(self.s)
        self.assertIsNone(t['reason'])

    def test_legacy_project_stage_migrates_without_inventing_help(self):
        import living_world
        self.s['living_world']['version']=1
        self.s['world']['minute']+=6*1440
        p=living_world.project(self.s,'emily')
        self.assertEqual(p['stage'],3)
        self.assertFalse(p['helped'])


if __name__=='__main__': unittest.main()
