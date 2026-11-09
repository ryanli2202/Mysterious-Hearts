import unittest
import game_core as core
import messaging
import phone_personalization as personal
from phone_chat import inbox_sort_key, inbox_time, latest_message_minute

class InboxOrderTests(unittest.TestCase):
    def test_latest_time_and_unknown_history(self):
        self.assertEqual(inbox_time(0, 0), '12:00 AM')
        self.assertEqual(inbox_time(12*60+5, 800), '12:05 PM')
        self.assertEqual(inbox_time(1439, 1440), 'Yesterday\n11:59 PM')
        self.assertEqual(inbox_time(None, 1440), '')
        self.assertEqual(inbox_time(0, 3*1440), '01 Jan\n12:00 AM')
        self.assertEqual(latest_message_minute({}, [{'minute':100}, {'minute':200}]),200)
        self.assertIsNone(latest_message_minute({}, [{'earlier':True}]))

    def test_recent_then_pinned_and_same_minute(self):
        s=core.fresh('rei')
        s['world']['minute']=600
        messaging.send(s,'emily','First')
        messaging.send(s,'sophie','Second')
        rows=[(k,False,s['routes'][k],k) for k in ('emily','sophie')]
        records=personal.records(s)
        ordered=lambda pins: [r[0] for r in sorted(rows,key=lambda r:inbox_sort_key(r,records,pins))]
        self.assertEqual(ordered([]),['sophie','emily'])
        self.assertEqual(ordered(['route:emily']),['emily','sophie'])
        messaging.send(s,'emily','Newest')
        self.assertEqual(ordered([]),['emily','sophie'])

    def test_legacy_timestamps_and_groups(self):
        rows=[('old',False,{},'A'),('new',True,{},'Z'),('empty',False,{},'B')]
        records=[dict(who='old',group=False,minute=100),dict(who='new',group=True,minute=200)]
        self.assertEqual([r[0] for r in sorted(rows,key=lambda r:inbox_sort_key(r,records,[]))],['new','old','empty'])

if __name__=='__main__': unittest.main()
