import copy
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import game_core as core
import town
import world_loop
import laboratory_missions as missions
import criminal_dynamics as canon


def state():
    s=core.fresh('ivan'); town.travel(s,canon.LAB)
    for who in (*missions.OPERATIVES,'sylvanis'):
        s['world']['cast'][who].update(location=canon.LAB,journey=None,activity='Private review')
    return s


class LaboratoryMissionTests(unittest.TestCase):
    def test_chain_save_resume_and_exactly_once(self):
        s=state()
        with self.assertRaises(ValueError): missions.begin(s,'strategy')
        for key in missions.MISSIONS:
            missions.begin(s,key); missions.choose(s,0)
            with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
                path=Path(folder)/'lab.json';core.save(s,path);s=core.load(path)
            missions.choose(s,0)
            before=copy.deepcopy(s)
            with self.assertRaises(ValueError): missions.choose(s,0)
            with self.assertRaises(ValueError): missions.begin(s,key)
            self.assertEqual(s,before)
        self.assertEqual(missions.read(s)['readiness'],10)
        self.assertEqual(len(missions.read(s)['completed']),5)
        self.assertEqual(missions.read(s)['concerns'],0)

    def test_privacy_remote_and_absent_partner_guards(self):
        s=state(); missions.begin(s,'blue')
        for who in ('rei','valentina'):
            s['world']['cast'][who].update(location=canon.LAB,journey=None)
            before=copy.deepcopy(s)
            self.assertFalse(missions.private(s))
            with self.assertRaises(ValueError): missions.choose(s,0)
            self.assertEqual(s,before)
            self.assertNotIn('Confidential strategy',canon.context('sylvanis',['ivan'],s))
            s['world']['cast'][who]['location']='square'
        s['world']['cast']['martos']['location']='square'
        with self.assertRaises(ValueError): missions.choose(s,0)
        s['world']['cast']['martos']['location']=canon.LAB
        s['world']['location']='square'
        with self.assertRaises(ValueError): missions.choose(s,0)
        s['world']['location']=canon.LAB
        s['world']['npcs']=['Nessa Quinn']
        with self.assertRaises(ValueError): missions.choose(s,0)
        self.assertNotIn('betray',canon.laboratory_briefing(s))

    def test_jack_gets_no_missions_or_private_history(self):
        s=state(); missions.begin(s,'blue'); missions.choose(s,0); missions.choose(s,1)
        self.assertTrue(missions.context(s,'martos',['ivan']))
        self.assertFalse(missions.context(s,'elias',['ivan']))
        self.assertFalse(missions.context(s,'martos',['ivan','rei']))
        s['player']='rei';s['world']['cast']['rei'].update(location=canon.LAB,journey=None)
        s.setdefault('job_apps',{})['membership']=dict(faction='Syndicate',branch='Spades',rank=6,strikes=0)
        self.assertTrue(canon.lab_access('rei',s))
        self.assertFalse(missions.private(s))
        with self.assertRaises(ValueError): missions.begin(s,'red')
        self.assertNotIn('betray',canon.laboratory_briefing(s))

    def test_bad_choices_abandon_and_ace_participation(self):
        s=state();missions.begin(s,'red')
        before=copy.deepcopy(s)
        for choice in (True,-1,2,'0'):
            with self.assertRaises(ValueError):missions.choose(s,choice)
        self.assertEqual(s,before)
        missions.choose(s,1);missions.abandon(s)
        self.assertEqual(missions.read(s)['readiness'],0)
        missions.begin(s,'red');missions.choose(s,1);missions.choose(s,1)
        self.assertEqual(missions.read(s)['concerns'],2)
        for who,key in (('martos','blue'),('mavis','red'),('camila','blue'),('elias','red')):
            s=state();s['player']=who
            missions.begin(s,key);missions.choose(s,0);missions.choose(s,0)
            self.assertIn(key,missions.read(s)['completed'])

    def test_schedule_and_old_save_read_only(self):
        s=state();before=copy.deepcopy(s)
        missions.read(s);missions.private(s);missions.context(s,'martos',['ivan'])
        self.assertEqual(s,before)
        s['world']['minute']=17*60
        for who in missions.OPERATIVES:
            self.assertEqual(world_loop.appointment(who,17*60)[1],canon.LAB)
        s['world']['cast']['martos']['location']='square'
        with patch('autonomy.control',return_value=False),patch('autonomy.tick'):
            world_loop.advance(s,1)
        self.assertEqual(s['world']['cast']['martos']['location'],canon.LAB)
