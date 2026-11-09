import copy
import json
import random
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
import combat as c
from combat_profiles import profile, make, TEACHERS, ARTS
import game_core as core
import world_loop


class CombatTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('garrett')
        self.s['world']['location']='iron_circle'
        for who in ('garrett','rei','sylvanis','takeo','ivan','mavis','emily'):
            self.s['world']['cast'][who].update(location='iron_circle',journey=None)

    def judgement(self,f,**kw):
        plan,_=c.tactics.prepare(self.s)
        j=dict(player_feasible=True,complexity=10,advantage=0,enemy_mode=plan['mode'],enemy_art=plan['art'],enemy_action=plan['action'],reason='The known technique is plausible.')
        j.update(kw)
        return dict(fight_id=f['id'],turn=f['turn'],action='Strike then cover.',style='Sanda',mode='Martial',judgement=j)

    def test_peak_profiles_and_teacher_map(self):
        self.assertEqual(list(make('sylvanis')['stats'].values()),[90,100,100,100])
        self.assertEqual(list(make('takeo')['stats'].values()),[100,80,95,90])
        self.assertEqual(list(make('crow')['stats'].values()),[80,100,100,100])
        self.assertEqual(set(TEACHERS['sylvanis']),set(ARTS))
        self.assertNotIn('takeo',TEACHERS); self.assertNotIn('crow',TEACHERS)
        self.assertTrue(make('emily')['trait']); self.assertTrue(make('garrett')['form'])
        self.assertIn('Shinigami Protocol',make('neo')['abilities'])
        for who,arts in TEACHERS.items():
            for art in arts:
                if art!='Combat analysis': self.assertIn(art,make(who)['arts'])

    def test_custom_starts_low(self):
        a=make('custom',{'awakened':False}); b=make('custom',{'awakened':True,'awakening_trait':'Spark','awakening_description':'A small spark.'})
        self.assertFalse(a['awakened']); self.assertEqual(a['stats']['awakened_power'],0)
        self.assertLess(a['stats']['martial_skill'],b['stats']['martial_skill'])
        self.assertLess(b['stats']['awakened_power'],25)

    def test_ledger_presence_schedule_and_tiers(self):
        self.s['world']['location']='cafe'
        with self.assertRaises(ValueError): c.sign_ledger(self.s,'Garrett')
        self.s['world']['location']='iron_circle'; c.sign_ledger(self.s,'Garrett')
        ledger=c.ensure(self.s)['ledger']; self.assertEqual(ledger['rank'],450)
        self.assertFalse(c.card_ready(self.s)); self.s['world']['minute']=ledger['next']; self.assertTrue(c.card_ready(self.s))
        for rank,awakened,trait in ((450,False,False),(200,True,False),(20,True,True)):
            ledger['rank']=rank
            p=c.validate_opponent(self.s,dict(name='Ari Vale',art='Boxing',trait='Spark',limitations='Short-range sparks only.'))
            self.assertEqual(p['awakened'],awakened); self.assertEqual(bool(p['trait']),trait)
        self.s['world']['minute']+=181
        self.assertFalse(c.card_ready(self.s)); self.assertEqual(ledger['missed'],1)

    def test_consent_and_remote_attack(self):
        with self.assertRaises(ValueError): c.start(self.s,'emily','challenge')
        self.s['world']['cast']['rei']['location']='cafe'
        with self.assertRaises(ValueError): c.start(self.s,'rei','attack')
        self.assertFalse(c.ensure(self.s)['ruptures'])

    def test_attack_permanent_rupture_and_friends(self):
        c.start(self.s,'rei','attack')
        self.assertIn('rei',c.ensure(self.s)['ruptures'])
        import relationship_dynamics
        relationship_dynamics.stats(self.s,'rei')['trust']=100
        c.enforce(self.s); self.assertEqual(relationship_dynamics.stats(self.s,'rei')['trust'],0)
        self.assertFalse(relationship_dynamics.repair_ready(self.s,'rei'))

    def test_expulsion_and_diplomacy(self):
        self.s['job_apps']={'membership':dict(faction='Shinokami',rank=1),'gang':None}
        c.start(self.s,'takeo','attack')
        self.assertIn('shinokami',c.ensure(self.s)['expelled'])
        self.assertIsNone(self.s['job_apps'].get('membership'))
        c.concede(self.s); c.close(self.s)
        self.s['job_apps']['membership']=dict(faction='Shinokami',rank=1)
        c.start(self.s,'mavis','attack')
        self.assertEqual(c.ensure(self.s)['diplomacy']['shinokami|syndicate'],25)

    def test_canonical_command_expulsion_survives_job_sync(self):
        import job_apps, hidden_cast, crime_diplomacy
        s=core.fresh('ivan'); job_apps.ensure(s)
        s['world']['location']='syndicate_hq'
        for who in ('ivan','crow'): s['world']['cast'][who].update(location='syndicate_hq',journey=None)
        self.assertEqual(c.affiliation(s,'ivan'),('syndicate',90))
        c.start(s,'crow','attack'); job_apps.ensure(s)
        self.assertFalse(hidden_cast.hq_access(s,'ivan'))
        self.assertIsNone(crime_diplomacy.mandate(s))
        self.assertFalse(s['job_apps'].get('story_membership'))

    def test_training_presence_and_limits(self):
        p=profile(self.s,'garrett')
        with patch.object(world_loop,'advance'):
            c.train(self.s,'Judo','rei'); self.assertEqual(p['arts']['Judo'],3)
            c.train(self.s,'Judo'); c.train(self.s,'Combat analysis')
            with self.assertRaises(ValueError): c.train(self.s,'Judo')
        with self.assertRaises(ValueError): c.train(self.s,'Boxing','takeo')

    def test_turns_save_roundtrip_and_stale_rejection(self):
        f=c.start(self.s,'rei','challenge'); result=self.judgement(f)
        c.commit_turn(self.s,result)
        self.assertEqual(f['elapsed'],30)
        with self.assertRaises(ValueError): c.commit_turn(self.s,result)
        restored=json.loads(json.dumps(self.s)); self.assertEqual(c.active(restored)['id'],f['id'])
        c.commit_turn(restored,self.judgement(c.active(restored)))
        self.assertEqual(c.active(restored)['turn'],2)

    def test_real_save_load_resumes_encounter(self):
        f=c.start(self.s,'rei','challenge'); c.commit_turn(self.s,self.judgement(f))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'combat-save.json'; core.save(self.s,path); restored=core.load(path)
        self.assertEqual(c.active(restored)['id'],f['id'])
        self.assertEqual(c.active(restored)['player'],f['player'])
        c.commit_turn(restored,self.judgement(c.active(restored)))
        self.assertEqual(c.active(restored)['turn'],2)

    def test_impossible_moves_and_resource_gate(self):
        p=make('garrett'); q=make('rei'); r=c.resources(p); t=c.resources(q)
        r['energy']=0
        damage,_=c.strike(p,q,r,t,'Trait','Sanda',20,0,random.Random(1),0)
        self.assertEqual(damage,0); self.assertEqual(t['health'],t['max_health'])
        f=c.start(self.s,'rei','challenge'); health=f['enemy']['health']
        c.commit_turn(self.s,self.judgement(f,player_feasible=False))
        self.assertEqual(f['enemy']['health'],health)

    def test_knockout_recovery_blocks_activity(self):
        c.start(self.s,'rei','challenge'); c.finish(self.s,'Defeat',self.s['player']); c.close(self.s)
        self.assertEqual(c.recovering(self.s),1440)
        with self.assertRaises(ValueError): c.train(self.s,'Sanda')
        with self.assertRaises(ValueError): world_loop.start_trip(self.s,'garrett','cafe')
        self.s['world']['minute']+=1440; self.assertEqual(c.recovering(self.s),0)

    def test_npc_knockout_cannot_be_attacked(self):
        c.start(self.s,'rei','challenge'); c.finish(self.s,'Victory','rei'); c.close(self.s)
        with self.assertRaises(ValueError): c.start(self.s,'rei','attack')
        self.assertFalse(world_loop.together(self.s,'rei'))

    def test_spar_has_no_winner(self):
        c.start(self.s,'rei','spar'); c.finish(self.s,'Victory','rei')
        self.assertEqual(c.active(self.s)['result'],'Practice complete — no winner or loser.')

    def test_circle_three_rounds(self):
        c.sign_ledger(self.s,'Garrett'); ledger=c.ensure(self.s)['ledger']; self.s['world']['minute']=ledger['next']
        f=c.start(self.s,'generated','circle',dict(name='Ari',art='Boxing',trait='',limitations=''))
        with patch.object(world_loop,'advance'), patch.object(c,'strike',return_value=(0,'guards')):
            for _ in range(30):
                result=self.judgement(f); result['mode']='Guard'; c.commit_turn(self.s,result)
        self.assertEqual(f['elapsed'],900); self.assertEqual(f['status'],'finished')
        self.assertEqual(ledger['losses'],1)

    def test_conduit_exact_duration_and_cooldown(self):
        self.s['player']='ivan'; f=c.start(self.s,'rei','challenge'); c.activate_form(self.s)
        self.assertEqual(f['player']['form_until'],300)
        c.concede(self.s); c.close(self.s); c.start(self.s,'rei','challenge')
        with self.assertRaises(ValueError): c.activate_form(self.s)

    def test_ai_invalid_response_is_atomic(self):
        c.start(self.s,'rei','challenge'); before=copy.deepcopy(self.s)
        with patch.object(c,'ask_ai',return_value={'player_feasible':'yes'}):
            with self.assertRaises(ValueError): c.adjudicate(self.s,'Strike','Sanda','Martial')
        self.assertEqual(self.s,before)

    def test_npc_proposes_not_attacks(self):
        c.observe_conversation(self.s,'rei','Want to practise martial arts and spar?')
        offers=c.pending_offers(self.s); self.assertEqual(len(offers),1)
        self.assertIsNone(c.active(self.s)); c.respond_offer(self.s,offers[0][0],True)
        self.assertEqual(c.active(self.s)['kind'],'spar')

if __name__=='__main__': unittest.main()
