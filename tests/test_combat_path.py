import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import combat
import combat_path as path
from combat_profiles import make, profile, RATINGS
import game_core as core


class PathTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('garrett')
        for who in ('garrett','rei','ivan'):
            self.s['world']['cast'][who].update(location='iron_circle',journey=None)
        self.s['world']['location']='iron_circle'

    def use_profile(self,p):
        p['name']='Test protagonist'
        combat.ensure(self.s)['profiles']['garrett']=p
        profile(self.s,'garrett')
        return p

    def finish_encounter(self,uses=0,enemy_uses=0,turns=4,damage=20,knocked=None):
        f=combat.start(self.s,'rei','challenge')
        f.update(turn=turns,score=[damage,0]); f['player']['trait_uses']=uses; f['enemy']['trait_uses']=enemy_uses
        combat.finish(self.s,'Practice concluded',knocked)
        saved=copy.deepcopy(f); combat.close(self.s)
        return saved

    def card(self,who='garrett'):
        p=profile(self.s,who)
        return dict(name='Refined manifestation',trait_name=p['trait']['name'],description='Extend the established Trait into a controlled defensive mantle.',
                    limitations='Requires concentration and finite mana; no automatic evasion.',expression='defence')

    def ready(self,stage=path.TOTALITY,refinement=93,who='garrett'):
        p=profile(self.s,who); p['path'].update(stage=stage,entered=self.s['world']['minute'])
        p['stats']['trait_refinement']=refinement
        self.s['world']['minute']+=path.MONTH
        return p

    def test_cast_seeding_and_ratings_unchanged(self):
        for who,ratings in RATINGS.items():
            p=profile(self.s,who)
            self.assertEqual(tuple(p['stats'].values()),ratings)
            self.assertEqual(p['path']['stage'],path.CAST_STAGES[who])
        self.assertEqual(profile(self.s,'sophie')['path']['stage'],path.DORMANCY)
        self.assertEqual(make('custom',{'awakened':True})['path']['stage'],path.AWAKENING)
        self.assertEqual(profile(self.s,'ivan')['path']['stage'],path.TOTALITY)

    def test_legacy_migration_preserves_training_and_starts_clock_now(self):
        p=profile(self.s,'rei'); p.pop('path'); p['stats']['trait_refinement']=99
        self.s['combat'].pop('path_epoch'); self.s['world']['minute']=100000
        before=copy.deepcopy(p['stats']); combat.ensure(self.s)
        self.assertEqual(p['stats'],before)
        self.assertEqual(p['path']['entered'],100000)
        combat.ensure(self.s); self.assertEqual(p['stats'],before)
        self.assertFalse(path.readiness(self.s,'rei')[0])

    def test_dormancy_awakens_after_real_exertion_without_inventing_trait(self):
        p=self.use_profile(make('custom'))
        for _ in range(29): self.finish_encounter()
        self.assertFalse(p['awakened'])
        self.finish_encounter()
        self.assertTrue(p['awakened']); self.assertEqual(p['path']['stage'],path.AWAKENING)
        self.assertEqual(p['stats']['awakened_power'],18); self.assertIsNone(p['trait'])
        self.assertEqual(p['stats']['martial_skill'],13)

    def test_no_mana_cannot_awaken(self):
        p=self.use_profile(make('custom',{'mana_potential':False}))
        p['path']['stage_encounters']=100
        self.assertIsNone(path.advance_early(p,100)); self.assertFalse(p['awakened'])

    def test_fixed_potency_and_trait_usage_progression(self):
        p=self.use_profile(make('custom',{'awakened':True,'awakening_trait':'Spark','awakening_description':'Short-range sparks.'}))
        power=p['stats']['awakened_power']; refinement=p['stats']['trait_refinement']
        self.finish_encounter(uses=3); self.assertEqual(p['stats']['trait_refinement'],refinement)
        self.finish_encounter(uses=1); self.assertEqual(p['stats']['trait_refinement'],refinement+1)
        self.assertEqual(p['stats']['awakened_power'],power)
        before=copy.deepcopy(p)
        with self.assertRaises(ValueError): combat.train(self.s,'Awakened power')
        self.assertEqual(p,before)

    def test_ascension_and_totality_gates_and_boosts(self):
        p=self.use_profile(make('custom',{'awakened':True,'awakening_trait':'Spark','awakening_description':'Short-range sparks.'}))
        p['path']['stage_encounters']=14; p['stats']['trait_refinement']=39
        self.finish_encounter(); self.assertEqual(p['path']['stage'],path.AWAKENING)
        with patch('world_loop.advance'): combat.train(self.s,'Trait refinement')
        self.assertEqual(p['path']['stage'],path.ASCENSION); self.assertEqual(p['stats']['awakened_power'],26)
        self.finish_encounter(); self.assertEqual(p['stats']['awakened_power'],27)
        p['path']['stage_encounters']=39; p['stats']['trait_refinement']=80
        self.finish_encounter(); self.assertEqual(p['path']['stage'],path.TOTALITY)
        self.assertEqual(p['stats']['awakened_power'],38)
        self.finish_encounter(); self.assertEqual(p['stats']['awakened_power'],38)

    def test_traitless_can_reach_totality_but_not_transcend(self):
        p=self.use_profile(make('custom',{'awakened':True}))
        p['path']['stage_encounters']=15; path.advance_early(p,100)
        p['path']['stage_encounters']=40; path.advance_early(p,200)
        self.assertEqual(p['path']['stage'],path.TOTALITY)
        self.s['world']['minute']+=path.MONTH
        self.assertFalse(path.readiness(self.s)[0])

    def test_no_farming_immediate_concessions_or_empty_guard_sessions(self):
        p=profile(self.s,'garrett'); before=p['path']['encounters']
        self.finish_encounter(turns=0,damage=0,uses=100)
        self.finish_encounter(turns=30,damage=0)
        self.finish_encounter(turns=1,damage=50)
        self.assertEqual(p['path']['encounters'],before)

    def test_one_exchange_knockout_counts_and_finish_is_idempotent(self):
        f=combat.start(self.s,'rei','challenge'); f.update(turn=1,score=[300,0])
        combat.finish(self.s,'Victory','rei'); p=profile(self.s,'garrett'); before=copy.deepcopy(p)
        combat.finish(self.s,'Victory','rei'); self.assertEqual(p,before)
        self.assertEqual(p['path']['encounters'],1)

    def test_npc_earns_same_progression(self):
        p=profile(self.s,'rei'); before=p['stats']['trait_refinement']
        self.finish_encounter(enemy_uses=4)
        self.assertEqual(p['stats']['trait_refinement'],before+1)
        self.assertEqual(p['path']['encounters'],1)

    def test_breakthrough_exact_age_and_refinement_boundaries(self):
        p=self.ready(refinement=92)
        self.assertFalse(path.readiness(self.s)[0]); p['stats']['trait_refinement']=93
        self.s['world']['minute']-=1; self.assertFalse(path.readiness(self.s)[0])
        self.s['world']['minute']+=1; self.assertTrue(path.readiness(self.s)[0])

    def test_generated_breakthrough_stage_two_and_no_double_commit(self):
        p=self.ready()
        with patch.object(combat,'ask_ai',return_value=self.card()): result=path.generate_breakthrough(self.s)
        before=copy.deepcopy(p); self.assertEqual(p,before)
        path.commit_breakthrough(self.s,result)
        self.assertEqual(p['path']['stage'],path.TRANSCENDENCE_1)
        self.assertEqual(p['form'],'Refined manifestation')
        with self.assertRaises(ValueError): path.commit_breakthrough(self.s,result)
        self.assertFalse(path.readiness(self.s)[0])
        p['stats']['trait_refinement']=100; self.s['world']['minute']+=path.MONTH
        with patch.object(combat,'ask_ai',return_value=self.card()): result=path.generate_breakthrough(self.s)
        path.commit_breakthrough(self.s,result)
        self.assertEqual(p['path']['stage'],path.TRANSCENDENCE_2)
        self.assertFalse(path.readiness(self.s)[0])

    def test_invalid_ai_failure_and_stale_response_are_atomic(self):
        p=self.ready(); before=copy.deepcopy(p)
        with patch.object(combat,'ask_ai',return_value={'name':'Omnipotence'}):
            with self.assertRaises(ValueError): path.generate_breakthrough(self.s)
        self.assertEqual(p,before)
        with patch.object(combat,'ask_ai',return_value=self.card()): result=path.generate_breakthrough(self.s)
        p['trait']['description']='Changed limits'; before=copy.deepcopy(p)
        with self.assertRaises(ValueError): path.commit_breakthrough(self.s,result)
        self.assertEqual(p,before)

    def test_npc_breakthrough_requires_presence_and_trust(self):
        p=self.ready(who='rei')
        with patch.object(combat,'ask_ai',return_value=self.card('rei')): result=path.generate_breakthrough(self.s,'rei')
        self.s['world']['cast']['rei']['location']='cafe'
        with self.assertRaises(ValueError): path.commit_breakthrough(self.s,result)
        self.s['world']['cast']['rei']['location']='iron_circle'
        path.commit_breakthrough(self.s,result)
        self.assertEqual(p['path']['stage'],path.TRANSCENDENCE_1)

    def test_transcendent_form_cost_upkeep_expiry_and_energy_failure(self):
        f=combat.start(self.s,'rei','challenge'); energy=f['player']['energy']
        combat.activate_form(self.s); self.assertEqual(f['player']['energy'],energy-35)
        self.assertEqual(f['player']['form_until'],180)
        path.upkeep(f); self.assertEqual(f['player']['energy'],energy-43)
        f['player']['energy']=7; path.upkeep(f)
        self.assertEqual(f['player']['form_until'],f['elapsed'])
        with self.assertRaises(ValueError): combat.activate_form(self.s)

    def test_trait_use_only_counts_when_paid_and_executable(self):
        import random
        p=make('garrett'); q=make('rei'); r=combat.resources(p); t=combat.resources(q)
        r['energy']=0
        combat.strike(p,q,r,t,'Trait','Sanda',10,0,random.Random(1),0)
        self.assertEqual(r['trait_uses'],0)
        r['energy']=100
        combat.strike(p,q,r,t,'Trait','Sanda',100,0,random.Random(1),0)
        self.assertEqual(r['trait_uses'],0)
        combat.strike(p,q,r,t,'Trait','Sanda',20,0,random.Random(1),0)
        self.assertEqual(r['trait_uses'],1)

    def test_save_load_stage_clock_and_generated_card(self):
        p=self.ready()
        with patch.object(combat,'ask_ai',return_value=self.card()): result=path.generate_breakthrough(self.s)
        path.commit_breakthrough(self.s,result)
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)/'path.json'; core.save(self.s,dest); restored=core.load(dest)
        self.assertEqual(profile(restored,'garrett')['path'],p['path'])
        self.assertFalse(path.readiness(restored)[0])

if __name__=='__main__': unittest.main()
