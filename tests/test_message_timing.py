from date_fixtures import next_morning
"""Regression coverage for busy/read-but-unanswered and zero-cost texts."""
import copy
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import autonomy
import game_core as core
import messaging as m
import town
import world_loop as loop

REPLY=dict(bubbles=['hello'],moment='none',pause_minutes=0)


class MessageTimingTests(unittest.TestCase):
    def state(self,player='rei',minute=14*60):
        s=core.fresh(player); s['world']['minute']=minute
        for p in s['autonomy']['people'].values(): p['next_decision']=10**12
        s['world']['cast']['emily'].update(location='emily_home',journey=None,activity='Free time')
        return s

    @patch.object(autonomy,'chance',return_value=0.)
    @patch.object(m,'affinity',return_value=50.)
    def test_followup_spacing_by_friendship(self, _affinity, _chance):
        s=self.state('minsu'); bond=s['relationships']['emily']
        m.profile(s,'emily')['social']=100
        for trust,close,multiplier in [(35,0,4),(49,25,4),(50,25,2),(70,54,2),(70,55,1),(95,90,1)]:
            with self.subTest(trust=trust,close=close):
                bond.update(trust=trust,closeness=close)
                self.assertEqual(m.followup_delay(s,'emily'),125*multiplier)

    def test_acquaintance_does_not_follow_up_at_old_deadline(self):
        s=self.state('minsu'); bond=s['relationships']['emily']
        bond.update(trust=35,closeness=0)
        t=m.thread(s,'emily'); t['last_reply']=s['world']['minute']
        delay=m.followup_delay(s,'emily')
        s['world']['minute']+=delay//4
        m.tick(s)
        self.assertIsNone(t['reason'])
        s['world']['minute']=t['last_reply']+delay
        with patch.object(m,'available',return_value=True), patch.object(m,'activity',return_value='Free time'):
            m.tick(s)
        self.assertEqual(t['reason']['kind'],'silence')

    @patch.object(autonomy,'chance',return_value=1.)
    def test_emily_prioritises_rei_over_minsu(self,_chance):
        rei=self.state('rei'); minsu=self.state('minsu')
        m.send(rei,'emily','Hello'); m.send(minsu,'emily','Hello')
        self.assertEqual(m.next_job(rei)['who'],'emily')
        self.assertIsNone(m.next_job(minsu))
        self.assertLess(m.followup_delay(rei,'emily'),m.followup_delay(minsu,'emily'))

    @patch.object(autonomy,'chance',return_value=1.)
    def test_double_text_speeds_up_instead_of_resetting_wait(self,_chance):
        s=self.state('minsu'); first=m.send(s,'emily','Hello')
        old=first['notice_at']['emily']
        m.send(s,'emily','Are you around?')
        self.assertLess(first['notice_at']['emily'],old)
        loop.advance(s,2)
        self.assertEqual(len(m.next_job(s)['ids']),2)

    @patch.object(autonomy,'chance',return_value=1.)
    def test_relationship_changes_affect_timing_and_harm_overrides_affinity(self,_chance):
        s=self.state('minsu'); before=m.timing(s,'emily')
        s['relationships']['emily'].update(trust=100,closeness=100,attraction=100)
        self.assertLess(m.timing(s,'emily'),before)
        s=self.state(); s['relationships']['emily'].update(status='strained',unresolved_harm=True)
        self.assertLess(m.affinity(s,'emily'),75)

    def test_read_message_survives_overnight_and_busy_clock_offset(self):
        s=self.state(minute=21*60)
        m.send(s,'emily','Hello'); self.assertIsNotNone(m.next_job(s))
        next_morning(s)
        # A previous short work-break window must not erase a ready reply.
        s['world']['minute']+=17
        s['world']['cast']['emily'].update(location='flowers',journey=None,activity='Flower-shop shift')
        job=m.next_job(s)
        self.assertEqual(job['who'],'emily'); self.assertEqual(job['ids'],[1])
        self.assertTrue(m.apply(s,job,REPLY))
        self.assertFalse(m.thread(s,'emily')['pending'])

    def test_legacy_read_backlog_migrates_without_new_text_postponing_it(self):
        s=self.state(minute=3360)
        t=m.thread(s,'emily'); s['messaging']['version']=1
        t['due']=3362
        t['pending']=[dict(id=1,text='Hello',minute=2105,read_by=['emily'],read_at={'emily':2108},answered_by=[])]
        s['messaging']['serial']=1
        m.send(s,'emily','Still around?')
        self.assertEqual(m.next_job(s)['ids'],[1,2])

    def test_player_reply_beats_older_unsolicited_message(self):
        s=self.state(); m.initiate(s,'sophie','A new thought')
        m.thread(s,'sophie')['due']=0
        m.send(s,'emily','Hello')
        self.assertEqual(m.next_job(s)['who'],'emily')

    def test_completed_sleeping_reply_does_not_block_other_chat(self):
        s=self.state(); m.send(s,'emily','Hello'); job=m.next_job(s)
        game=SimpleNamespace(bind=lambda *a,**kw:None,in_game=True,state_data=s,busy=False,suggestion_job=None,persist=lambda:None,render=lambda:None)
        pump=m.MessagePump(game); pump.running=(s,job)
        s['world']['cast']['emily']['activity']='Sleep'
        pump.results.put((s,job,REPLY,None))
        with patch.object(m,'next_job',return_value=None): pump.tick()
        self.assertIsNone(pump.running)
        self.assertIsNotNone(m.thread(s,'emily')['prepared'])
        m.send(s,'sophie','Hello'); loop.advance(s,10)
        s['world']['cast']['emily']['activity']='Sleep'
        self.assertEqual(m.next_job(s)['who'],'sophie')
        s['world']['cast']['emily']['activity']='Free time'
        with patch.object(m,'next_job',return_value=None): pump.tick()
        self.assertFalse(m.thread(s,'emily')['pending'])

    def test_burst_does_not_wake_sleeping_recipient(self):
        s=self.state(minute=23*60); s['world']['cast']['emily']['activity']='Sleep'
        m.send(s,'emily','Hello'); m.send(s,'emily','Another thought')
        self.assertIsNone(m.next_job(s))
        self.assertTrue(all(not msg['read_by'] for msg in m.thread(s,'emily')['pending']))

    def test_sent_and_received_bursts_cost_zero_minutes(self):
        s=self.state(); now=s['world']['minute']
        m.send(s,'emily','Hello'); m.send(s,'emily','One more thing')
        m.apply(s,m.next_job(s),dict(REPLY,bubbles=['hello','what’s up?']))
        self.assertEqual(s['world']['minute'],now)

    def test_accepted_visit_deadline_survives_starting_hangout(self):
        s=self.state(); home=loop.HOUSES[s['player']][0]
        s['world']['location']=home; s['world']['cast'][s['player']]['location']=home
        s['world']['cast']['emily']['location']=home
        offer=autonomy.request(s,'emily','visit','A visit',home)
        autonomy.respond(s,offer['id'],'accept')
        until=autonomy.person(s,'emily')['plan']['until']
        loop.advance(s,1)
        self.assertIsNotNone(autonomy.person(s,'emily')['plan'])
        loop.advance(s,until-s['world']['minute'])
        self.assertIsNone(s['world']['cast']['emily']['journey'])
        self.assertEqual(s['world']['cast']['emily']['location'],loop.appointment('emily',s['world']['minute'])[1])

    def test_overnight_plan_survives_in_person_channel_before_bedtime(self):
        s=self.state(minute=21*60+30); home=loop.HOUSES[s['player']][0]
        s['world']['location']=home; s['world']['cast'][s['player']]['location']=home
        s['world']['cast']['emily']['location']=home
        town.meet(s,'emily')
        o=autonomy.request(s,'emily','overnight','A separate sleeping place')
        autonomy.respond(s,o['id'],'accept'); loop.advance(s,40)
        self.assertEqual(autonomy.status(s,'emily'),'Asleep')
        self.assertEqual(s['world']['cast']['emily']['location'],home)

    def test_legacy_private_group_and_date_text_paths_cost_zero(self):
        import groups,dating
        from test_game import SCENE
        from date_fixtures import invite
        s=self.state('garrett'); now=s['world']['minute']
        core.commit(s,'Hello',copy.deepcopy(SCENE))
        self.assertEqual(s['world']['minute'],now)
        gid=groups.create_text(s,'Friends',['emily','sophie'])
        groups.commit(s,gid,'Hello',dict(narration='Incoming texts.',choices=SCENE['choices'],
            lines=[dict(speaker=core.CONTACTS[w][0],text='hello') for w in ('emily','sophie')]))
        self.assertEqual(s['world']['minute'],now)
        invite(s,'emily')
        self.assertEqual(s['world']['minute'],now)

    def test_helping_project_preserves_prior_progress(self):
        import living_world
        s=self.state(); s['world']['location']='flowers'; s['world']['cast'][s['player']]['location']='flowers'
        s['world']['cast']['emily']['location']='flowers'
        living_world.ensure(s)['projects']['emily']=dict(work_minutes=240)
        living_world.participate(s,'emily')
        self.assertGreaterEqual(living_world.ensure(s)['projects']['emily']['work_minutes'],240)

    def test_reported_promise_completion_is_owned_and_not_inferred(self):
        import memory_store as mem
        s=self.state()
        mem.utterance(s,'promise','I promise to bring a sketch.',s['player'],['rei','emily','sophie'],s['world']['minute'])
        original=mem.open_commitments(s,['rei','emily'])[0]
        msg=m.send(s,'emily','I finished the sketch I promised.')
        job=m.next_job(s)
        result=dict(REPLY,commitment_updates=[dict(id=original['id'],status='reported_fulfilled',evidence=msg['text'])])
        m.apply(s,job,result)
        self.assertFalse(mem.open_commitments(s,['rei','emily']))
        self.assertTrue(mem.open_commitments(s,['sophie']))
        latest=next(r for r in mem.ensure(s)['records'].values() if r.get('supersedes')==original['id'])
        self.assertIn('not independently verified',latest['certainty'])

    def test_small_npc_disagreement_can_repair_without_erasing_major_harm(self):
        s=self.state()
        for who,other in (('emily','valentina'),('valentina','emily')):
            p=autonomy.person(s,who); p['social']=20
            p['relationships'][other]=dict(interest=30,trust=30,closeness=20,tension=0)
        with patch.object(autonomy,'chance',return_value=0):
            autonomy.social_encounter(s,'emily','valentina','cafe')
            tie=autonomy.person(s,'emily')['relationships']['valentina']
            self.assertGreater(tie['minor_tension'],0)
            autonomy.social_encounter(s,'emily','valentina','cafe')
            self.assertEqual(tie['minor_tension'],0)
            tie['tension']=40
            autonomy.social_encounter(s,'emily','valentina','cafe')
            self.assertEqual(tie['tension'],40)

    def test_rain_changes_peer_plan_through_travel(self):
        import weather
        s=self.state(); now=s['world']['minute']
        s['world']['cast']['amy'].update(location='park',journey=None,activity='Free time')
        autonomy.person(s,'amy')['plan']=dict(kind='project',venue='park',until=now+90,target='amy')
        with patch.object(weather,'shelter',return_value=True): autonomy.control(s,'amy')
        self.assertIsNone(s['world']['cast']['amy']['journey'])
        import leisure
        self.assertNotIn(s['world']['cast']['amy']['location'],leisure.OUTDOORS)
        self.assertEqual(s['world']['cast']['amy']['location'],autonomy.person(s,'amy')['plan']['venue'])

    def test_legacy_town_contact_direct_text_uses_async_queue(self):
        import groups
        s=self.state(); s['npc_chats']={'Theo':dict(history=[],connection=dict(trust=60,closeness=70))}
        groups.sync_contacts(s); key='npc:Theo'
        m.send(s,key,'Hello Theo',True); loop.advance(s,15)
        job=m.next_job(s); self.assertEqual(job['who'],'Theo')
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(REPLY)}}):
            result=m.generate(copy.deepcopy(s),job)
        m.apply(s,job,result)
        self.assertEqual(s['groups'][key]['history'][-1]['speaker'],'Theo')
        self.assertFalse(m.thread(s,key,True)['pending'])

    def test_new_game_starts_new_year_at_eight_without_retiming_save(self):
        s=core.fresh('rei')
        self.assertEqual(s['world']['minute'],480)
        self.assertEqual((loop.dates.story_date(480).month,loop.dates.story_date(480).day),(1,1))
        s['world']['minute']=840
        town.ensure(s)
        self.assertEqual(s['world']['minute'],840)

    def test_free_acquaintance_can_reply_immediately(self):
        s=self.state('minsu')
        with patch.object(autonomy,'chance',return_value=0):
            m.send(s,'emily','Hello')
            self.assertIsNotNone(m.next_job(s))

    def test_work_replies_depend_on_relationship_and_bursts_keep_delay(self):
        close=self.state(); distant=self.state('minsu')
        for s in (close,distant):
            s['world']['cast']['emily']['activity']='Flower-shop shift'
        self.assertLess(m.timing(close,'emily')[0],m.timing(distant,'emily')[0])
        self.assertGreater(m.timing(close,'emily',True)[0],0)
        m.send(close,'emily','Hello')
        close['world']['minute']+=10
        m.tick(close)
        self.assertIsNotNone(m.next_job(close))

    def test_skip_makes_waiting_reply_ready_without_another_send(self):
        s=self.state('minsu')
        with patch.object(autonomy,'chance',return_value=1.):
            m.send(s,'emily','Hello')
            self.assertIsNone(m.next_job(s))
            loop.advance(s,15)
            self.assertEqual(m.next_job(s)['ids'],[1])

    def test_ready_reply_survives_skip_into_sleep_and_is_delivered_by_pump(self):
        s=self.state(minute=21*60)
        m.send(s,'emily','Hello')
        loop.advance(s,180)
        self.assertEqual(m.activity(s,'emily'),'Asleep')
        job=m.next_job(s)
        self.assertEqual(job['ids'],[1])
        game=SimpleNamespace(bind=lambda *a,**kw:None,in_game=True,state_data=s,busy=False,suggestion_job=None,persist=lambda:None,render=lambda:None)
        pump=m.MessagePump(game); pump.results.put((s,job,REPLY,None))
        with patch.object(m,'next_job',return_value=None): pump.tick()
        self.assertFalse(m.thread(s,'emily')['pending'])

    def test_repeated_silence_distinguishes_delivered_and_read(self):
        for unread,receipt in ((1,'delivered but not read'),(0,'read without a reply')):
            s=self.state(); t=m.thread(s,'emily')
            t.update(last_reply=s['world']['minute']-1000,followups=2)
            s['routes']['emily']['unread']=unread
            m.tick(s)
            self.assertIn(receipt,t['reason']['text'])
            self.assertEqual(t['followups'],3)
            m.apply(s,m.next_job(s),REPLY)
            m.tick(s)
            self.assertIsNone(t['reason'])

    def test_scheduled_checkin_survives_skip_into_sleep(self):
        s=self.state(minute=21*60)
        m.initiate(s,'emily','A thought to share')
        loop.advance(s,180)
        self.assertEqual(m.next_job(s)['who'],'emily')

    def test_reply_cancels_unsent_silence_followup(self):
        s=self.state(); t=m.thread(s,'emily')
        t['last_reply']=s['world']['minute']-1000
        m.tick(s)
        self.assertEqual(t['reason']['kind'],'silence')
        m.send(s,'emily','Sorry, I was busy earlier. How are you?')
        self.assertIsNone(t['reason'])
        self.assertEqual(t['followups'],0)

if __name__=='__main__': unittest.main()
