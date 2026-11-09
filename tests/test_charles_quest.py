import copy
import json
import tempfile
from pathlib import Path
import unittest
import game_core as core
import charles_quest as quest
import town,hidden_cast,phone_numbers,criminal_dynamics,groups,messaging


def arrive(s,index,day=None):
    s['world']['minute']=(day if day is not None else index+2)*1440+20*60
    place=quest.STEPS[index][1]
    s['world']['location']=place
    s['world']['cast']['garrett'].update(location=place,journey=None,activity='Investigating')
    s['world']['party']=[];s['world']['npcs']=[]
    for who,a in s['world']['cast'].items():
        if who not in ('garrett','charles') and a['location']==quest.LAB:a['location']='square'


class CharlesQuestTests(unittest.TestCase):
    def test_full_chain_both_endings_and_saved_resume(self):
        for ending in (0,1):
            s=core.fresh('garrett')
            self.assertFalse(criminal_dynamics.lab_access('garrett',s))
            for i in range(len(quest.STEPS)):
                arrive(s,i);quest.advance(s,ending if i==10 else 0)
                with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
                    p=Path(folder)/'quest.json';core.save(s,p);s=core.load(p)
                if i<8:self.assertFalse(criminal_dynamics.lab_access('garrett',s))
            self.assertEqual(quest.read(s)['ending'],('quiet alliance','guarded reconciliation')[ending])
            self.assertTrue(quest.reunited(s));self.assertTrue(hidden_cast.known(s,'charles'))
            import conversation_lore
            conversation_lore.check_reply(s,'garrett','Charles?', 'Charles went undercover.')
            with self.assertRaises(ValueError):conversation_lore.check_reply(s,'garrett','Charles?', 'Charles is dead.')
            self.assertTrue(hidden_cast.contact(s,'charles'))
            self.assertFalse(criminal_dynamics.research_access('garrett',s))
            with self.assertRaises(ValueError):criminal_dynamics.laboratory_briefing(s)
            bond=copy.deepcopy(s['friendships']['charles'])
            with self.assertRaises(ValueError):quest.advance(s,0)
            self.assertEqual(s['friendships']['charles'],bond)
            arrive(s,0,20);quest.check_in(s)
            with self.assertRaises(ValueError):quest.check_in(s)
            self.assertIn('undercover',quest.knowledge(s,'charles',['garrett']))
            self.assertNotIn('discussed Charles’s undercover',quest.knowledge(s,'garrett',['ivan']))

    def test_legacy_projection_read_only_and_setback_recovery(self):
        for old,count,expected in [('unopened',0,0),('slip',0,1),('traced',0,2),('traced',3,5)]:
            s=core.fresh('garrett');s['charles_lead']=old
            s['living_world']={'mystery':[{'day':i} for i in range(count)]}
            before=copy.deepcopy(s);self.assertEqual(quest.read(s)['step'],expected);self.assertEqual(s,before)
        arrive(s,5,10);quest.advance(s,1)
        self.assertEqual(quest.read(s)['step'],5)
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError):quest.advance(s,0)
        self.assertEqual(before,s)
        arrive(s,5,11);quest.advance(s,0);self.assertEqual(quest.read(s)['step'],6)

    def test_physical_and_private_reunion_gates(self):
        s=core.fresh('garrett');before=copy.deepcopy(s)
        with self.assertRaises(ValueError):quest.advance(s,0)
        self.assertEqual(before,s)
        s['charles_quest']=dict(quest.read(s),step=9)
        arrive(s,9);s['world']['minute']=18*60
        with self.assertRaises(ValueError):quest.advance(s,0)
        arrive(s,9);s['world']['cast']['ivan']['location']=quest.LAB
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError):quest.advance(s,0)
        self.assertEqual(before,s)
        s['world']['cast']['ivan']['location']='square';quest.advance(s,0)
        self.assertTrue(quest.reunited(s))
        s['player']='ivan'
        self.assertFalse(quest.reunited(s));self.assertFalse(quest.guest(s,'garrett'))
        with self.assertRaises(ValueError):quest.advance(s,0)

    def test_genuine_early_lab_encounter(self):
        s=core.fresh('garrett');arrive(s,9)
        with self.assertRaises(ValueError):quest.recognise(s)
        s.setdefault('job_apps',{})['membership']=dict(faction='Syndicate',branch='Clubs',rank=6,strikes=0)
        quest.recognise(s)
        self.assertEqual(quest.read(s)['step'],9)
        self.assertEqual(len(quest.read(s)['evidence']),1)
        quest.advance(s,0)
        self.assertTrue(quest.reunited(s))

    def test_no_number_in_old_or_new_saves_or_groups(self):
        s=core.fresh('ivan');town.travel(s,quest.LAB);town.meet(s,'charles');town.end_hangouts(s)
        old='12025550186'
        s['phone_numbers']={'directory':{'charles':old},'contacts':{'charles':{'number':old}}}
        with self.assertRaises(ValueError):phone_numbers.add(s,old)
        phone_numbers.ensure(s)
        self.assertIn('charles',phone_numbers.NUMBERS)
        self.assertNotIn('charles',s['phone_numbers']['directory'])
        self.assertFalse(hidden_cast.contact(s,'charles'));self.assertIsNone(phone_numbers.saved_number(s,'charles'))
        with self.assertRaises(ValueError):phone_numbers.number(s,'charles')
        with self.assertRaises(ValueError):groups.create_text(s,'Old contacts',['charles','garrett'])
        with self.assertRaises(ValueError):messaging.send(s,'charles','hello')
        self.assertFalse(messaging.available(s,'charles'))
