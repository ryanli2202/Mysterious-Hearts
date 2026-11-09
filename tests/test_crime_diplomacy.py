import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import game_core as core
import custom_protagonist
import crime_diplomacy as dip
import job_apps as jobs
import careers
import hidden_cast
from test_custom_protagonist import PROFILE


def place(s,venue,minute):
    s['world'].update(location=venue,minute=minute,party=[])
    s['world']['cast'][s['player']].update(location=venue,journey=None)


def fast(s,minutes,*args):
    s['world']['minute']+=minutes
    dip.tick(s)


def attend(s,m):
    dip.begin(s,m['id'])
    for _ in range(3): dip.discuss(s,m['id'])


class DiplomacyTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('garrett')
        self.timer=patch.object(careers,'spend_time',fast); self.timer.start(); self.addCleanup(self.timer.stop)

    def arrange(self,s=None,target='waterfront',terms='measured'):
        s=s or self.s
        b=dip.ensure(s)
        start=(s['world']['minute']//1440+1)*1440+1080
        m=dip.book(s,target,start)
        place(s,m['venue'],start)
        attend(s,m)
        dip.conclude(s,m['id'],terms)
        return b,m

    def test_gate_established_and_custom_all_pathways(self):
        for player in ('garrett','ivan'):
            s=core.fresh(player); b=dip.ensure(s)
            self.assertGreater(b['treasury'],5000)
            b['treasury']=1234; self.assertEqual(dip.ensure(s)['treasury'],1234)
        for branch,threshold in (('Clubs',5),('Shinokami',4)):
            s=core.fresh('minsu'); d=jobs.ensure(s)
            with self.assertRaises(ValueError): dip.ensure(s)
            d['membership']=dict(faction=jobs.BRANCHES[branch][0],branch=branch,rank=threshold-1,strikes=0)
            with self.assertRaises(ValueError): dip.ensure(s)
            d['membership']['rank']=threshold; self.assertEqual(dip.ensure(s)['treasury'],5000)
            d['membership']['strikes']=2
            with self.assertRaises(ValueError): dip.ensure(s)
        with tempfile.TemporaryDirectory(dir=core.ROOT/'assets'/'generated') as folder:
            path=Path(folder)/'portrait.png'
            art=Image.new('RGBA',(8,8),(0,0,0,0)); art.putpixel((4,4),(60,90,100,255)); art.save(path)
            s=custom_protagonist.create(PROFILE,path.relative_to(core.ROOT).as_posix())
            d=jobs.ensure(s); self.assertIsNone(dip.mandate(s))
            d['gang']=dict(name='Custom Circle',role='Founder',rank=3,standing=16)
            b,m=self.arrange(s)
            deal=b['deals'][0]; dip.settle(s,deal['id'])
            self.assertEqual(deal['status'],'completed')
            self.assertNotIn('custom',s.get('careers',{}).get('tracks',{}))

    def test_meeting_guards_conflicts_and_read_only_commitments(self):
        before=copy.deepcopy(self.s); self.assertEqual(dip.commitments(self.s),[]); self.assertEqual(before,self.s)
        b=dip.ensure(self.s); m=dip.book(self.s,'waterfront',2520)
        self.assertIsNotNone(careers.conflict(self.s,2520,2580))
        with self.assertRaises(ValueError): dip.book(self.s,'rojos',2520)
        other=dip.book(self.s,'rojos',2640)
        with self.assertRaises(ValueError): careers.book(self.s,'dragons','2050-01-02','20:00')
        dip.cancel(self.s,other['id'])
        with self.assertRaises(ValueError): dip.conclude(self.s,m['id'],'relations')
        place(self.s,'market',2520)
        with self.assertRaises(ValueError): dip.conclude(self.s,m['id'],'relations')
        place(self.s,m['venue'],2520); self.s['world']['party']=['emily']
        with self.assertRaises(ValueError): dip.conclude(self.s,m['id'],'relations')
        self.s['world']['party']=[]; attend(self.s,m); dip.conclude(self.s,m['id'],'relations')
        self.assertEqual(m['status'],'completed')
        self.assertIsNone(careers.conflict(self.s,2520,2580))
        with self.assertRaises(ValueError): dip.conclude(self.s,m['id'],'relations')

    def test_two_way_calendar_conflict_and_reschedule(self):
        self.s['scheduled_events']=[dict(start=2520,end=2580,cancelled=False)]
        with self.assertRaises(ValueError): dip.book(self.s,'waterfront',2520)
        self.s['scheduled_events']=[]; b=dip.ensure(self.s); m=dip.book(self.s,'waterfront',2520)
        dip.reschedule(self.s,m['id']); self.assertEqual(m['start'],3960)
        dip.cancel(self.s,m['id']); self.assertFalse(dip.commitments(self.s))

    def test_success_money_daily_limit_career_and_once_only(self):
        c=careers.get(self.s,'dragons'); c['pressure']=20
        careers.start_project(self.s,'dragons')
        wallet=self.s['world']['money']; b,m=self.arrange()
        self.assertEqual(b['treasury'],23500)
        deal=b['deals'][0]; dip.settle(self.s,deal['id'])
        self.assertEqual(b['treasury'],25960)
        self.assertEqual(self.s['world']['money'],wallet+240)
        self.assertEqual(c['project']['quality'],8); self.assertEqual(c['pressure'],14)
        with self.assertRaises(ValueError): dip.settle(self.s,deal['id'])
        with self.assertRaises(ValueError): jobs.accept(self.s,'parcel')
        self.assertTrue(careers.ensure(self.s)['history'])

    def test_aggressive_failure_and_default_exactly_once(self):
        b,m=self.arrange(terms='aggressive'); jobs.ensure(self.s)['heat']=40
        deal=b['deals'][0]; dip.settle(self.s,deal['id'])
        self.assertEqual(deal['status'],'failed'); self.assertEqual(b['treasury'],21000)
        b,m=self.arrange(); deal=b['deals'][-1]
        self.s['world']['minute']=deal['deadline']+1; dip.tick(self.s)
        self.assertEqual(deal['status'],'defaulted')
        history=copy.deepcopy(b['history']); dip.tick(self.s); self.assertEqual(b['history'],history)

    def test_invites_leaders_and_no_access_leaks(self):
        b=dip.ensure(self.s); self.assertEqual(len(b['invitations']),1)
        dip.ensure(self.s); self.assertEqual(len(b['invitations']),1)
        with self.assertRaises(ValueError): dip.request(self.s,'waterfront',True)
        for _ in range(2): self.arrange(terms='relations')
        self.assertTrue(dip.leader_ready(self.s,b,'waterfront'))
        dip.request(self.s,'waterfront',True)
        self.assertTrue(b['meetings'][-1]['leader'])
        self.assertFalse(hidden_cast.hq_access(self.s,'garrett'))
        self.assertEqual(dip.context(self.s,'rei'),[])
        self.assertTrue(dip.context(self.s,'garrett'))

    def test_automatic_leader_invite_heat_and_busy_obligations(self):
        b=dip.ensure(self.s); b['influence']=10; b['relations']['waterfront']=55
        place(self.s,'downtown',6*1440+480)
        dip.ensure(self.s)
        self.assertTrue(any(i['target']=='waterfront' and i['leader'] for i in b['invitations']))
        jobs.ensure(self.s)['heat']=60
        with self.assertRaises(ValueError): dip.request(self.s,'rojos')
        jobs.ensure(self.s)['heat']=0
        b,m=self.arrange(); deal=b['deals'][0]
        jobs.ensure(self.s)['heat']=60
        with self.assertRaises(ValueError): dip.settle(self.s,deal['id'])
        self.assertEqual(deal['status'],'active')
        with self.assertRaises(ValueError): jobs.sponsor(self.s,'Clubs')

    def test_invitation_accept_decline_and_missed(self):
        b=dip.ensure(self.s); invitation=b['invitations'][0]
        dip.invitation(self.s,invitation['id'])
        self.assertEqual(invitation['status'],'accepted')
        with self.assertRaises(ValueError): dip.invitation(self.s,invitation['id'])
        m=b['meetings'][0]; self.s['world']['minute']=m['end']; dip.tick(self.s)
        self.assertEqual(m['status'],'missed')
        rep=dip.relation(b,m['target']); dip.tick(self.s); self.assertEqual(dip.relation(b,m['target']),rep)

    def test_extend_abandon_fund_and_affiliation(self):
        b,m=self.arrange(target='hamayashi')
        self.assertTrue(jobs.ensure(self.s)['hamayashi_affiliated'])
        self.assertFalse(jobs.ensure(self.s)['hamayashi_discovery']['return_known'])
        deal=b['deals'][0]; due=deal['deadline']; dip.extend(self.s,deal['id'])
        self.assertEqual(deal['deadline'],due+1440)
        with self.assertRaises(ValueError): dip.extend(self.s,deal['id'])
        dip.abandon(self.s,deal['id']); self.assertEqual(b['treasury'],24250)
        money=self.s['world']['money']; dip.fund(self.s)
        self.assertEqual(self.s['world']['money'],money-1000); self.assertEqual(b['treasury'],25250)

    def test_real_clock_and_save_load_keep_pending_meeting_and_deal(self):
        self.timer.stop()
        b=dip.ensure(self.s); m=dip.book(self.s,'waterfront',2520)
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'diplomacy.json'; core.save(self.s,path); s=core.load(path)
        place(s,m['venue'],m['start']+10)
        attend(s,m)
        dip.conclude(s,m['id'],'measured')
        self.assertEqual(s['world']['minute'],m['end'])
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'deal.json'; core.save(s,path); restored=core.load(path)
        self.assertEqual(restored['crime_diplomacy'],s['crime_diplomacy'])
        b=dip.ensure(restored); dip.settle(restored,b['deals'][0]['id'])
        self.assertEqual(restored['world']['minute'],m['end']+60)


if __name__=='__main__': unittest.main()
