import unittest
import game_core as core
import job_apps as jobs
import crime_diplomacy as dip
import syndicate_council as council

class IvanStatusTests(unittest.TestCase):
    def test_membership_and_standing_migration(self):
        s=core.fresh('ivan')
        self.assertEqual(jobs.ensure(s)['story_membership']['role'],'Black and White Joker')
        b=dip.ensure(s)
        self.assertEqual(dip.relation(b,'syndicate'),98)
        b.pop('joker_standing_v1'); b['relations']['syndicate']=25
        self.assertEqual(dip.ensure(s)['relations']['syndicate'],88)
        b['relations']['syndicate']=70
        self.assertEqual(dip.ensure(s)['relations']['syndicate'],70)
        self.assertIsNone(jobs.ensure(s)['membership'])
        self.assertEqual(dip.relation(dip.ensure(core.fresh('garrett')),'syndicate'),35)

    def test_calendar_recovers_cancelled_and_extends_horizon(self):
        s=core.fresh('ivan'); council.ensure(s)
        e=s['scheduled_events'][0]; e['cancelled']=True
        horizon=s['world']['minute']+180*1440
        council.ensure(s,horizon)
        self.assertFalse(e['cancelled']); self.assertTrue(e['mandatory'])
        self.assertGreater(max(x['start'] for x in s['scheduled_events']),horizon-council.WEEK)
        ids=[x['id'] for x in s['scheduled_events']]
        council.ensure(s,horizon)
        self.assertEqual(ids,[x['id'] for x in s['scheduled_events']])

if __name__=='__main__': unittest.main()
