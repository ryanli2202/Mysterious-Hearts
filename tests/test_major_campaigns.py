import copy
import json
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import game_core as core
import organisation_guards as guards
import rei_story as rei
import combat
import combat_engine
import combat_moves
import interpol
import charles_quest as charles
import town

def arrive(s,venue):
    s['world']['location']=venue
    s['world']['cast'][s['player']].update(location=venue,journey=None,activity='Investigating')
    s['world']['party']=[];s['world']['npcs']=[]

def win(s):
    combat.finish(s,'Victory — test resolution');combat.close(s)

def clear(s,venues,scope):
    for venue in venues:
        arrive(s,venue)
        while guards.remaining(s,venue,scope):guards.begin(s,venue,scope);win(s)

def investigate(s):
    for i,scene in enumerate(rei.SCENES):
        from flashback_helpers import finish_memories
        finish_memories(s)
        arrive(s,scene[1]);rei.advance(s,i%2)

class MajorCampaignTests(unittest.TestCase):
    def test_active_mission_roundtrip_and_record_once(self):
        s=core.fresh('rei');investigate(s);arrive(s,'blackstone_hq');rei.fight_guards(s)
        token=combat.active(s)['guard_token']
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'story.json';core.save(s,p);s=core.load(p)
        self.assertEqual(combat.active(s)['guard_token'],token)
        win(s);count=len(guards.data(s)['history']);combat.close(s)
        self.assertEqual(len(guards.data(s)['history']),count)
        self.assertEqual(len(guards.remaining(s,'blackstone_hq','rei:blackstone')),2)

    def test_former_crew_cannot_steal_guards(self):
        s=core.fresh('rei');import job_apps
        job_apps.ensure(s)['gang']=dict(name='First crew',role='Founder',rank=0,standing=0,members={})
        arrive(s,'crew_lot_west');s['world']['money']=100000
        guards.buy(s,'crew_lot_west','Hideout');guards.recruit(s,'First watch','robotic','crew_lot_west')
        kind=guards.data(s)['roster'][0]['type'];guards.rename_type(s,kind,'Workshop watch')
        self.assertEqual(guards.spec(s,kind)[0],'Workshop watch')
        s['job_apps']['gang']['name']='Second crew'
        with self.assertRaises(ValueError):guards.recruit(s,'Another watch','robotic','crew_lot_west')
        with self.assertRaises(ValueError):guards.rename_type(s,kind,'Stolen watch')
    def test_all_rei_endings_and_reload(self):
        for ending in ('leave','lead','destroy'):
            s=core.fresh('rei');investigate(s);rei.choose(s,ending)
            self.assertFalse(rei.data(s)['complete'])
            if ending=='destroy':
                clear(s,guards.HAMAYASHI,'rei:hamayashi')
                self.assertEqual(rei.data(s)['hamayashi'],'destroyed')
                self.assertFalse(guards.slots(s,'hamayashi_house'))
            if ending=='lead':self.assertEqual(s['job_apps']['gang']['role'],'Leader')
            s=json.loads(json.dumps(s));clear(s,guards.BLACKSTONE,'rei:blackstone')
            rei.confront(s)
            self.assertIn('cybernetic',combat.active(s)['opponent_profile']['name'])
            combat.concede(s);combat.close(s)
            self.assertFalse(rei.data(s)['richter'])
            rei.confront(s);win(s)
            self.assertTrue(rei.data(s)['complete'])
            self.assertIn('I am sorry',rei.data(s)['journal'][-1]['text'])
            with self.assertRaises(ValueError):rei.confront(s)

    def test_gates_and_private_context(self):
        s=core.fresh('rei')
        with self.assertRaises(ValueError):rei.advance(s)
        with self.assertRaises(ValueError):guards.check_trip(s,'rei','blackstone_lab')
        investigate(s);arrive(s,'blackstone_command')
        with self.assertRaises(ValueError):rei.confront(s)
        arrive(s,'blackstone_hq');s['world']['party']=['garrett']
        with self.assertRaises(ValueError):rei.fight_guards(s)
        self.assertEqual(rei.context(s,'garrett',['emily']),'')
        with self.assertRaises(ValueError):rei.advance(core.fresh('garrett'))

    def test_patrol_respawn_and_campaign_no_respawn(self):
        s=core.fresh('rei');arrive(s,'hamayashi_house')
        count=len(guards.remaining(s,'hamayashi_house'))
        guards.begin(s);combat.concede(s);combat.close(s)
        self.assertEqual(len(guards.remaining(s,'hamayashi_house')),count)
        guards.begin(s);win(s)
        self.assertEqual(len(guards.remaining(s,'hamayashi_house')),count-1)
        s['world']['minute']+=1440
        self.assertEqual(len(guards.remaining(s,'hamayashi_house')),count)
        clear(s,('hamayashi_house',),'rei:hamayashi');s['world']['minute']+=1440
        self.assertFalse(guards.remaining(s,'hamayashi_house','rei:hamayashi'))

    def test_recruitment_purchase_and_duplicate_protection(self):
        s=core.fresh('rei');import job_apps
        job_apps.ensure(s)['gang']=dict(name='Test crew',role='Founder',rank=0,standing=0,members={})
        venue='crew_lot_west';arrive(s,venue);s['world']['money']=100000
        guards.buy(s,venue,'Hideout');before=s['world']['money']
        with self.assertRaises(ValueError):guards.buy(s,venue,'Hideout')
        self.assertEqual(s['world']['money'],before)
        for kind in ('awakened','unawakened','robotic'):guards.recruit(s,'Named '+kind,kind,venue)
        self.assertEqual(s['world']['money'],before-16500)
        self.assertEqual(len(guards.slots(s,venue)),3)
        arrive(s,'crew_lot_south');guards.buy(s,'crew_lot_south','Affiliate')
        guards.station(s,guards.data(s)['roster'][0]['id'],'crew_lot_south')
        self.assertEqual(len(guards.slots(s,'crew_lot_south')),1)

    def test_tiers_equipment_and_real_combat(self):
        s=core.fresh('rei');arrive(s,'blackstone_hq')
        totals={}
        for faction,types in guards.DEPLOYMENTS.values():totals[faction]=totals.get(faction,0)+len(types)
        self.assertGreater(totals['syndicate'],totals['blackstone'])
        self.assertGreater(totals['shinokami'],totals['blackstone'])
        for kind in ('oni','pmc','spades','headhunter','team9'):
            p=guards.profile(s,kind)
            self.assertTrue(any(m['kind']=='equipment' for m in combat_moves.actions(p)))
        guards.begin(s,scope='test')
        f=combat.active(s)
        req=combat_engine.request(s,'utility:guard')
        combat_engine.resolve(s,req)
        self.assertGreater(f['turn'],0)
        combat.concede(s);combat.close(s)

    def test_interpol_guards_precede_original_target(self):
        s=core.fresh('fox');arrive(s,'interpol_hq')
        s['world']['cast']['gordon'].update(location='interpol_hq',journey=None,activity='Available')
        interpol.begin(s,'blackhaven')
        step=interpol.objective(s);arrive(s,step['venue'])
        s['world']['cast']['gordon'].update(location=step['venue'],journey=None,activity='Available')
        interpol.advance(s);interpol.advance(s)
        step_before=interpol.read(s)['files']['blackhaven']['step']
        for _ in range(2):
            interpol.advance(s);self.assertEqual(combat.active(s)['kind'],'guard');self.assertEqual(combat.active(s)['ally'],'gordon');win(s)
            self.assertEqual(interpol.read(s)['files']['blackhaven']['step'],step_before)
        interpol.advance(s);self.assertEqual(combat.active(s)['kind'],'interpol');win(s)
        self.assertEqual(interpol.read(s)['files']['blackhaven']['step'],step_before+1)

    def test_charles_requires_guard_and_boss_victories(self):
        s=core.fresh('garrett');s['charles_quest']=dict(charles.read(s),step=9)
        __import__('flashback_helpers').finish_memories(s)
        arrive(s,charles.LAB);s['world']['minute']=20*60
        for who,a in s['world']['cast'].items():
            if who not in ('garrett','charles') and a['location']==charles.LAB:a['location']='square'
        s['world']['cast']['charles'].update(location=charles.LAB,journey=None,activity='Available')
        with self.assertRaises(ValueError):charles.advance(s,0)
        while guards.remaining(s,charles.LAB,'charles:search'):charles.security_action(s);win(s)
        charles.security_action(s);combat.concede(s);combat.close(s)
        self.assertFalse(charles.reunited(s))
        with self.assertRaises(ValueError):charles.advance(s,0)
        charles.security_action(s);win(s)
        with patch('messaging.initiate'):charles.advance(s,0)
        self.assertTrue(charles.reunited(s))
        self.assertIn('charles',guards.data(s)['victories']['charles:finale'])

if __name__=='__main__':unittest.main()
