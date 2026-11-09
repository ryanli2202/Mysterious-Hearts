import json
import tempfile
import unittest
from pathlib import Path
import game_core as core
import scheduled_events as events
import story_calendar as calendar
import qol


class QualityOfLifeTests(unittest.TestCase):
    def setUp(self):
        self.s = core.fresh('rei')
        self.s['world']['minute'] = 8*60

    def event(self, **kw):
        args = dict(title='Tea together', day=calendar.START.isoformat(), time='10:00',
                    venue='cafe', guests=['emily', 'sophie'], duration=60)
        args.update(kw)
        return events.create(self.s, **args)

    def test_reminders_attendance_and_end(self):
        e = self.event()
        core.town.loop.advance(self.s, 60)
        self.assertEqual(e['reminded'], [60])
        core.town.loop.advance(self.s, 45)
        self.assertEqual(e['reminded'], [60,15])
        core.town.loop.advance(self.s, 15)
        for who in e['guests']:
            self.assertEqual(self.s['world']['cast'][who]['location'], 'cafe')
            self.assertIsNone(self.s['world']['cast'][who]['journey'])
        self.assertEqual(len(self.s['event_notifications']), 3)
        core.town.loop.advance(self.s, 60)
        self.assertIsNone(events.active(self.s, 'emily'))

    def test_large_time_jump_and_cancel(self):
        e = self.event()
        core.town.loop.advance(self.s, 150)
        self.assertEqual(e['reminded'], [60,15])
        e['cancelled'] = True
        self.assertIsNone(events.active(self.s, 'emily'))

    def test_event_survives_load_without_duplicate_reminders(self):
        self.event()
        core.town.loop.advance(self.s, 60)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'story.json'; core.save(self.s,path)
            restored = core.load(path)
            core.town.loop.advance(restored, 60)
            self.assertEqual(restored['scheduled_events'][0]['reminded'], [60,15])
            self.assertEqual(len(restored['event_notifications']),3)

    def test_invalid_and_overlapping_events(self):
        for kw in [dict(time='07:00'),dict(time='24:10'),dict(guests=[]),dict(guests=['rei']),dict(venue='car:rei')]:
            with self.assertRaises(ValueError): self.event(**kw)
        self.event()
        with self.assertRaises(ValueError): self.event(time='10:30')
        self.event(time='11:00',guests=['emily'])

    def test_join_checks_place_and_creates_selected_group(self):
        e=self.event(); core.town.loop.advance(self.s,120)
        with self.assertRaises(ValueError): events.join(self.s,e)
        self.s['world']['location']='cafe'
        self.s['world']['cast']['rei'].update(location='cafe',journey=None)
        gid=events.join(self.s,e)
        self.assertEqual(self.s['groups'][gid]['members'],['emily','sophie'])
        events.cancel(self.s,e)
        self.assertFalse(self.s['groups'][gid]['open'])
        self.assertEqual(self.s['world']['party'],[])

    def test_future_day_and_single_guest(self):
        from datetime import timedelta
        e = self.event(day=(calendar.START+timedelta(days=1)).isoformat(),guests=['emily'])
        core.town.loop.advance(self.s, 26*60, finish_day=True)
        self.assertEqual(e['reminded'],[60,15])
        self.assertEqual(self.s['world']['cast']['emily']['location'],'cafe')

    def test_cancel_before_event_suppresses_reminders(self):
        e=self.event(); events.cancel(self.s,e)
        core.town.loop.advance(self.s,120)
        self.assertEqual(e['reminded'],[])
        self.assertNotIn('event_notifications',self.s)

    def test_recovery_drafts_and_bookmarks_roundtrip(self):
        self.s['drafts']={'route:emily':'Still typing'}
        self.s['bookmarks']=['route:emily:0']
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json'; core.save(self.s,path)
            self.s['save_name']='Second version'; core.save(self.s,path)
            self.assertNotIn('save_name',core.load(path.with_name('story.backup1.json')))
            loaded=core.load(path)
            self.assertEqual(loaded['drafts'],self.s['drafts'])
            self.assertEqual(loaded['bookmarks'],self.s['bookmarks'])

    def test_agenda_and_change_feed_are_grounded(self):
        e=self.event(); before=qol.stats(self.s)
        self.s['relationships']['emily']['trust']+=2
        self.assertIn('Emily · Trust +2',qol.changes(before,self.s))
        self.assertIn('Tea together','\n'.join(qol.agenda(self.s)))
        self.assertIn('Instant travel',qol.travel_preview(self.s,'cafe'))


if __name__ == '__main__': unittest.main()
