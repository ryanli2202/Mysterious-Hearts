"""Persistence defaults and information boundaries for MH-007 presentation."""
import copy
import json
import unittest
from unittest.mock import patch
import game_core as core
import combat
import combat_engine as engine
import combat_rpg_ui as rpg


class RPGPresentationTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('ivan'); self.s['world']['location']='park'
        for who in ('ivan','sylvanis'): self.s['world']['cast'][who].update(location='park',journey=None)
        with patch.object(combat,'consent',return_value=(True,'')):
            self.f=combat.start(self.s,'sylvanis','challenge')
        engine.ensure_arena(self.f)

    def test_legacy_preferences_do_not_mutate_story(self):
        before=copy.deepcopy(self.s)
        self.assertEqual(rpg.preferences(self.s)['favourites'],[])
        self.assertEqual(before,self.s)
        self.s['combat']['ui_preferences']={'ivan':{'text_size':'invalid','favourites':'bad','density':'bad'}}
        self.assertEqual(rpg.preferences(self.s)['text_size'],10)
        self.assertEqual(rpg.preferences(self.s)['density'],'Detailed')
        self.assertEqual(rpg.preferences(self.s)['favourites'],[])

    def test_preferences_are_protagonist_scoped_and_serializable(self):
        self.s['combat']['ui_preferences']={'ivan':{'favourites':['utility:recover'],'text_size':14,'hints_dismissed':True}}
        restored=json.loads(json.dumps(self.s))
        self.assertEqual(rpg.preferences(restored)['favourites'],['utility:recover'])
        restored['player']='rei'
        self.assertEqual(rpg.preferences(restored)['favourites'],[])

    def test_opponent_inspection_only_lists_observed_moves(self):
        text=rpg.inspection(self.s,self.f,'enemy')
        self.assertIn('No techniques observed',text)
        self.assertNotIn('Crazed Demon',text)
        self.assertNotIn('Shadow Requiem',text)
        result=engine.resolve(self.s,engine.request(self.s,'utility:guard'))
        move=next(r for r in result['records'] if r['side']=='enemy')['move']
        self.assertIn(move,rpg.inspection(self.s,self.f,'enemy'))

    def test_breakdown_uses_recorded_data_and_supports_old_exchanges(self):
        self.assertIn('No exchange',rpg.breakdown(self.f))
        before=rpg.resource_snapshot(self.f)
        result=engine.resolve(self.s,engine.request(self.s,'utility:guard'))
        self.assertIn('older exchange',rpg.breakdown(self.f))
        self.f['exchanges'][-1]['ui_resource_audit']={'before':before,'after':rpg.resource_snapshot(self.f)}
        text=rpg.breakdown(self.f)
        self.assertIn('net exchange changes',text)
        for record in result['records']: self.assertIn(str(record['damage'])+' damage',text)
        self.assertIn(f"Health: {before['player']['health']} → {self.f['player']['health']}",text)
        self.f['support_exchanges']=[dict(turn=result['turn'],records=[dict(name='Partner',move='Observed strike',outcome='landed',damage=5)])]
        self.assertIn('Partner · Observed strike · landed · 5 damage',rpg.breakdown(self.f))
        self.f['support_exchanges'][0]['turn']=-1
        self.assertNotIn('FIELD PARTNER',rpg.breakdown(self.f))


if __name__=='__main__': unittest.main()
