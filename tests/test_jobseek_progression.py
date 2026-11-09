"""Career development, migration, economic boundaries and end-to-end progression."""
import copy
import json
import unittest
from unittest.mock import patch
import game_core as core
import job_apps as jobs
import jobseek_progression as dev
from test_job_apps import place, advance


class CareerDevelopmentTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('rei')
        jobs.apply(self.s,'barista')
        self.s['world']['money']=20000
        place(self.s,'cafe')
        self.timer=patch.object(jobs.careers,'spend_time',advance)
        self.timer.start(); self.addCleanup(self.timer.stop)

    def test_legacy_profile_and_pending_roundtrip(self):
        d=jobs.ensure(self.s)
        d['jobs']['barista']=dict(rank=3,shifts=15,craft=30,reliability=85)
        p=jobs.profile(self.s,'barista')
        self.assertEqual(p['rank'],3)
        self.assertEqual(p['portfolio'],[])
        jobs.begin_shift(self.s)
        del d['pending']['brief']
        restored=json.loads(json.dumps(self.s))
        jobs.resolve(restored,0)
        self.assertEqual(jobs.profile(restored,'barista')['shifts'],16)

    def test_training_guards_and_cross_employer_daily_limit(self):
        before=self.s['world']['money']
        dev.train(self.s,'craft')
        self.assertEqual(self.s['world']['money'],before-120)
        self.assertEqual(self.s['world']['minute'],630)
        jobs.apply(self.s,'model'); place(self.s,'studio')
        with self.assertRaises(ValueError): dev.train(self.s,'craft')
        place(self.s,'downtown',1)
        with self.assertRaises(ValueError): dev.train(self.s,'craft')
        place(self.s,'studio',1)
        self.s['scheduled_events']=[dict(start=600+1440,end=660+1440)]
        with self.assertRaises(ValueError): dev.train(self.s,'craft')
        self.s['scheduled_events']=[]
        self.s['world']['money']=0
        with self.assertRaises(ValueError): dev.train(self.s,'craft')
        self.assertEqual(jobs.profile(self.s,'model')['courses'],{})

    def test_projects_deadline_withdraw_and_no_duplicate_pay(self):
        p=jobs.profile(self.s,'barista'); p.update(rank=1,mentor=20)
        dev.project(self.s)
        for day in range(3):
            place(self.s,'cafe',day)
            jobs.begin_shift(self.s); jobs.resolve(self.s,0)
        before=self.s['world']['money']; dev.deliver(self.s)
        self.assertEqual(self.s['world']['money']-before,670)
        self.assertEqual(p['budget'],200)
        with self.assertRaises(ValueError): dev.deliver(self.s)
        dev.project(self.s)
        jobs.apply(self.s,'model'); place(self.s,'studio',11)
        jobs.apply(self.s,'barista')
        before=self.s['world']['money']; dev.deliver(self.s)
        self.assertEqual(self.s['world']['money'],before)
        self.assertIsNone(p['project'])

    def test_deadline_requires_full_delivery_and_full_shift(self):
        p=jobs.profile(self.s,'barista'); p.update(rank=1,mentor=20)
        dev.project(self.s)
        p['project'].update(stages=3,deadline=610)
        with self.assertRaises(ValueError): dev.deliver(self.s)
        p['project'].update(stages=0,deadline=630)
        jobs.begin_shift(self.s); jobs.resolve(self.s,0)
        self.assertEqual(p['project']['stages'],0)

    def test_workplace_guards_and_retained_specialisation(self):
        dev.network(self.s,'mentor')
        with self.assertRaises(ValueError): dev.network(self.s,'team')
        with self.assertRaises(ValueError): dev.specialise(self.s,'expert')
        p=jobs.profile(self.s,'barista')
        p.update(rank=2,mentor=20,certificates=['craft'])
        dev.specialise(self.s,'expert')
        self.assertEqual(dev.wage('barista',p),420)
        with self.assertRaises(ValueError): dev.specialise(self.s,'coordinator')
        jobs.apply(self.s,'model'); jobs.apply(self.s,'barista')
        self.assertEqual(p['specialty'],'expert')
        jobs.begin_shift(self.s)
        with self.assertRaises(ValueError): dev.network(self.s,'mentor')
        with self.assertRaises(ValueError): jobs.promote(self.s)

    def test_management_uses_department_budget(self):
        p=jobs.profile(self.s,'barista')
        with self.assertRaises(ValueError): dev.manage(self.s,'team')
        p.update(rank=3,portfolio=[{}],budget=200)
        before=self.s['world']['money']
        dev.manage(self.s,'team')
        self.assertEqual(self.s['world']['money'],before)
        self.assertEqual(p['budget'],100)
        self.assertEqual(p['morale'],60)
        with self.assertRaises(ValueError): dev.manage(self.s,'quality')

    def test_playable_eight_rank_path_and_save(self):
        p=jobs.profile(self.s,'barista')
        for day in range(75):
            place(self.s,'cafe',day)
            if day<9: dev.train(self.s,('craft','service','leadership')[day//3])
            if day<2: dev.network(self.s,'mentor')
            if p['rank']>=2 and not p['specialty']: dev.specialise(self.s,'expert')
            if p['rank']>=1 and p['project'] is None: dev.project(self.s)
            jobs.begin_shift(self.s); jobs.resolve(self.s,1 if day%2 else 0)
            if p['project'] and p['project']['stages']==3: dev.deliver(self.s)
            if p['rank']<7:
                try: jobs.promote(self.s)
                except ValueError: pass
        self.assertEqual(p['rank'],7)
        self.assertGreaterEqual(len(p['portfolio']),8)
        with self.assertRaises(ValueError): jobs.promote(self.s)
        restored=json.loads(json.dumps(self.s))
        self.assertEqual(jobs.profile(restored,'barista'),p)
        self.assertEqual(jobs.ensure(restored)['reputation'],0)
        self.assertIsNone(jobs.ensure(restored)['membership'])
        jobs.apply(restored,'model'); jobs.apply(restored,'barista')
        self.assertEqual(restored['world']['job'],'Career fellow')

    def test_all_employers_and_saved_jobs(self):
        self.assertEqual(set(dev.WORKPLACES),set(jobs.JOBS))
        for key in jobs.JOBS:
            dev.save_job(self.s,key)
            self.assertIn(key,jobs.ensure(self.s)['saved_jobs'])
            dev.save_job(self.s,key)
            self.assertNotIn(key,jobs.ensure(self.s)['saved_jobs'])
            self.assertEqual(len(dev.titles(key)),8)
            self.assertEqual(len(set(dev.WORKPLACES[key][4:])),3)


if __name__=='__main__': unittest.main()
