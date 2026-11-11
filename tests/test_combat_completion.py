"""Remaining Part 2 contracts: partners, objective movement and disclosure."""
import copy,json,random,unittest
from unittest.mock import patch
import combat,combat_engine as engine,combat_profiles as profiles,combat_states as states
import combat_identity as identity,combat_objectives as objectives,game_core as core

class CompletionTests(unittest.TestCase):
    def test_crow_campaign_forces_defeat_at_four_exchanges(self):
        s,f=self.scene(); f['turn']=3; f['enemy']['health']=1
        with patch('interpol.crow_story_fight',return_value=True):
            combat.complete_exchange(s)
        self.assertEqual(f['turn'],4)
        self.assertTrue(f['result'].startswith('Defeat'))
        self.assertGreater(f['enemy']['health'],0)
        self.assertEqual(f['player']['health'],0)

    def test_repeated_control_cannot_refresh_immunity_or_infinite_lock(self):
        import combat_moves as moves
        s,f=self.scene(); p=profiles.profile(s,'rei'); q=f['opponent_profile']
        f['arena']['positions'].update(player=2,enemy=3)
        attack=moves.spec('test:control','Control','Finite control','control',tags=['restrain'])
        guard=moves.selection(q,'utility:recover'); rng=random.Random(1)
        for n in range(2):
            rec=dict(target='opponent',damage=0,hits=0,terrain=[])
            with patch.object(rng,'random',return_value=0): engine.attack(f,'player',p,q,attack,guard,rng,rec)
            if n==0:
                self.assertEqual(f['enemy']['control_immunity'],3)
                f['enemy']['restrained']=0; f['enemy']['control_immunity']=2
        self.assertEqual(f['enemy']['restrained'],0)
        self.assertEqual(f['enemy']['control_immunity'],2)

    def test_reflection_and_stored_force_are_capped(self):
        import combat_moves as moves
        s,f=self.scene(); p=profiles.make('gordon'); q=profiles.make('rei')
        f.update(player=combat.resources(p),enemy=combat.resources(q)); engine.ensure_arena(f)
        attack=moves.selection(p,'unique:gordon:living-cannon'); attack['force']=10000
        counter=moves.selection(q,'unique:rei:flowing-stream')
        capacity=engine.raw_damage(q,counter,f['enemy'],f,'enemy')
        rec=dict(target='opponent',damage=0,hits=0,terrain=[]); ret=dict(damage=0,hits=0,terrain=[])
        rng=random.Random(1)
        with patch.object(rng,'random',return_value=0): engine.attack(f,'player',p,q,attack,counter,rng,rec,ret)
        self.assertLessEqual(ret['damage'],round(capacity*2)+1)
        self.assertLessEqual(f['player']['stored'],120)

    def test_recovery_does_not_heal_and_resources_stay_capped(self):
        import combat_moves as moves
        s,f=self.scene(); p=profiles.profile(s,'rei'); r=f['player']; r['health']=10
        m=moves.selection(p,'utility:recover')
        for n in range(12): engine.utility(f,'player',p,m,{})
        self.assertEqual(r['health'],10); self.assertEqual(r['stamina'],100)
        self.assertEqual(r['energy'],r['max_energy'])

    def test_generated_review_contains_current_force_forecast(self):
        from test_enhanced_combat import custom_state,candidates
        import combat_workshop as workshop
        s=custom_state(); p=profiles.profile(s,s['player'])
        skills=workshop.validate_skills(candidates(s),p)
        for skill in skills:
            review=skill['balance_review']; self.assertEqual(review['version'],2)
            self.assertGreater(review['forecast']['raw_force'],0)
            self.assertTrue(review['forecast']['affordable'])

    def scene(self,ally='neo'):
        s=core.fresh('rei'); s['world']['location']='park'
        s['world']['cast']['ivan'].update(location='park',journey=None)
        with patch.object(combat,'consent',return_value=(True,'')): combat.start(s,'ivan','challenge')
        f=combat.active(s); f['kind']='guard'; engine.ensure_arena(f)
        p=profiles.make(ally); f.update(ally=ally,ally_profile=p,ally_resources=combat.resources(p))
        f['arena']['positions'].update(player=1,enemy=4,ally=1)
        return s,f

    def test_partner_protocol_four_clocks_without_double_ticking_enemy(self):
        s,f=self.scene(); r=f['ally_resources']; states.ensure(r); r['protocol_ready']=4
        f['enemy']['protocol_left']=3
        for n in range(4):
            engine.support_turn(s,f,random.Random(n))
            self.assertEqual(r['protocol_left'],3-n)
            self.assertEqual(f['enemy']['protocol_left'],3)
            f['turn']+=1
        self.assertEqual(r['protocol_strain'],2)
        self.assertIn('neo',s['combat']['protocol_spent'])
        restored=json.loads(json.dumps(s))
        self.assertEqual(restored['combat']['active']['ally_resources']['protocol_strain'],2)

    def test_partner_channels_costs_and_endurance_expire(self):
        s,f=self.scene('valentina'); r=f['ally_resources']; r['health']=round(r['max_health']*.4)
        before=r['energy']; engine.support_turn(s,f,random.Random(1))
        self.assertLess(r['energy'],before); self.assertEqual(r['endurance_left'],3)
        self.assertEqual(r['channel'],'Wind')
        self.assertGreaterEqual(r['energy'],0)

    def test_april_observed_support_is_bounded_and_not_free(self):
        s,f=self.scene('april'); r=f['ally_resources']; f['turn']=1
        engine.support_turn(s,f,random.Random(2)); self.assertFalse(any('calls an opening' in x for x in f['log']))
        f['turn']=3; before=r['stamina']; engine.support_turn(s,f,random.Random(3))
        self.assertEqual(f['player']['focus'],1)
        self.assertEqual(r['stamina'],before-2) # seven cost, five guard recovery
        self.assertLess(r['max_health'],f['player']['max_health'])
        self.assertTrue(any('observed patterns' in x for x in f['log']))

    def test_rescue_requires_escort_position_alive_and_unrestrained(self):
        s,f=self.scene('april'); f.update(objective='Rescue ally',turn=4)
        f['arena']['positions'].update(player=0,enemy=5,ally=2)
        self.assertFalse(objectives.success(f))
        f['arena']['positions']['ally']=0
        self.assertTrue(objectives.success(f))
        f['ally_resources']['restrained']=1; self.assertFalse(objectives.success(f))
        f['ally_resources']['restrained']=0; f['ally_resources']['health']=0
        self.assertFalse(objectives.success(f))

    def test_escort_follows_one_space_without_charging_the_enemy(self):
        s,f=self.scene('daniel'); f.update(objective='Rescue ally',turn=1)
        f['arena']['positions'].update(player=0,enemy=6,ally=2)
        engine.support_turn(s,f,random.Random(1))
        self.assertEqual(f['arena']['positions']['ally'],1)
        engine.support_turn(s,f,random.Random(2))
        self.assertEqual(f['arena']['positions']['ally'],0)

    def test_exhausted_partner_recovers_without_negative_resources(self):
        s,f=self.scene('thirteen'); r=f['ally_resources']; states.ensure(r)
        r.update(stamina=0,energy=0,protocol_left=2,protocol_used=True)
        engine.support_turn(s,f,random.Random(4))
        self.assertGreater(r['stamina'],0); self.assertGreaterEqual(r['energy'],0)
        self.assertEqual(r['protocol_left'],1)

    def test_operational_reputation_does_not_link_civilian_identity(self):
        s=core.fresh('rei'); title=identity.LORE['mavis']['title']
        identity.learn_title(s,['rei'],title,'authored briefing')
        self.assertTrue(identity.known_title(s,'rei',title))
        self.assertFalse(identity.recognised(s,'rei','mavis'))
        self.assertFalse(identity.public(s,'mavis',['rei'])['title'])
        self.assertTrue(identity.public_titles(s,['rei']))
        self.assertFalse(identity.public_titles(s,['rei','emily']))

    def test_earned_disclosures_cover_non_ace_operatives(self):
        import interpol
        s=core.fresh('rei'); self.assertFalse(identity.recognised(s,'rei','ivan'))
        interpol.reveal(s,['rei'],'ivan','case evidence')
        self.assertTrue(identity.recognised(s,'rei','ivan'))
        self.assertIn('Joker',identity.public(s,'ivan',['rei'])['title'])
        self.assertFalse(identity.public(s,'ivan',['rei','emily'])['title'])

    def test_no_absent_or_recovering_patrol_partner(self):
        import organisation_guards as guards,relationship_dynamics as relationships
        s=core.fresh('rei'); s['world']['location']='park'
        s['groups']['test']=dict(members=['april'],open=True,channel='in_person',history=[])
        s['active_group']='test'; s['world']['cast']['april'].update(location='park',journey=None)
        with patch.object(relationships,'stats',return_value={'trust':80}):
            self.assertIn('april',guards.patrol_allies(s))
            combat.ensure(s)['recovery']['april']=s['world']['minute']+10
            self.assertNotIn('april',guards.patrol_allies(s))
            s['combat']['recovery'].clear(); s['world']['cast']['april']['location']='downtown'
            self.assertNotIn('april',guards.patrol_allies(s))

if __name__=='__main__': unittest.main()
