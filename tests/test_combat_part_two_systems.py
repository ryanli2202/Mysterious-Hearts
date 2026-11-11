import copy,json,unittest
from unittest.mock import patch
import combat,combat_engine as engine,combat_profiles as profiles,combat_states as states,combat_circle
import combat_identity,combat_boss,combat_moves,combat_objectives
import game_core as core

class PartTwoSystemTests(unittest.TestCase):
    def fight(self,who='neo',enemy='thirteen'):
        s=core.fresh(who); s['world']['location']='park'
        s['world']['cast'][enemy].update(location='park',journey=None)
        with patch.object(combat,'consent',return_value=(True,'')): combat.start(s,enemy,'challenge')
        return s,combat.active(s)

    def test_protocol_cost_duration_strain_save_and_restart(self):
        s,f=self.fight(); p=profiles.profile(s,'neo'); f['player']['protocol_ready']=4
        states.activate_protocol(s); self.assertEqual(f['player']['stamina'],80)
        s=json.loads(json.dumps(s)); f=combat.active(s); self.assertEqual(f['player']['protocol_left'],4)
        records={side:dict(move_id='utility:guard',role='defence',damage=0) for side in ('player','enemy')}
        selected={side:combat_moves.selection(p,'utility:guard') for side in records}
        for n in range(4):
            states.end_exchange(f,{'player':p,'enemy':f['opponent_profile']},selected,copy.deepcopy(records))
            self.assertEqual(f['player']['protocol_left'],3-n)
        self.assertEqual(f['player']['protocol_strain'],2)
        self.assertFalse(states.protocol_available(s,f,'player',p))
        combat.concede(s); combat.close(s)
        with patch.object(combat,'consent',return_value=(True,'')): combat.start(s,'thirteen','challenge')
        f=combat.active(s); f['player']['protocol_ready']=4
        self.assertFalse(states.protocol_available(s,f,'player',p))
        combat.concede(s); combat.close(s)
        states.rest(s); self.assertFalse(s['combat']['protocol_spent'])

    def test_repetition_does_not_farm_readiness_and_momentum(self):
        s,f=self.fight('daniel','neo'); p=profiles.profile(s,'daniel')
        f['arena']['positions'].update(player=1,enemy=2)
        records={side:dict(move_id='utility:strike',role='attack',damage=10) for side in ('player','enemy')}
        selected={side:combat_moves.selection(p,'utility:strike') for side in records}
        for n in range(6): states.end_exchange(f,{'player':p,'enemy':f['opponent_profile']},selected,copy.deepcopy(records))
        self.assertEqual(f['player']['war_momentum'],1); self.assertEqual(f['enemy']['protocol_ready'],1)
        for n in range(2):
            records['player']['move_id']=str(n)
            states.end_exchange(f,{'player':p,'enemy':f['opponent_profile']},selected,copy.deepcopy(records))
        self.assertEqual(f['player']['war_momentum'],3)
        m=combat_moves.spec('test','Test','Test','break'); altered=states.prepare_action(p,f['player'],m)
        self.assertTrue(altered['war_finisher']); self.assertGreater(altered['stamina'],m['stamina'])

    def test_elemental_effects_and_no_free_efficiency(self):
        p=profiles.make('ivan'); r=combat.resources(p); states.ensure(r)
        move=combat_moves.selection(p,'utility:strike'); changes={}
        for channel in states.channels(p)[1:]:
            r['channel']=channel; changes[channel]=states.prepare_action(p,r,move)
        self.assertGreater(changes['Red lightning']['force'],changes['Fire']['force'])
        self.assertIn('speed',changes['Blue lightning']['tags'])
        self.assertTrue(changes['Ice']['instant_reaction'])
        self.assertEqual(changes['Wind']['soul_fraction'],.22)
        self.assertIn('breach',changes['Fire']['tags'])
        p=profiles.make('charles'); m=copy.deepcopy(move); m['mana']=1
        self.assertEqual(states.prepare_action(p,r,m)['mana'],5) # 1 minimum plus active ice upkeep
        self.assertNotIn('Ice',states.channels(profiles.make('valentina')))

    def test_title_bout_required_and_earned_title_retained(self):
        s=core.fresh('garrett'); s['world']['location']='iron_circle'; combat.sign_ledger(s,'G')
        ledger=s['combat']['ledger']; ledger['rank']=3; s['world']['minute']=ledger['next']
        p=combat.validate_opponent(s,dict(name='Challenger',art='Boxing',trait='Spark',limitations='Contact only'))
        combat.start(s,'circle:test','circle',p); combat.finish(s,'Victory — fixture'); combat.close(s)
        self.assertEqual(ledger['rank'],2); s['world']['minute']=ledger['next']
        with self.assertRaises(ValueError): combat.validate_opponent(s,p)
        with patch.object(combat,'ask_ai',side_effect=AssertionError('Champion is authored')): title=combat.generate_opponent(s)
        self.assertEqual(title['champion_id'],'rei')
        f=combat.start(s,'ignored','circle',title); self.assertEqual(f['opponent'],'rei')
        combat.finish(s,'Victory — fixture'); self.assertEqual(ledger['champion'],'garrett')
        restored=json.loads(json.dumps(s)); combat.ensure(restored)
        self.assertEqual(restored['combat']['ledger']['rank'],1)
        self.assertEqual(restored['combat']['ledger']['titles_earned'],1)

    def test_recognition_observation_does_not_disclose_identity(self):
        s=core.fresh('rei'); combat_identity.observe(s,'rei','mavis','unique:mavis:test')
        self.assertFalse(combat_identity.public(s,'mavis',['rei'])['title'])
        s['combat']['recognition']['rei']['mavis']['identity']=True
        self.assertIn('Ace of Spades',combat_identity.public(s,'mavis',['rei'])['title'])
        self.assertFalse(combat_identity.public(s,'mavis',['rei','emily'])['title'])
        self.assertIn('personal identity unknown',combat_identity.sheet('crow')['reputation'])

    def test_title_defence_loss_preserves_earned_history_and_current_champion(self):
        s=core.fresh('garrett'); s['world']['location']='iron_circle'; combat.sign_ledger(s,'G')
        ledger=s['combat']['ledger']; ledger.update(rank=1,champion='garrett',titles_earned=2)
        challenger=profiles.make('rei')
        f=dict(id='defence',title_defence=True,opponent='rei',opponent_profile=challenger)
        combat_circle.finish(s,f,False)
        self.assertEqual(ledger['rank'],2); self.assertEqual(ledger['titles_earned'],2)
        self.assertEqual(combat_circle.candidate(s)['champion_id'],'rei')
        self.assertEqual(ledger['title_history'][-1]['previous'],'garrett')

    def test_protocol_zero_stamina_still_allows_recovery(self):
        s,f=self.fight('neo','rei'); p=profiles.make('thirteen')
        s['combat']['profiles']['neo']=p
        f['player'].update(stamina=0,protocol_left=2,protocol_used=True)
        recovery=states.prepare_action(p,f['player'],combat_moves.selection(p,'utility:recover'))
        self.assertEqual(recovery['stamina'],0)
        engine.resolve(s,engine.request(s,'utility:recover'))
        self.assertGreater(f['player']['stamina'],0)

    def test_objectives_exclude_campaign_boss(self):
        s,f=self.fight('garrett','rei'); f['opponent_profile']['boss']='richter'
        self.assertEqual(combat_objectives.choices(f),['Duel'])
        with self.assertRaises(ValueError): combat_objectives.select(s,'Escape')
        del f['opponent_profile']['boss']; combat_objectives.select(s,'Escape')
        f['arena']['positions'].update(player=0,enemy=4)
        self.assertTrue(combat_objectives.success(f)); f['player']['restrained']=1
        self.assertFalse(combat_objectives.success(f))

    def test_custom_names_do_not_grant_canonical_states(self):
        for name in ('Shinigami Protocol','Conduit','True Sight'):
            p=profiles.make('custom',dict(awakened=True,awakening_trait=name,awakening_description='A reviewed custom effect.'))
            self.assertFalse(states.trait(p,name)); self.assertFalse(states.channels(p))

    def test_misanthropy_records_injury_debt_and_does_not_heal(self):
        s,f=self.fight('ivan','rei'); states.activate_endurance(s)
        r=f['player']; r['health']=5; rec={'damage':0}
        engine.hurt(f,'player',10,rec)
        self.assertEqual(r['health'],1); self.assertEqual(r['endurance_debt'],6)
        self.assertEqual(rec['endurance_debt'],6)
        engine.hurt(f,'player',r['max_health'],rec)
        self.assertEqual(r['health'],0)

if __name__=='__main__': unittest.main()
