"""Part 2 initial slice: save compatibility and enforced arena calibration."""
import copy
import json
import unittest
from unittest.mock import patch
import combat
import combat_balance
import combat_engine
import combat_profiles as profiles
import game_core as core


class CombatPartTwoTests(unittest.TestCase):
    def test_all_rank_boundaries_and_small_numeric_steps(self):
        expected={450:'D',301:'D',300:'C',101:'C',100:'B',11:'B',10:'Low A',2:'Low A'}
        for rank,band in expected.items():
            self.assertEqual(combat_balance.arena_profile(rank)[0],band)
        for rank in range(3,451):
            stronger=combat_balance.arena_profile(rank-1)[2]
            weaker=combat_balance.arena_profile(rank)[2]
            self.assertTrue(all(0<=a-b<=1 for a,b in zip(stronger,weaker)),rank)
        contender=combat_balance.arena_profile(2)[2]
        self.assertTrue(all(a<b for a,b in zip(contender,profiles.RATINGS['rei'])))

    def test_generated_claims_cannot_override_rank_calibration(self):
        s=core.fresh('garrett'); s['world']['location']='iron_circle'
        combat.sign_ledger(s,'Garrett')
        original=copy.deepcopy(profiles.profile(s,'garrett'))
        for rank in (450,301,300,101,100,11,10,3):
            s['combat']['ledger']['rank']=rank
            p=combat.validate_opponent(s,dict(name='Test',art='Boxing',trait='Spark',
                limitations='Contact only',stats=dict.fromkeys(profiles.STATS,10000),arena_band='S+'))
            band,_,values=combat_balance.arena_profile(rank)
            self.assertEqual(tuple(p['stats'].values()),values)
            self.assertEqual(p['arena_band'],band)
            self.assertEqual(p,combat.validate_opponent(s,p))
            self.assertEqual(bool(p['trait']),rank<=100)
        self.assertEqual(original,profiles.profile(s,'garrett'))
        with self.assertRaises(ValueError):
            combat.validate_opponent(s,dict(name='Test',art='Boxing',trait='',limitations=''))

    def test_trait_migration_preserves_progress_and_is_idempotent(self):
        for who,name in (('neo','Shinigami Protocol'),('thirteen','Shinigami Protocol'),
                         ('daniel','War God'),('april','Polymath')):
            p=profiles.make(who); p.pop('identity_version'); p['trait']=None
            p['stats']['trait_refinement']=0; p['stats']['martial_skill']+=1
            p['moveset']['amplifications']=[]
            p['path']['encounters']=23
            old=copy.deepcopy(p)
            profiles.reconcile_identity(p,who)
            self.assertEqual(p['trait']['name'],name)
            self.assertEqual(p['path'],old['path'])
            self.assertEqual(p['stats']['martial_skill'],old['stats']['martial_skill'])
            for key in ('learned','unique'):
                self.assertEqual(p['moveset'][key],old['moveset'][key])
            self.assertEqual(p['moveset']['amplifications'],profiles.make(who)['moveset']['amplifications'])
            saved=json.loads(json.dumps(p)); profiles.reconcile_identity(p,who)
            self.assertEqual(p,saved)
        custom=profiles.make('neo',{'awakened':True,'awakening_trait':'Custom','awakening_description':'My trait'})
        custom.pop('identity_version'); before=copy.deepcopy(custom)
        profiles.reconcile_identity(custom,'neo'); before['identity_version']=1
        self.assertEqual(custom,before)

    def test_active_resources_and_catalogue_ids_survive_reload(self):
        s=core.fresh('garrett'); s['world']['location']='park'
        s['world']['cast']['neo'].update(location='park',journey=None)
        with patch.object(combat,'consent',return_value=(True,'')):
            f=combat.start(s,'neo','challenge')
        q=f['opponent_profile']; q.pop('identity_version'); q['trait']=None
        q['stats']['trait_refinement']=0; q['moveset']['amplifications']=[]
        f['enemy']['health']=40; f['enemy']['stamina']=31; f['enemy']['energy']=17
        resources=copy.deepcopy(f['enemy']); ids=[a['id'] for a in q['moveset']['unique']]
        s=json.loads(json.dumps(s)); combat.ensure(s); f=combat.active(s)
        self.assertEqual(f['enemy'],resources)
        self.assertEqual(f['opponent_profile']['trait']['name'],'Shinigami Protocol')
        self.assertEqual(ids,[a['id'] for a in f['opponent_profile']['moveset']['unique']])
        # Actual resolver accepts the migrated encounter; narrative is not needed.
        combat_engine.resolve(s,combat_engine.request(s,'utility:guard'))
        self.assertEqual(f['turn'],1)


if __name__=='__main__': unittest.main()
