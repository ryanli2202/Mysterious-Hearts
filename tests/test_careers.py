import copy
import json
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
import careers as c
import game_core as core
import scheduled_events
import story_calendar as dates
import town
import world_loop


def place(s, key, day=0):
    spec=c.TRACKS[key]
    s['world']['minute']=day*1440+spec['hours'][0]*60
    s['world']['location']=spec['venue']
    s['world']['cast'][s['player']].update(location=spec['venue'],journey=None)


def fast_advance(s, minutes):
    s['world']['minute']+=minutes
    c.tick(s)


class CareersTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('rei')

    def book(self,s,key,day=4,kind='finale'):
        spec=c.TRACKS[key]
        return c.book(s,key,dates.story_date(day*1440).isoformat(),f'{spec["hours"][0]:02}:00',kind)

    def test_old_save_migration_is_additive_and_idempotent(self):
        before=copy.deepcopy(self.s)
        c.ensure(self.s); once=copy.deepcopy(self.s); c.ensure(self.s)
        self.assertEqual(once,self.s)
        for k,v in before.items(): self.assertEqual(self.s[k],v)
        self.assertEqual(c.get(self.s,'iron')['rank'],1)
        self.assertIsNone(c.get(self.s,'iron')['defence_due'])

    def test_all_eight_paths_and_invalid_ownership(self):
        with patch.object(world_loop,'advance',fast_advance):
            for key,spec in c.TRACKS.items():
                s=core.fresh(spec['player']); place(s,key)
                c.start_project(s,key); money=s['world']['money']; start=s['world']['minute']
                c.begin(s,key); c.choose(s,0); c.choose(s,1)
                self.assertEqual(s['world']['minute'],start+60)
                self.assertEqual(len(c.get(s,key)['project']['days']),1)
                self.assertEqual(s['world']['money']-money,0 if key in ('iron','taekwondo') else spec['pay'])
                before=copy.deepcopy(s)
                with self.assertRaises(ValueError): c.quick(s,key)
                self.assertEqual(before,s)
        with self.assertRaises(ValueError): c.get(self.s,'joker')

    def test_active_session_survives_json_and_pays_only_once(self):
        place(self.s,'modelling'); c.begin(self.s,'modelling'); c.choose(self.s,0)
        restored=json.loads(json.dumps(self.s)); money=restored['world']['money']
        with patch.object(world_loop,'advance',fast_advance): c.choose(restored,2)
        self.assertEqual(restored['world']['money'],money+4000)
        with self.assertRaises(ValueError): c.choose(restored,2)

    def test_normal_save_restores_project_bookings_and_pending_decision(self):
        place(self.s,'modelling'); c.start_project(self.s,'modelling')
        self.book(self.s,'modelling'); c.begin(self.s,'modelling'); c.choose(self.s,0)
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'career-story.json'
            core.save(self.s,path); restored=core.load(path)
        self.assertEqual(restored['careers'],self.s['careers'])
        with patch.object(world_loop,'advance',fast_advance): c.choose(restored,1)
        self.assertIsNone(restored['careers']['active'])

    def test_real_clock_consumes_duration_and_expires_unfinished_work(self):
        place(self.s,'modelling'); start=self.s['world']['minute']
        c.quick(self.s,'modelling')
        self.assertEqual(self.s['world']['minute'],start+60)
        place(self.s,'modelling',1); c.begin(self.s,'modelling')
        money=self.s['world']['money']; world_loop.advance(self.s,60)
        self.assertIsNone(c.ensure(self.s)['active'])
        self.assertEqual(self.s['world']['money'],money)

    def test_project_requires_three_days_and_future_finale(self):
        place(self.s,'modelling'); c.start_project(self.s,'modelling')
        b=self.book(self.s,'modelling')
        with patch.object(world_loop,'advance',fast_advance):
            for day in range(3):
                place(self.s,'modelling',day); c.quick(self.s,'modelling')
            place(self.s,'modelling',4)
            c.begin(self.s,'modelling',booking_id=b['id'])
        d=c.get(self.s,'modelling')
        self.assertIsNone(d['project']); self.assertEqual(d['completed'],1)
        self.assertEqual(b['status'],'completed')
        with self.assertRaises(ValueError): c.finish_project(self.s,'modelling',b['id'])

    def test_calendar_conflicts_in_both_directions_and_reschedule_atomicity(self):
        b=self.book(self.s,'modelling',1,'shift')
        day=dates.story_date(b['start']).isoformat()
        with self.assertRaises(ValueError): scheduled_events.create(self.s,'Lunch',day,'09:30','cafe',['emily'])
        scheduled_events.create(self.s,'Lunch',day,'12:00','cafe',['emily'])
        before=copy.deepcopy(b)
        with self.assertRaises(ValueError): c.book(self.s,'modelling',day,'12:00',replace=b['id'])
        self.assertEqual(before,b)
        c.book(self.s,'modelling',day,'14:00',replace=b['id'])
        self.assertEqual(b['status'],'rescheduled')

    def test_cancel_miss_and_reminders_do_not_repeat(self):
        b=self.book(self.s,'modelling',1,'shift'); d=c.get(self.s,'modelling')
        before=d['reliability']; c.cancel(self.s,b['id']); self.assertEqual(before,d['reliability'])
        b=self.book(self.s,'modelling',2,'shift')
        self.s['world']['minute']=b['start']-15; c.tick(self.s); count=len(self.s['event_notifications']); c.tick(self.s)
        self.assertEqual(count,len(self.s['event_notifications']))
        self.s['world']['minute']=b['end']; c.tick(self.s); c.tick(self.s)
        self.assertEqual(d['reliability'],before-5); self.assertEqual(b['status'],'missed')

    def test_late_arrival_window_uses_remaining_booking_time(self):
        b=self.book(self.s,'modelling',1,'shift'); place(self.s,'modelling',1)
        self.s['world']['minute']+=10
        with patch.object(world_loop,'advance',fast_advance):
            c.begin(self.s,'modelling',booking_id=b['id']); c.choose(self.s,1); c.choose(self.s,2)
        self.assertEqual(self.s['world']['minute'],b['end'])

    def test_preparation_fatigue_recovery_and_location_guards(self):
        place(self.s,'iron'); d=c.get(self.s,'iron')
        with self.assertRaises(ValueError): c.prepare(self.s,'iron','technique')
        self.s['world']['location']='arena'
        with patch.object(world_loop,'advance',fast_advance): c.prepare(self.s,'iron','technique')
        with self.assertRaises(ValueError): c.prepare(self.s,'iron','feedback')
        d['fatigue']=90; place(self.s,'iron',1)
        with self.assertRaises(ValueError): c.begin(self.s,'iron')
        self.s['world']['location']=town.HOMES['rei']
        with patch.object(world_loop,'advance',fast_advance): c.prepare(self.s,'iron','recovery')
        self.assertLess(d['fatigue'],90)

    def ready(self,s,key,day):
        c.start_project(s,key); d=c.get(s,key)
        d['project'].update(days=[day-3,day-2,day-1],quality=60)
        d.update(craft=100,fatigue=0,training=6)
        b=self.book(s,key,day); place(s,key,day)
        return d,b

    def test_champion_loss_comeback_and_deadline(self):
        place(self.s,'iron'); d,b=self.ready(self.s,'iron',4)
        d.update(craft=0,fatigue=80,training=2)
        with patch.object(world_loop,'advance',fast_advance): c.finish_project(self.s,'iron',b['id'])
        self.assertEqual(d['rank'],2)
        d,b=self.ready(self.s,'iron',12)
        with patch.object(world_loop,'advance',fast_advance): c.finish_project(self.s,'iron',b['id'])
        self.assertEqual(d['rank'],1)
        self.s['world']['minute']=d['defence_due']+1; c.tick(self.s)
        self.assertEqual(d['rank'],2); self.assertIsNone(d['defence_due'])

    def test_olympic_pathway_has_no_paid_medical_practice_or_repeat_medals(self):
        s=core.fresh('minsu'); place(s,'taekwondo'); money=s['world']['money']
        with patch.object(world_loop,'advance',fast_advance):
            for stage in range(6):
                d,b=self.ready(s,'taekwondo',4+stage*8)
                c.finish_project(s,'taekwondo',b['id'])
        self.assertEqual(d['stage'],5); self.assertEqual(len(d['medals']),1)
        self.assertEqual(s['world']['money'],money)

    def test_delegation_requires_review_and_builds_experience(self):
        s=core.fresh('garrett'); place(s,'dragons'); c.start_project(s,'dragons')
        d=c.get(s,'dragons'); person=c.TRACKS['dragons']['contacts'][0]
        with patch.object(world_loop,'advance',fast_advance):
            c.delegate(s,'dragons',person)
            with self.assertRaises(ValueError): c.review_delegation(s,'dragons')
            place(s,'dragons',2); c.review_delegation(s,'dragons')
        self.assertIsNone(d['delegation']); self.assertEqual(d['contacts'][person]['competence'],63)

    def test_private_updates_only_reach_explicit_recipient(self):
        s=core.fresh('ivan'); place(s,'joker'); c.record(s,'joker','Private branch dispute resolved.')
        self.assertEqual(c.context(s,['valentina']),[])
        c.share(s,'joker','valentina')
        self.assertEqual(len(c.context(s,['valentina'])),1)
        self.assertEqual(c.context(s,['valentina','rei']),[])
        with self.assertRaises(ValueError): c.share(s,'joker','nobody')
        self.assertNotIn('Private branch dispute',town.context(s,'rei'))

    def test_legacy_daily_lock_and_deadline_only_penalise_once(self):
        place(self.s,'modelling'); self.s['world']['career_shifts']=['0:rei:0']
        with self.assertRaises(ValueError): c.begin(self.s,'modelling')
        c.start_project(self.s,'modelling'); d=c.get(self.s,'modelling'); reliability=d['reliability']
        self.s['world']['minute']=d['project']['deadline']+1; c.tick(self.s); c.tick(self.s)
        self.assertEqual(d['reliability'],reliability-5)
        c.extend_project(self.s,'modelling'); self.assertFalse(d['project']['overdue'])
        with self.assertRaises(ValueError): c.extend_project(self.s,'modelling')


if __name__=='__main__': unittest.main()
