import copy
import json
import tempfile
from pathlib import Path
import unittest
import game_core as core
import post_story as post
import combat
import organisation_guards as guards
import interpol as law
from test_major_campaigns import arrive,win
from test_interpol import locate


def finished(player,route='leave'):
    s=core.fresh(player)
    if player=='garrett':
        import charles_quest
        s['charles_quest']=dict(charles_quest.read(s),step=len(charles_quest.STEPS),complete=True)
    else:
        import rei_story,job_apps
        rei_story.data(s).update(stage=6,richter=True,hamayashi=route,complete=True)
        guards.data(s)['disabled']=['blackstone']+(['hamayashi'] if route=='destroyed' else [])
        if route=='lead':job_apps.ensure(s)['gang']=dict(id='hamayashi',name='Hamayashi-kai',role='Leader',rank=4,standing=100)
    arrive(s,post.base(s))
    return s


def run(s,key):
    arrive(s,post.base(s));post.begin(s,key)
    arrive(s,post.MISSIONS[key]['venue']);post.verify(s)
    while post.remaining(s):post.fight(s);win(s)
    return post.finish(s)


class PostStoryTests(unittest.TestCase):
    def test_completion_and_route_gates(self):
        for player in ('garrett','rei','fox'):
            s=core.fresh(player)
            self.assertFalse(post.available(s))
            with self.assertRaises(ValueError):post.begin(s,'dragon_market')
        for route,key in [('lead','kai_charter'),('leave','kai_watch'),('destroyed','kai_remnants')]:
            s=finished('rei',route)
            self.assertEqual(set(post.available(s)),{'blackstone_transfer','blackstone_records',key})
            with self.assertRaises(ValueError):post.begin(s,'dragon_market')

    def test_all_missions_repeat_without_reviving_defeated_factions(self):
        for player,route in [('garrett','leave'),('rei','lead'),('rei','leave'),('rei','destroyed')]:
            s=finished(player,route);disabled=copy.deepcopy(guards.data(s)['disabled'])
            for key in post.available(s):
                run(s,key);count=post.data(s)['protected']
                arrive(s,post.base(s))
                with self.assertRaises(ValueError):post.begin(s,key)
                s['world']['minute']+=1440;run(s,key)
                self.assertEqual(post.data(s)['protected'],count+1)
                self.assertEqual(guards.data(s)['disabled'],disabled)
            self.assertNotIn('crow',s.get('interpol',{}).get('custody',{}))

    def test_physical_evidence_victory_and_duplicate_gates(self):
        s=finished('garrett');post.begin(s,'dragon_market')
        with self.assertRaises(ValueError):post.verify(s)
        arrive(s,'blackhaven')
        with self.assertRaises(ValueError):post.fight(s)
        post.verify(s)
        post.fight(s);combat.concede(s);combat.close(s)
        self.assertEqual(len(post.remaining(s)),2)
        with self.assertRaises(ValueError):post.finish(s)
        while post.remaining(s):post.fight(s);win(s)
        post.finish(s);before=copy.deepcopy(s)
        with self.assertRaises(ValueError):post.finish(s)
        self.assertEqual(s,before)

    def test_active_fight_save_load_and_midnight_keep_victories(self):
        s=finished('rei','destroyed');post.begin(s,'kai_remnants');arrive(s,'market');post.verify(s)
        post.fight(s)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json';core.save(s,path);s=core.load(path)
        win(s);s['world']['minute']+=1440
        self.assertEqual(len(post.remaining(s)),1)
        post.fight(s);win(s);post.finish(s)
        self.assertEqual(post.data(s)['completed']['kai_remnants'],s['world']['minute']//1440)

    def test_management_funds_daily_limit_and_shelter_use(self):
        s=finished('rei','lead');money=s['world']['money']
        import bubblegram_progression
        self.assertIn('Leader',bubblegram_progression.gang_title(s['job_apps']['gang']))
        post.manage(s,'shelter');m=post.data(s)['management']
        self.assertEqual(m['budget'],350)
        with self.assertRaises(ValueError):post.manage(s,'departures')
        text=run(s,'blackstone_transfer')
        self.assertIn('funded shelter',text);self.assertEqual(m['shelter'],0);self.assertEqual(m['budget'],450)
        self.assertEqual(s['world']['money'],money)
        s['world']['minute']+=1440;post.manage(s,'departures')
        self.assertEqual(m['actions']['departures'],1)
        s['world']['minute']+=1440;post.manage(s,'recruitment')
        s['job_apps']['gang']=None
        with self.assertRaises(ValueError):post.manage(s,'shelter')
        self.assertNotIn('kai_charter',post.available(s))
        for route in ('leave','destroyed'):
            with self.assertRaises(ValueError):post.manage(finished('rei',route),'shelter')

    def test_withdrawal_cannot_reuse_victories(self):
        s=finished('garrett');post.begin(s,'dragon_market');arrive(s,'blackhaven');post.verify(s)
        post.fight(s);win(s);scope=post.read(s)['active']['scope'];post.withdraw(s)
        self.assertEqual(post.read(s)['protected'],0)
        arrive(s,post.base(s));post.begin(s,'dragon_market')
        self.assertNotEqual(post.read(s)['active']['scope'],scope)
        self.assertEqual(len(post.remaining(s)),2)

    def test_post_night_ledger_operations_for_both_partners(self):
        keys=[k for k,v in law.OPERATIONS.items() if v.get('post_story')]
        for player,partner in [('fox','gordon'),('gordon','fox')]:
            s=core.fresh(player);d=law.ensure(s)
            d['files']['blackhaven']=dict(complete=True)
            locate(s,'interpol_hq',partner)
            with self.assertRaises(ValueError):law.begin(s,keys[0],True)
            d['files']['crow_operation']=dict(complete=True,crow_defeated_team=True)
            d['syndicate_outcome']='ongoing resistance'
            for key in keys:
                locate(s,'interpol_hq',partner);law.begin(s,key,True);law.travel_objective(s)
                while d['active']:
                    law.advance(s)
                    self.assertNotEqual(combat.active(s)['opponent'],'crow')
                    win(s)
                self.assertNotIn('crow',d['custody'])
                self.assertEqual(d['syndicate_outcome'],'ongoing resistance')
                locate(s,'interpol_hq',partner)
                with self.assertRaises(ValueError):law.begin(s,key,True)
                s['world']['minute']+=1440;law.begin(s,key,True);law.suspend(s)


if __name__=='__main__':unittest.main()
