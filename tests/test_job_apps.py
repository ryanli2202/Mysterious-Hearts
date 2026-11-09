import copy
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
import game_core as core
import job_apps as j
import town
import hidden_cast
import four_aces


def place(s,venue,day=0,hour=10):
    s['world'].update(location=venue,minute=day*1440+hour*60)
    s['world']['cast'][s['player']].update(location=venue,journey=None)


def advance(s,minutes,*args): s['world']['minute']+=minutes


class JobAppsTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('rei')
        self.timer=patch.object(j.careers,'spend_time',advance); self.timer.start(); self.addCleanup(self.timer.stop)

    def test_additive_save_and_all_real_locations(self):
        old=copy.deepcopy(self.s); j.ensure(self.s)
        for key,value in old.items(): self.assertEqual(value,self.s[key])
        self.assertEqual(j.ensure(self.s),j.ensure(json.loads(json.dumps(self.s))))
        for spec in [*j.JOBS.values(),*j.CONTRACTS.values()]: self.assertIn(spec['venue'],town.LOCATIONS)

    def test_all_jobs_and_once_daily_across_switches(self):
        for key,spec in j.JOBS.items():
            s=core.fresh('rei'); j.apply(s,key); place(s,spec['venue'],hour=spec['hours'][0])
            before=s['world']['money']; j.begin_shift(s)
            s=json.loads(json.dumps(s)); j.resolve(s,0)
            self.assertEqual(s['world']['money']-before,spec['pay'])
            with self.assertRaises(ValueError): j.resolve(s,0)
            j.apply(s,'barista' if key!='barista' else 'model')
            place(s,j.JOBS[j.ensure(s)['employment']]['venue'])
            with self.assertRaises(ValueError): j.begin_shift(s)

    def test_promotion_is_earned_and_retained(self):
        j.apply(self.s,'model')
        with self.assertRaises(ValueError): j.promote(self.s)
        for day in range(15):
            place(self.s,'studio',day); j.begin_shift(self.s); j.resolve(self.s,1)
            if day in (2,7,14): j.promote(self.s)
        self.assertEqual(j.profile(self.s,'model')['rank'],3)
        j.apply(self.s,'cinema'); j.apply(self.s,'model')
        self.assertEqual(j.profile(self.s,'model')['rank'],3)

    def test_guards_and_expired_work(self):
        j.apply(self.s,'oculus'); place(self.s,'downtown')
        with self.assertRaises(ValueError): j.begin_shift(self.s)
        place(self.s,'site_07_reception',hour=20)
        with self.assertRaises(ValueError): j.begin_shift(self.s)
        place(self.s,'site_07_reception'); now=self.s['world']['minute']
        self.s['scheduled_events']=[dict(start=now,end=now+60)]
        with self.assertRaises(ValueError): j.begin_shift(self.s)
        self.s['scheduled_events']=[]; j.begin_shift(self.s); advance(self.s,61)
        with self.assertRaises(ValueError): j.resolve(self.s,1)
        j.withdraw(self.s); self.assertIsNone(j.ensure(self.s)['pending'])

    def ready(self):
        d=j.ensure(self.s)
        d.update(reputation=55,completed=10,gang=dict(name='Test crew',role='Founder',standing=3))
        d['connections'].update(Syndicate=3,Shinokami=3)
        return d

    def test_recruitment_gates_and_rank_ceiling_every_branch(self):
        for branch in j.BRANCHES:
            self.s=core.fresh('rei')
            with self.assertRaises(ValueError): j.sponsor(self.s,branch)
            d=self.ready(); j.sponsor(self.s,branch)
            with self.assertRaises(ValueError): j.review(self.s)
            for day in range(18):
                place(self.s,j.BRANCHES[branch][1]+'_reception',day)
                j.faction_assignment(self.s); j.resolve(self.s,0)
                if day in (2,6,11,17): j.review(self.s)
            self.assertEqual(d['membership']['rank'],4)
            with self.assertRaises(ValueError): j.review(self.s)
            with self.assertRaises(ValueError): j.sponsor(self.s,branch)
            self.assertFalse(hidden_cast.hq_access(self.s,'rei'))
            self.assertNotIn('rei',four_aces.INSIDERS)
            self.assertFalse(self.s.get('hq_invitations'))
            self.assertFalse(self.s.get('crime_operations',{}).get('people',{}).get('rei',{}).get('permits'))
            last=18
            for target in range(5,len(j.BRANCHES[branch][2])):
                count,rep=j.progression.REVIEWS[target]
                for day in range(last,count):
                    place(self.s,j.BRANCHES[branch][1]+'_reception',day)
                    j.faction_assignment(self.s); j.resolve(self.s,0)
                j.review(self.s); last=count
                self.assertEqual(d['membership']['rank'],target)
                self.assertEqual(hidden_cast.hq_access(self.s,'rei'),branch!='Shinokami')
            with self.assertRaises(ValueError): j.review(self.s)

    def test_playable_criminal_path_from_zero(self):
        for day in range(13):
            d=j.ensure(self.s)
            key='syndicate' if d['reputation']>=40 else 'resale' if d['reputation']>=20 else 'parcel'
            place(self.s,j.CONTRACTS[key]['venue'],day)
            j.accept(self.s,key); j.resolve(self.s,0)
            if day==4: j.gang(self.s,'New crew')
        j.sponsor(self.s,'Hearts')
        self.assertEqual(j.ensure(self.s)['membership']['rank'],0)

    def test_heat_failure_and_rehabilitation(self):
        d=self.ready(); j.sponsor(self.s,'Spades')
        for day in range(2):
            place(self.s,'site_08_reception',day); j.ensure(self.s); d['heat']=25
            j.faction_assignment(self.s); before=self.s['world']['money']; j.resolve(self.s,2)
            self.assertEqual(before,self.s['world']['money'])
        with self.assertRaises(ValueError): j.faction_assignment(self.s)
        with self.assertRaises(ValueError): j.review(self.s)
        d.update(heat=0,reputation=50); j.review(self.s)
        self.assertEqual(d['membership']['strikes'],0)

    def test_civilian_employment_and_private_contracts_do_not_reveal_secrets(self):
        before=copy.deepcopy(self.s.get('discoveries'))
        j.apply(self.s,'oculus'); place(self.s,'site_07_reception'); j.begin_shift(self.s); j.resolve(self.s,1)
        self.assertEqual(before,self.s.get('discoveries'))
        self.assertFalse(hidden_cast.hq_access(self.s,'rei'))
        s=core.fresh('ivan'); j.ensure(s).update(reputation=100)
        with self.assertRaises(ValueError): j.sponsor(s,'Clubs')
        self.assertTrue(hidden_cast.hq_access(s,'ivan'))

    def test_contract_deadline_rival_and_persistence(self):
        place(self.s,'downtown'); j.accept(self.s,'parcel')
        restored=json.loads(json.dumps(self.s)); advance(restored,1441)
        with self.assertRaises(ValueError): j.resolve(restored,0)
        j.withdraw(restored)
        d=self.ready(); j.withdraw(self.s); j.sponsor(self.s,'Diamonds')
        with self.assertRaises(ValueError): j.accept(self.s,'shinokami')

    def test_real_save_and_clock_complete_remaining_shift(self):
        self.timer.stop()
        j.apply(self.s,'model'); place(self.s,'studio'); j.begin_shift(self.s)
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'jobs.json'; core.save(self.s,path); restored=core.load(path)
        self.assertEqual(restored['job_apps'],self.s['job_apps'])
        import world_loop
        world_loop.advance(restored,10)
        j.resolve(restored,1)
        self.assertEqual(restored['world']['minute'],660)
        self.assertEqual(j.profile(restored,'model')['shifts'],1)

    def test_executive_gates_private_reveal_and_saved_access(self):
        d=self.ready(); j.sponsor(self.s,'Spades'); m=d['membership']
        m.update(rank=4,assignments=25); d['reputation']=90
        with self.assertRaises(ValueError): j.review(self.s)
        with self.assertRaises(ValueError): j.executive_briefing(self.s)
        m['assignments']=26; d['heat']=30
        with self.assertRaises(ValueError): j.review(self.s)
        d['heat']=0; d['reputation']=89
        with self.assertRaises(ValueError): j.review(self.s)
        d['reputation']=90; j.review(self.s)
        for p in four_aces.CAST.values(): self.assertIn(p['name'],j.executive_briefing(self.s))
        self.assertTrue(four_aces.knows_identities(self.s,'rei'))
        self.assertFalse(hidden_cast.hq_access(self.s,'emily'))
        self.assertFalse(hidden_cast.hq_access(core.fresh('rei'),'rei'))
        private=four_aces.private_context('martos',['rei'],self.s)
        self.assertIn('Executive induction',private)
        mixed=four_aces.private_context('martos',['rei','emily'],self.s)
        self.assertNotIn('Shared Ace working history',mixed)
        self.assertIn('uncleared',mixed['Audience clearance'])
        import social_world
        self.assertIn('Executive induction',social_world.reference_for(self.s,'martos',['rei'],'Syndicate')['Vendetta AU'])
        place(self.s,'syndicate_hq')
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'executive.json'; core.save(self.s,path); restored=core.load(path)
        self.assertTrue(hidden_cast.hq_access(restored,'rei'))
        self.assertEqual(restored['world']['location'],'syndicate_hq')
        place(restored,'downtown')
        import world_loop
        with self.assertRaises(ValueError): world_loop.start_trip(restored,'rei','syndicate_hq',['emily'])
        j.travel(restored,'syndicate_hq')
        actor=restored['world']['cast']['rei']
        self.assertTrue(actor['location']=='syndicate_hq' or (actor.get('journey') or {}).get('destination')=='syndicate_hq')


if __name__=='__main__': unittest.main()
