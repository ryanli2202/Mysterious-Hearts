import copy
import json
import random
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import combat
import combat_engine as engine
import combat_moves as moves
import combat_workshop as workshop
from combat_profiles import make,profile,ARTS
import game_core as core


AMP=dict(name='Resonant force',description='Reinforce contact with sound vibrations.',aspect='Sound',
    role='Contact force and accuracy',tags=['breach','precision'],compatible=list(moves.ROLES),mana=8,
    environment='Vibrations crack contacted cover.')


def custom_state():
    s=core.fresh('garrett'); p=profile(s,'garrett')
    p.update(trait=dict(name='Resonance',description='Shapes nearby sound through vibration.',effect='custom'),
             stats=dict(awakened_power=18,trait_refinement=0,martial_skill=12,fight_iq=14),arts={})
    p['moveset']=dict(version=1,learned=[],arts=[],amplifications=workshop.validate_amplifications([AMP]),unique=[])
    return s


def candidates(s):
    amp=profile(s,s['player'])['moveset']['amplifications'][0]['id']
    return [dict(name='Echo '+str(i),description='A controlled burst of sound reinforces a short strike '+str(i)+'.',
        role='attack',tags=['precision','breach'],aspects=[amp],range=2,stamina=9,mana=12,hits=1,
        environment='Cracks nearby cover on impact.',setup='None',counter='Evasion or guard contests the strike.') for i in range(3)]


class CatalogueTests(unittest.TestCase):
    def test_complete_catalogues_and_ids(self):
        self.assertEqual(len(moves.MOVES),432)
        self.assertEqual({x['art'] for x in moves.MOVES.values()},set(ARTS))
        self.assertEqual(len(moves.CAST),33)
        self.assertEqual(sum(map(len,moves.AMPLIFICATIONS.values())),58)
        self.assertEqual(sum(len(x) for k,x in moves.UNIQUES.items() if moves.CAST[k]['kind']=='trait'),124)
        self.assertEqual(sum(len(x) for k,x in moves.UNIQUES.items() if moves.CAST[k]['kind']=='awakened'),15)
        all_ids=[a['id'] for group in (*moves.UNIQUES.values(),*moves.AMPLIFICATIONS.values()) for a in group]
        self.assertEqual(len(all_ids),len(set(all_ids)))

    def test_legacy_migration_does_not_grant_untrained_masters(self):
        p=make('garrett'); p.pop('moveset'); p['arts']['Judo']=3
        moves.initialise(p,'garrett')
        learned=[moves.MOVES[x] for x in p['moveset']['learned']]
        self.assertTrue(any(x['tier']=='master' for x in learned if x['art']=='Sanda'))
        self.assertEqual({x['tier'] for x in learned if x['art']=='Judo'},{'basic'})
        before=copy.deepcopy(p); moves.initialise(p,'garrett'); self.assertEqual(p,before)

    def test_learning_thresholds_and_first_lesson(self):
        s=custom_state(); p=profile(s,s['player']); s['world']['location']='iron_circle'
        s['world']['cast']['tyler'].update(location='iron_circle',journey=None)
        advanced=next(x for x in moves.MOVES.values() if x['art']=='Boxing' and x['tier']=='advanced')
        master=next(x for x in moves.MOVES.values() if x['art']=='Boxing' and x['tier']=='master')
        with patch('world_loop.advance'):
            combat.train(s,'Boxing','tyler')
            self.assertEqual(len(p['moveset']['learned']),14)
            with self.assertRaises(ValueError): moves.lesson(s,advanced['id'],'tyler')
            p['stats']['martial_skill']=60; moves.lesson(s,advanced['id'],'tyler')
            self.assertIn(advanced['id'],p['moveset']['learned'])
            p['stats']['martial_skill']=80; p['awakened']=False
            with self.assertRaises(ValueError): moves.lesson(s,master['id'],'tyler')
            p['awakened']=True; moves.lesson(s,master['id'],'tyler')
            self.assertIn(master['id'],p['moveset']['learned'])

    def test_trait_skills_have_no_stat_gate_and_no_extra_amp(self):
        for who,data in moves.CAST.items():
            p=make(who)
            if data['kind']=='dormant': self.assertFalse(moves.amps(p)); continue
            p['stats'].update(awakened_power=1,trait_refinement=0,martial_skill=0,fight_iq=0)
            for skill in moves.UNIQUES[who]:
                selected=moves.selection(p,skill['id']); self.assertTrue(moves.can_pay(combat.resources(p),selected))
                self.assertFalse(moves.amps(p,selected))
            if moves.amps(p):
                with self.assertRaises(ValueError): moves.selection(p,moves.UNIQUES[who][0]['id'],moves.amps(p)[0]['id'])


class ResolutionTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('ivan'); self.s['world']['location']='park'
        for who in ('ivan','sylvanis','rei'): self.s['world']['cast'][who].update(location='park',journey=None)
        self.f=combat.start(self.s,'sylvanis','challenge'); self.f['seed']=17

    def test_opponent_attacks_recovery_and_uses_form(self):
        plan=engine.opponent_plan(self.s); before=copy.deepcopy(self.f)
        self.assertEqual(plan,engine.opponent_plan(self.s)); self.assertEqual(before,self.f)
        self.assertTrue(plan['activate_form']); self.assertIn(plan['move_id'],[x['id'] for x in moves.actions(self.f['opponent_profile'])])
        with patch('world_loop.advance'):
            engine.resolve(self.s,engine.request(self.s,'utility:recover'))
        self.assertEqual(self.f['turn'],1); self.assertTrue(self.f['enemy']['active_form'])
        self.assertGreater(self.f['enemy']['trait_uses'],0)
        self.assertTrue(any(x['side']=='enemy' for x in self.f['exchanges'][0]['records']))

    def test_no_double_turn_and_insufficient_cost_is_atomic(self):
        request=engine.request(self.s,'utility:guard')
        engine.resolve(self.s,request); after=copy.deepcopy(self.f)
        with self.assertRaises(ValueError): engine.resolve(self.s,request)
        self.assertEqual(after,self.f)
        self.f['player']['energy']=0
        skill=moves.UNIQUES['ivan'][0]['id']; before=copy.deepcopy(self.s)
        with self.assertRaises(ValueError): engine.resolve(self.s,engine.request(self.s,skill))
        self.assertEqual(before,self.s)

    def test_environment_breaks_cover_and_roundtrips(self):
        p=profile(self.s,'ivan'); r=self.f['player']; wall=engine.object_at(self.f,'wall')
        self.f['enemy']['cover']='wall'; events=[]
        move=moves.selection(p,'utility:strike')
        damage=engine.terrain_force(p,move,100)
        engine.damage_object(self.f,wall,damage,events)
        self.assertEqual(wall['integrity'],0); self.assertIsNone(self.f['enemy']['cover'])
        self.assertIn(wall['position'],self.f['arena']['rubble'])
        restored=json.loads(json.dumps(self.s)); combat.ensure(restored)
        self.assertEqual(self.f['arena'],restored['combat']['active']['arena'])
        car=engine.object_at(self.f,'vehicle'); engine.damage_object(self.f,car,400,events)
        self.assertEqual(car['integrity'],0)

    def test_trait_amplifications_change_actual_roles(self):
        p=profile(self.s,'ivan'); amps=moves.amps(p)
        for name,tag in [('Fire','heat'),('Wind','speed'),('Ice','ice'),('Red lightning','stagger'),('Blue lightning','precision')]:
            amp=next(x for x in amps if x['name']==name)
            m=moves.selection(p,'utility:strike',amp['id']); self.assertIn(tag,m['tags']); self.assertGreater(m['mana'],0)

    def test_flowing_stream_counters_ranged_with_full_partial_and_failure(self):
        p=make('gordon'); q=make('rei')
        attack=moves.selection(p,'unique:gordon:living-cannon'); counter=moves.selection(q,'unique:rei:flowing-stream')
        outcomes=set()
        for roll in (0.,.4,.99):
            f=copy.deepcopy(self.f); f['player']=combat.resources(p); f['enemy']=combat.resources(q); engine.ensure_arena(f)
            f['arena']['positions']={'player':0,'enemy':6}
            rec=dict(target='opponent',damage=0,hits=0,terrain=[]); ret=dict(damage=0,hits=0,terrain=[])
            rng=random.Random(1)
            with patch.object(rng,'random',return_value=roll): engine.attack(f,'player',p,q,attack,counter,rng,rec,ret)
            outcomes.add(ret.get('outcome'))
        self.assertEqual(outcomes,{'full counter','partial counter','counter missed'})

    def test_partial_combo_and_knockout_interrupt(self):
        p=make('ivan'); q=make('rei'); f=copy.deepcopy(self.f)
        m=moves.selection(p,'unique:ivan:fivefold-ruin'); defence=moves.selection(q,'utility:recover')
        f['arena']['positions']={'player':2,'enemy':3}; rec=dict(target='opponent',damage=0,hits=0,terrain=[])
        rng=random.Random(1)
        with patch.object(rng,'random',side_effect=[0.,.999,0.,.999,0.]): engine.attack(f,'player',p,q,m,defence,rng,rec)
        self.assertEqual(rec['hits'],3); self.assertEqual(rec['outcome'],'partial')
        f['enemy']['health']=1; rec=dict(target='opponent',damage=0,hits=0,terrain=[])
        with patch.object(rng,'random',return_value=0): engine.attack(f,'player',p,q,m,defence,rng,rec)
        self.assertEqual(f['enemy']['health'],0); self.assertEqual(rec['hits'],1)

    def test_narration_failure_never_rerolls_and_stale_result_rejected(self):
        result=engine.resolve(self.s,engine.request(self.s,'utility:guard')); before=copy.deepcopy(self.s)
        with patch.object(combat,'ask_ai',side_effect=ValueError('offline')):
            with self.assertRaises(ValueError): engine.narrate(result)
        self.assertEqual(self.s,before)
        with self.assertRaises(ValueError): engine.commit_narration(self.s,dict(id=result['id'],records=[],narration='wrong'))
        self.assertEqual(self.s,before)

    def test_form_expiry_and_no_unearned_upgrade(self):
        p=self.f['opponent_profile']; action=moves.selection(p,moves.UNIQUES['sylvanis'][0]['id'])
        self.assertEqual(engine.form_action(self.f,'enemy',p,action),action)
        combat.activate_form(self.s,'enemy'); upgraded=engine.form_action(self.f,'enemy',p,action)
        self.assertIn('heat',upgraded['tags']); self.assertGreaterEqual(upgraded['range'],3)
        self.f['enemy']['energy']=0; engine.resolve(self.s,engine.request(self.s,'utility:guard'))
        self.assertIsNone(engine.active_form(self.f,'enemy'))

    def test_interpol_partner_uses_catalogue_and_paid_resources(self):
        self.f.update(kind='interpol',ally='gordon',ally_profile=make('gordon'),ally_resources=combat.resources(make('gordon')))
        energy=self.f['ally_resources']['energy']
        engine.resolve(self.s,engine.request(self.s,'utility:guard'))
        self.assertLess(self.f['ally_resources']['energy'],energy)
        self.assertTrue(any('Field partner exchange' in line for line in self.f['log']))

    def test_wreckage_movement_changes_footing(self):
        car=engine.object_at(self.f,'vehicle'); events=[]
        engine.damage_object(self.f,car,400,events); old=car['position']; record={'terrain':[]}
        self.assertTrue(engine.displace_object(self.f,car,'player',record))
        self.assertNotEqual(car['position'],old); self.assertIn(car['position'],self.f['arena']['rubble'])

    def test_successful_narration_only_replaces_text(self):
        result=engine.resolve(self.s,engine.request(self.s,'utility:guard')); mechanics=copy.deepcopy(combat.exchange_state(self.s))
        def provider(prompt,schema,**kw):
            data=json.loads(prompt.split('Data: ',1)[1])
            return dict(outcome_token=data['outcome_token'],narration=result['narration'])
        with patch.object(combat,'ask_ai',side_effect=provider): narrated=engine.narrate(result)
        engine.commit_narration(self.s,narrated)
        self.assertEqual(combat.exchange_state(self.s),mechanics)

    def test_all_catalogued_actions_resolve_with_bounded_resources(self):
        for who,data in moves.CAST.items():
            p=make(who)
            for action in moves.actions(p):
                if action['kind'] not in ('unique','signature'): continue
                s=copy.deepcopy(self.s); f=s['combat']['active']; s['combat']['profiles'][s['player']]=copy.deepcopy(p)
                f['player']=combat.resources(p); f['enemy']['health']=f['enemy']['max_health']=10000
                f['opponent_profile']['form']=None; f['enemy']['form_used']=True
                f['arena']['positions']={'player':2,'enemy':3}
                with patch('world_loop.advance'): engine.resolve(s,engine.request(s,action['id']))
                for side in ('player','enemy'):
                    self.assertGreaterEqual(f[side]['energy'],0,(who,action['id']))
                    self.assertGreaterEqual(f[side]['stamina'],0,(who,action['id']))


class WorkshopTests(unittest.TestCase):
    def setUp(self): self.s=custom_state()

    def generate(self):
        with patch.object(combat,'ask_ai',return_value={'skills':candidates(self.s)}): return workshop.generate(self.s)

    def test_generate_absorb_cooldown_save_and_no_reset(self):
        result=self.generate(); workshop.commit_candidates(self.s,result); w=workshop.book(self.s)
        chosen=w['candidates'][0]; workshop.absorb(self.s,chosen['id'],w['batch']); ready=w['next_absorption']
        self.assertEqual(workshop.remaining(self.s),1440)
        self.assertEqual(profile(self.s,'garrett')['moveset']['unique'][0],chosen)
        with self.assertRaises(ValueError): workshop.absorb(self.s,chosen['id'],w['batch'])
        restored=json.loads(json.dumps(self.s)); self.assertEqual(workshop.remaining(restored),1440)
        profile(restored,'garrett')['moveset']['unique'].clear(); self.assertEqual(workshop.book(restored)['next_absorption'],ready)
        restored['world']['minute']+=1440; self.assertEqual(workshop.remaining(restored),0)

    def test_stale_generation_stats_or_batch_no_cooldown(self):
        result=self.generate(); profile(self.s,'garrett')['stats']['martial_skill']+=1
        with self.assertRaises(ValueError): workshop.commit_candidates(self.s,result)
        self.assertEqual(workshop.remaining(self.s),0)
        result=self.generate(); workshop.commit_candidates(self.s,result)
        with self.assertRaises(ValueError): workshop.commit_candidates(self.s,result)
        self.assertEqual(workshop.remaining(self.s),0)

    def test_invalid_generation_preserves_saved_candidates(self):
        result=self.generate(); workshop.commit_candidates(self.s,result); before=copy.deepcopy(workshop.book(self.s))
        raw=candidates(self.s); raw[0]['mana']=999
        with patch.object(combat,'ask_ai',return_value={'skills':raw}):
            with self.assertRaises(ValueError): workshop.generate(self.s)
        self.assertEqual(workshop.book(self.s),before)

    def test_generated_effects_stay_within_reviewed_trait(self):
        raw=candidates(self.s); raw[0]['tags']=['ice']
        with self.assertRaises(ValueError): workshop.validate_skills(raw,profile(self.s,'garrett'))
        result=self.generate(); result['candidates'][0]['mana']=999
        with self.assertRaises(ValueError): workshop.commit_candidates(self.s,result)
        self.assertEqual(workshop.remaining(self.s),0)

    def test_reviewed_amp_validation_and_old_custom_bootstrap(self):
        p=profile(self.s,'garrett'); p['moveset']['amplifications']=[]
        with patch.object(combat,'ask_ai',return_value={'amplifications':[AMP]}): result=workshop.generate_amplifications(self.s)
        self.assertFalse(p['moveset']['amplifications']); workshop.accept_amplifications(self.s,result)
        self.assertEqual(len(moves.amps(p)),1); self.assertEqual(workshop.remaining(self.s),0)
        with self.assertRaises(ValueError): workshop.validate_amplifications([AMP|{'mana':True}])

    def test_skill_identity_survives_growth(self):
        result=self.generate(); workshop.commit_candidates(self.s,result); w=workshop.book(self.s)
        workshop.absorb(self.s,w['candidates'][0]['id'],w['batch']); p=profile(self.s,'garrett')
        before=copy.deepcopy(p['moveset']['unique']); p['stats']['awakened_power']=70; moves.initialise(p,'garrett')
        self.assertEqual(p['moveset']['unique'],before)

    def test_real_save_roundtrip_preserves_skill_and_absolute_timer(self):
        result=self.generate(); workshop.commit_candidates(self.s,result); w=workshop.book(self.s)
        workshop.absorb(self.s,w['candidates'][0]['id'],w['batch'])
        with tempfile.TemporaryDirectory() as folder:
            dest=Path(folder)/'enhanced-save.json'; core.save(self.s,dest); restored=core.load(dest)
        self.assertEqual(workshop.book(restored),w)
        self.assertEqual(profile(restored,'garrett')['moveset'],profile(self.s,'garrett')['moveset'])


if __name__=='__main__': unittest.main()
