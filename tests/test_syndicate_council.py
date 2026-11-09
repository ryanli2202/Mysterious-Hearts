import tempfile
import unittest
from pathlib import Path
import game_core as core
import careers
import scheduled_events as events
import syndicate_council as council
import world_loop


class CouncilTests(unittest.TestCase):
    def first(self, s):
        council.ensure(s)
        return next(e for e in s['scheduled_events'] if e.get('source') == council.SOURCE)

    def test_weekly_roster_and_access(self):
        s = core.fresh('ivan'); e = self.first(s)
        self.assertEqual(council.calendar.story_date(e['start']).weekday(), 6)
        self.assertEqual(e['start'] % 1440, 1200)
        self.assertEqual(set(e['guests']) | {'ivan'}, set(council.ROSTER))
        self.assertTrue(e['mandatory'])
        council.ensure(s)
        self.assertEqual(len(s['scheduled_events']), 9)
        self.assertEqual(s['scheduled_events'][1]['start']-e['start'], council.WEEK)
        s = core.fresh('garrett')
        self.assertFalse(council.eligible(s)); self.assertFalse(s['scheduled_events'])
        for rank, faction, branch, expected in [(5,'Syndicate','Clubs',False),
                (6,'Syndicate','Spades',True),(7,'Shinokami','Shinokami',False)]:
            s['job_apps'] = {'membership': dict(rank=rank,faction=faction,branch=branch)}
            self.assertEqual(council.eligible(s), expected)

    def test_no_backfill_and_no_cancellation(self):
        s = core.fresh('ivan'); s['scheduled_events'] = []; s['world']['minute'] = 90*1440
        e = self.first(s)
        self.assertGreaterEqual(e['start'], s['world']['minute'])
        with self.assertRaises(ValueError): events.cancel(s, e)
        self.assertIs(careers.conflict(s,e['start'],e['end']), e)

    def test_actual_clock_attendance_and_persistence(self):
        s = core.fresh('ivan'); e = self.first(s)
        s['world']['minute'] = e['start']-1
        s['world']['location'] = e['venue']
        s['world']['cast']['ivan'].update(location=e['venue'],journey=None,activity='Waiting')
        world_loop.advance(s, 1)
        for who in council.ROSTER:
            self.assertEqual(s['world']['cast'][who]['location'], e['venue'])
        self.assertEqual(e['attendance_minutes'], 0)
        events.join(s,e)
        events.observe(s)
        self.assertEqual(e['attendance_minutes'], 1)
        world_loop.advance(s, 44)
        self.assertEqual(e['attendance_minutes'],45)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'council.json'; core.save(s,p); s=core.load(p)
        e=next(x for x in s['scheduled_events'] if x['id']==e['id'])
        before=careers.get(s,'joker')['reliability']
        world_loop.advance(s,16)
        self.assertEqual(e['memory_phase'],'completed')
        self.assertEqual(careers.get(s,'joker')['reliability'],before)
        self.assertIsNone(s['active_group'])

    def test_missed_once_and_late_attendance(self):
        for minutes in (0,10):
            s=core.fresh('ivan'); e=self.first(s)
            e['attendance_minutes']=minutes
            d=careers.get(s,'joker'); before=d['reliability']; pressure=d['pressure']
            s['world']['minute']=e['end']+3
            events.tick(s); events.tick(s)
            self.assertEqual(d['reliability'],before-5)
            self.assertEqual(d['pressure'],pressure+10)
            self.assertEqual(e['memory_phase'],'missed')

    def test_private_world_roster_and_revocation(self):
        s=core.fresh('garrett'); start=council.week_start(s['world']['minute'])
        self.assertEqual(events.active(s,'ivan',start)['venue'],'syndicate_hq')
        self.assertFalse(s['scheduled_events'])
        s['job_apps']={'membership':dict(rank=6,faction='Syndicate',branch='Clubs')}
        e=self.first(s)
        s['job_apps']['membership']['rank']=5
        council.ensure(s)
        self.assertTrue(e['cancelled'])
        with self.assertRaises(ValueError): council.join(s,e)


if __name__ == '__main__': unittest.main()
