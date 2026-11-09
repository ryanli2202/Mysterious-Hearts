from datetime import date
from pathlib import Path
import tempfile
import unittest

import game_core as core
import story_calendar as dates
import town


class CalendarTests(unittest.TestCase):
    def test_winterfield_outings(self):
        for (month, day), outing in dates.OUTINGS.items():
            with self.subTest(event=outing.title):
                s = core.fresh('garrett')
                s['world']['minute'] = (date(2050, month, day)-dates.START).days*1440 + 600
                choice = next(iter(outing.activities))
                self.assertIn(outing.title, dates.context(s)['occasions'])
                with self.assertRaises(ValueError):
                    dates.celebrate(s, outing.title, 'rei', choice)
                town.travel(s, outing.venue)
                town.finish_drive(s)
                with self.assertRaises(ValueError):
                    dates.celebrate(s, outing.title, 'daniel', choice)
                self.assertIn('rei', dates.outing_companions(s))
                s['relationships']['amy']['status'] = 'dating'
                self.assertIn('amy', dates.outing_companions(s))
                self.assertTrue(dates.celebrate(s, outing.title, 'rei', choice))
                self.assertEqual(s['shared_events'][-1]['witnesses'], ['rei'])
                self.assertIn(choice, s['shared_events'][-1]['text'])
                self.assertTrue(town.present(s, 'rei'))
                self.assertFalse(dates.celebrate(s, outing.title, 'amy', choice))

    def test_dates_and_holidays(self):
        self.assertEqual(dates.context(core.fresh())['date'], 'Saturday, January 01, 2050')
        self.assertEqual(dates.story_date(59*1440), date(2050,3,1))
        self.assertEqual(dates.story_date((365*2+59)*1440), date(2052,2,29))
        self.assertEqual(dates.holiday(date(2050,11,24)), 'Thanksgiving')
        self.assertEqual(dates.holiday(date(2055,12,31)), 'New Year’s Day (observed)')
        for day in [date(2050,1,1), date(2050,1,8), date(2050,1,9), date(2050,12,25)]:
            s = core.fresh()
            s['world']['minute'] = (day - dates.START).days*1440 + 16*60
            # Isolate the authored holiday routine from optional autonomous outings.
            s['autonomy']['people']['emily']['next_decision']=10**12
            for p in s['autonomy']['people'].values(): p['next_decision']=10**12
            town.loop.advance(s, 90)
            self.assertEqual(s['world']['cast']['emily']['activity'],town.loop.appointment('emily',s['world']['minute'])[2])
            self.assertNotEqual(s['world']['cast']['emily']['activity'],'Flower-shop shift')
            self.assertIsNone(s['world']['cast']['emily']['journey'])

    def test_birthday_rollover_and_persistence(self):
        s = core.fresh()
        s['world']['minute'] = (date(2050,1,31)-dates.START).days*1440-1
        town.loop.advance(s, 2, finish_day=True)
        title = 'Samantha’s birthday'
        self.assertIn(title, s['routes']['samantha']['history'][-1]['content'])
        self.assertTrue(dates.celebrate(s,title))
        self.assertFalse(dates.celebrate(s,title))
        s['nicknames'] = {'samantha':'Sam'}
        s['world']['log'].append('Day 2 · 08:00: Went outside.')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'story.json'
            core.save(s,path)
            saved = core.load(path)
        self.assertEqual(core.contact_name(saved,'samantha'),'Sam')
        self.assertFalse(dates.celebrate(saved,title))
        self.assertEqual(saved['world']['log'][-1], 'Sun, Jan 02 · 08:00: Went outside.')

    def test_existing_2024_story_loads_in_2050(self):
        s = core.fresh()
        del s['calendar_start_year']
        s['world']['minute'] = 30 * 1440 + 600
        title = 'Samantha’s birthday'
        s['celebrations'] = ['2024-01-31/' + title]
        s['world']['log'] = ['Wed, Jan 31 · 10:00: Had birthday cake.']
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'story.json'
            core.save(s, path)
            saved = core.load(path)
            self.assertEqual(dates.context(saved)['date'], 'Monday, January 31, 2050')
            self.assertEqual(saved['world']['minute'], s['world']['minute'])
            self.assertEqual(saved['world']['log'], ['Mon, Jan 31 · 10:00: Had birthday cake.'])
            self.assertFalse(dates.celebrate(saved, title))
            core.save(saved, path)
            self.assertEqual(core.load(path), saved)

    def test_hidden_birthdays_and_seasonal_events(self):
        s = core.fresh()
        self.assertFalse(dates.events(s,date(2050,6,12)))
        town.hidden.mark_met(s,'lena')
        self.assertEqual(dates.events(s,date(2050,6,12))[0][2], 'lena')
        for month, day, title in [(4,1,'April Fools’ Day'), (10,31,'Halloween'), (12,25,'Christmas')]:
            self.assertIn(title, [e[0] for e in dates.events(s,date(2050,month,day))])
