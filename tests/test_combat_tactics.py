import copy
import json
import unittest
from unittest.mock import Mock, patch

import combat
import combat_path as path
import combat_tactics as tactics
import game_core as core
from combat_profiles import make, profile, RATINGS


class OpponentTacticsTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('ivan')
        self.s['world']['location']='iron_circle'
        for who in ('ivan','rei','sylvanis','garrett'):
            self.s['world']['cast'][who].update(location='iron_circle',journey=None)

    def start(self,who='sylvanis'):
        f=combat.start(self.s,who,'challenge'); f['seed']=21
        return f

    def judge(self,mode='Guard',feasible=True):
        plan,_=tactics.prepare(self.s)
        j=dict(player_feasible=feasible,complexity=20,advantage=0,enemy_mode=plan['mode'],
               enemy_art=plan['art'],enemy_action=plan['action'],reason='Both attempts remain bounded.')
        with patch.object(combat,'ask_ai',return_value=j) as request:
            result=combat.adjudicate(self.s,'Protect my head and look for an opening.','Judo',mode)
        return result,request.call_args.args[0]

    def landed_strikes(self):
        strike=combat.strike
        return patch.object(combat,'strike',side_effect=lambda *args: strike(*args[:8],Mock(random=lambda:0),*args[9:]))

    def test_opening_shadow_attack_and_form_are_known_before_player_input(self):
        f=self.start(); before=copy.deepcopy(self.s)
        plan,preview=tactics.prepare(self.s)
        self.assertEqual(plan['mode'],'Trait')
        self.assertEqual(plan['activate_form'],'Advanced form')
        self.assertIn('Umbrakinesis',plan['action'])
        self.assertIn('piercing shadow',plan['action'])
        self.assertIn(plan['art'],f['opponent_profile']['arts'])
        self.assertEqual(preview['enemy']['energy'],f['enemy']['energy']-55-12)
        self.assertEqual(preview['enemy']['active_form']['name'],'Black-eyed Shadow Dominion')
        self.assertEqual(self.s,before)
        result,prompt=self.judge()
        self.assertIn('"active_form": {"name": "Black-eyed Shadow Dominion"',prompt)
        self.assertIn('independently committed',prompt)
        self.assertEqual(result['opponent_plan'],plan)
        self.assertEqual(self.s,before)

    def test_opponent_attacks_guard_recovery_and_impossible_moves(self):
        for mode,feasible in (('Guard',True),('Recover',True),('Martial',False)):
            with self.subTest(mode=mode):
                self.setUp(); f=self.start(); before=f['enemy']['energy']
                result,_=self.judge(mode,feasible)
                with self.landed_strikes():
                    combat.commit_turn(self.s,result)
                self.assertLess(f['player']['health'],f['player']['max_health'])
                self.assertEqual(f['enemy']['trait_uses'],1)
                self.assertEqual(f['enemy']['energy'],before-55-12-tactics.trait_cost(f['opponent_profile'],60))
                self.assertTrue(any('Sylvanis [Trait' in line for line in f['log']))

    def test_known_arts_and_trait_attacks_vary_across_cast(self):
        f=self.start()
        for who in RATINGS:
            with self.subTest(who=who):
                p=make(who); f.update(opponent=who,opponent_profile=p,enemy=combat.resources(p))
                modes=set(); arts=set()
                for turn in range(9):
                    f['turn']=turn
                    plan,_=tactics.prepare(self.s)
                    modes.add(plan['mode']); arts.add(plan['art'])
                    self.assertIn(plan['art'],p['arts'] or {'Untrained':0})
                    self.assertLessEqual(plan['complexity'],p['stats']['trait_refinement'])
                self.assertIn('Martial',modes)
                self.assertEqual('Trait' in modes,bool(p['trait']))
                if len(p['arts'])>1: self.assertGreater(len(arts),1)

    def test_no_mana_uses_martial_and_exhaustion_recovers(self):
        f=self.start(); f['enemy']['energy']=0
        plan,preview=tactics.prepare(self.s)
        self.assertEqual(plan['mode'],'Martial'); self.assertIsNone(plan['activate_form'])
        result,_=self.judge(); combat.commit_turn(self.s,result)
        self.assertEqual(f['enemy']['trait_uses'],0); self.assertEqual(f['enemy']['energy'],0)
        f['enemy']['stamina']=7
        plan,_=tactics.prepare(self.s); self.assertEqual(plan['mode'],'Recover')
        result,_=self.judge(); combat.commit_turn(self.s,result)
        self.assertEqual(f['enemy']['stamina'],25); self.assertEqual(f['enemy']['energy'],10)

    def test_low_mana_refinement_and_biocreation_cost(self):
        f=self.start(); p=make('gordon'); f.update(opponent='gordon',opponent_profile=p,enemy=combat.resources(p))
        f['enemy']['energy']=15
        plan,_=tactics.prepare(self.s)
        self.assertEqual(plan['mode'],'Trait')
        self.assertLess(plan['complexity'],10)
        self.assertEqual(tactics.trait_cost(p,plan['complexity']),15)
        f['enemy']['energy']=14
        self.assertEqual(tactics.prepare(self.s)[0]['mode'],'Martial')
        p['stats']['trait_refinement']=3; f['enemy']['energy']=100
        self.assertEqual(tactics.prepare(self.s)[0]['complexity'],3)

    def test_forms_pressure_cooldown_and_no_unearned_transcendence(self):
        f=self.start('garrett')
        self.assertIsNone(tactics.prepare(self.s)[0]['activate_form'])
        combat.activate_form(self.s)
        self.assertEqual(tactics.prepare(self.s)[0]['activate_form'],'Advanced form')
        p=make('ivan'); f.update(opponent='ivan',opponent_profile=p,enemy=combat.resources(p),turn=4)
        self.s['combat']['form_cooldowns'].pop('ivan',None)
        self.assertEqual(tactics.prepare(self.s)[1]['enemy']['active_form']['name'],'Conduit State')
        self.s['combat']['form_cooldowns']['ivan']=self.s['world']['minute']+1440
        self.assertIsNone(tactics.prepare(self.s)[0]['activate_form'])
        p=make('alyssa'); f.update(opponent='alyssa',opponent_profile=p,enemy=combat.resources(p),turn=0)
        plan,_=tactics.prepare(self.s)
        self.assertIsNone(plan['activate_form']); self.assertNotIn('piercing',plan['action'])

    def test_form_upkeep_expiry_and_no_reactivation(self):
        f=self.start(); result,_=self.judge(); combat.commit_turn(self.s,result)
        self.assertTrue(f['enemy']['form_used'])
        f['enemy']['energy']=11
        plan,preview=tactics.prepare(self.s)
        self.assertIsNone(plan['activate_form'])
        self.assertEqual(preview['enemy']['form_until'],f['elapsed'])
        self.assertNotIn('second-stage',plan['action'])
        result,_=self.judge(); combat.commit_turn(self.s,result)
        self.assertEqual(f['enemy']['form_until'],f['elapsed']-30)
        f['enemy']['energy']=184; f['elapsed']=600; f['turn']=20
        self.assertIsNone(tactics.prepare(self.s)[0]['activate_form'])
        self.assertNotIn('second-stage',tactics.prepare(self.s)[0]['action'])

    def test_failed_response_retry_and_save_load_keep_same_intent(self):
        f=self.start(); before=copy.deepcopy(self.s); plan=tactics.prepare(self.s)[0]
        with patch.object(combat,'ask_ai',side_effect=ValueError('offline')):
            with self.assertRaises(ValueError): combat.adjudicate(self.s,'Guard.','Judo','Guard')
        self.assertEqual(self.s,before)
        restored=json.loads(json.dumps(self.s)); combat.ensure(restored)
        self.assertEqual(tactics.prepare(restored)[0],plan)
        # Existing active encounters need no newly saved plan field.
        self.assertNotIn('opponent_plan',f)
        result,_=self.judge(); combat.commit_turn(restored,result)
        self.assertEqual(combat.active(restored)['turn'],1)
        with self.assertRaises(ValueError): combat.commit_turn(restored,result)

    def test_changed_plan_or_resources_rejected_before_costs(self):
        self.start(); result,_=self.judge()
        result['judgement']['enemy_mode']='Guard'; before=copy.deepcopy(self.s)
        with patch.object(combat,'ask_ai',return_value=result['judgement']):
            with self.assertRaises(ValueError): combat.adjudicate(self.s,'Guard.','Judo','Guard')
        self.assertEqual(self.s,before)
        with self.assertRaises(ValueError): combat.commit_turn(self.s,result)
        self.assertEqual(self.s,before)
        result,_=self.judge(); combat.activate_form(self.s); before=copy.deepcopy(self.s)
        with self.assertRaises(ValueError): combat.commit_turn(self.s,result)
        self.assertEqual(self.s,before)

    def test_form_reserves_first_attack_and_never_activates_during_recovery(self):
        f=self.start(); f['enemy']['energy']=76
        self.assertIsNone(tactics.prepare(self.s)[0]['activate_form'])
        f['enemy']['energy']=77
        plan,preview=tactics.prepare(self.s)
        self.assertIsNotNone(plan['activate_form'])
        self.assertEqual(plan['mode'],'Trait')
        self.assertLessEqual(tactics.trait_cost(f['opponent_profile'],plan['complexity']),preview['enemy']['energy'])
        f['enemy']['stamina']=8
        plan,_=tactics.prepare(self.s)
        self.assertEqual(plan['mode'],'Recover'); self.assertIsNone(plan['activate_form'])

    def test_either_fighter_can_act_first_and_knockout_stops_reply(self):
        f=self.start(); outcomes=set()
        for seed in range(20):
            f['seed']=seed; outcomes.add(tactics.prepare(self.s)[0]['enemy_first'])
        self.assertEqual(outcomes,{False,True})
        for first in (False,True):
            with self.subTest(enemy_first=first):
                self.setUp(); f=self.start()
                f['seed']=next(seed for seed in range(100) if self.seed_first(f,seed)==first)
                f['player']['health']=1; f['enemy']['health']=1
                result,_=self.judge('Martial')
                with self.landed_strikes():
                    combat.commit_turn(self.s,result)
                self.assertEqual(f['status'],'finished')
                self.assertEqual(f['player' if first else 'enemy']['health'],0)
                self.assertEqual(f['enemy' if first else 'player']['health'],1)

    def seed_first(self,f,seed):
        f['seed']=seed
        return tactics.prepare(self.s)[0]['enemy_first']


if __name__=='__main__': unittest.main()
