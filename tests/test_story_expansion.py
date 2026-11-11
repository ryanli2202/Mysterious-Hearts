import copy
import json
import unittest

import combat
import combat_engine
import game_core as core
import charles_quest as quest
import interpol as law
from test_charles_quest import arrive, clear_security
from test_interpol import locate


def crow_fight(player='fox'):
    s=core.fresh(player)
    partner='gordon' if player=='fox' else 'fox'
    locate(s,'interpol_hq',partner,minute=12*60)
    d=law.ensure(s)
    d['files']['crow_trail']=dict(complete=True)
    law.begin(s,'crow_operation')
    d['files']['crow_operation']['step']=2
    locate(s,'syndicate_hq',partner)
    law.start_encounter(s)
    return s


class StoryExpansionTests(unittest.TestCase):
    def test_old_reunion_continues_without_erasing_it(self):
        s=core.fresh('garrett')
        s['charles_quest']=dict(quest.read(s),step=11,ending='guarded reconciliation')
        before=copy.deepcopy(s['charles_quest'])
        self.assertEqual(quest.objective(s)[1],'garrett_home')
        self.assertEqual(before,s['charles_quest'])
        self.assertTrue(quest.reunited(s))
        arrive(s,0);quest.check_in(s)
        for i in range(11,len(quest.STEPS)):
            arrive(s,i);clear_security(s);quest.advance(s,1)
            s=json.loads(json.dumps(s))
        d=quest.read(s)
        self.assertTrue(d['complete'])
        self.assertEqual(d['ending'],'guarded reconciliation')
        self.assertEqual(d['red_dragons']['18'],'resident-led accountability council')
        self.assertEqual(d['red_dragons']['15'],'supervised restitution')
        self.assertNotIn('red_dragons',str(quest.knowledge(s,'charles',['ivan'])))

    def test_protection_defeat_requires_retry_and_victories_persist(self):
        s=core.fresh('garrett');s['charles_quest']=dict(quest.read(s),step=14)
        with self.assertRaises(ValueError):quest.security_action(s)
        arrive(s,14)
        with self.assertRaises(ValueError):quest.advance(s,0)
        quest.security_action(s);combat.concede(s);combat.close(s)
        self.assertEqual(len(quest.garrett_chapters.remaining(s,14)),3)
        clear_security(s);s=json.loads(json.dumps(s));s['world']['minute']+=1440
        self.assertFalse(quest.garrett_chapters.remaining(s,14))
        quest.advance(s,0)
        self.assertEqual(quest.read(s)['step'],15)

    def test_new_charles_scene_remains_private(self):
        s=core.fresh('garrett');s['charles_quest']=dict(quest.read(s),step=17)
        arrive(s,17);s['world']['cast']['ivan']['location']=quest.LAB
        with self.assertRaises(ValueError):quest.advance(s,0)

    def test_crow_cannot_be_awarded_victory_or_knockout(self):
        for player in ('fox','gordon'):
            s=crow_fight(player);s=json.loads(json.dumps(s))
            combat.finish(s,'Victory — test finishing strike','crow')
            self.assertTrue(combat.active(s)['result'].startswith('Defeat'))
            self.assertEqual(combat.recovering(s,'crow'),0)
            combat.close(s);combat.close(s)
            file=law.read(s)['files']['crow_operation']
            self.assertEqual(file['step'],3)
            self.assertEqual(len(file['evidence']),1)
            self.assertTrue(file['crow_defeated_team'])
            self.assertNotIn('crow',law.read(s)['custody'])
            self.assertEqual(s['world']['location'],'interpol_containment')
            law.regroup(s)
            self.assertTrue(law.here(s,law.read(s)['active']['partner']))
            law.advance(s)

    def test_crow_ends_after_four_real_exchanges(self):
        s=crow_fight()
        for _ in range(4):
            if combat.active(s)['status']=='finished':break
            combat_engine.resolve(s,combat_engine.request(s,'utility:guard'))
        self.assertEqual(combat.active(s)['status'],'finished')
        self.assertTrue(combat.active(s)['result'].startswith('Defeat'))

    def test_previously_earned_crow_capture_is_preserved(self):
        s=crow_fight();combat.active(s)['status']='finished';s['combat']['active']=None
        d=law.ensure(s);d['encounter']=None
        d['files']['crow_operation'].update(step=3,evidence=[dict(finding='The Crow is defeated in this operation; the team secures the command records.')])
        self.assertEqual(law.objective(s)['kind'],'close')
        law.travel_objective(s);law.advance(s)
        self.assertTrue(d['files']['crow_operation']['complete'])
        self.assertIn('crow',d['custody'])
        self.assertNotIn('syndicate_outcome',d)


if __name__=='__main__':unittest.main()
