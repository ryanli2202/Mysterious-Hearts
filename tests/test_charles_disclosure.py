import unittest
import json
import game_core as core
import charles_disclosure as report
import charles_han, charles_quest, phone_numbers, hidden_cast, messaging, groups, world_loop

def meet(s,who,venue):
    w=s['world'];w['location']=venue;w['party']=[];w['npcs']=[]
    for key,a in w['cast'].items():
        if key in (who,s['player']):a.update(location=venue,journey=None,activity='Talking')
        elif key!='charles':a.update(location='square',journey=None,activity='Relaxing')

class DisclosureTests(unittest.TestCase):
    def test_direct_number_permission_and_group_privacy(self):
        s=core.fresh('garrett')
        self.assertFalse(charles_han.number_allowed(s))
        self.assertTrue(charles_han.number_allowed(s,'sylvanis'))
        with self.assertRaises(ValueError):phone_numbers.add(s,phone_numbers.NUMBERS['charles'])
        s['charles_quest']=dict(charles_quest.read(s),step=10)
        self.assertTrue(hidden_cast.contact(s,'charles'))
        self.assertTrue(phone_numbers.saved_number(s,'charles'))
        messaging.send(s,'charles','I made it home.')
        self.assertNotIn('charles',phone_numbers.context(s,['charles','ivan']))
        with self.assertRaises(ValueError):groups.create_text(s,'Family',['charles','ivan'])
        self.assertFalse(charles_han.number_allowed(s,'ivan'))
        patron=core.fresh('sylvanis')
        self.assertTrue(hidden_cast.known(patron,'charles'))
        self.assertTrue(phone_numbers.saved_number(patron,'charles'))
        messaging.send(patron,'charles','Please review the file.')

    def test_report_reunion_and_saved_response(self):
        s=core.fresh('ivan')
        with self.assertRaises(ValueError):report.act(s)
        meet(s,'charles',report.LAB);hidden_cast.mark_met(s,'charles')
        meet(s,'garrett','park');self.assertIn('saw him yourself',report.act(s))
        self.assertEqual(report.read(s)['stage'],1)
        self.assertFalse(charles_han.number_allowed(s,'garrett'))
        meet(s,'charles',report.LAB);report.act(s)
        meet(s,'garrett','park');report.act(s)
        s=json.loads(json.dumps(s))
        self.assertTrue(charles_quest.guest(s,'garrett'))
        self.assertFalse(charles_quest.reunited(s))
        s['world']['minute']=report.read(s)['due']
        # Real travel, then actual private minutes; eyewitness remains outside.
        report.hold(s)
        self.assertTrue(s['world']['cast']['garrett']['journey'] or s['world']['cast']['garrett']['location']==report.LAB)
        world_loop.advance(s,90)
        self.assertEqual(report.read(s)['stage'],4)
        self.assertTrue(charles_han.number_allowed(s,'garrett'))
        self.assertFalse(hidden_cast.contact(s,'charles'))
        self.assertIsNone(phone_numbers.saved_number(s,'charles'))
        meet(s,'garrett','park');self.assertIn('I saw him',report.act(s))
        self.assertEqual(report.read(s)['stage'],5)
        with self.assertRaises(ValueError):report.act(s)
        import conversation_lore
        self.assertIn('met privately',conversation_lore.charles_context(s,'garrett',2))

    def test_bystander_and_appointment_privacy(self):
        s=core.fresh('ivan');meet(s,'charles',report.LAB);hidden_cast.mark_met(s,'charles')
        meet(s,'garrett','park');s['world']['cast']['rei']['location']='park'
        with self.assertRaises(ValueError):report.act(s)
        self.assertFalse(report.read(s))
        s['charles_disclosure']=dict(stage=3,journal=[],reporter='ivan',due=1200)
        s['world']['minute']=1200;meet(s,'garrett',report.LAB)
        self.assertTrue(report.hold(s));self.assertNotIn('started',report.read(s))
        s['world']['location']='park';s['world']['cast']['ivan']['location']='park'
        report.hold(s);s['world']['minute']+=19;report.hold(s)
        self.assertEqual(report.read(s)['stage'],3)
        s['world']['cast']['rei']['location']=report.LAB;report.hold(s)
        self.assertNotIn('started',report.read(s))
