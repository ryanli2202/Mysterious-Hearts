import copy
import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as core
import combat
import interpol as law
import interpol_cast
import four_aces
import phone_numbers
import grove
import grove_accounts
import town
from combat_profiles import profile


def locate(s,place,*people,minute=None):
    if minute is not None:s['world']['minute']=minute
    s['world']['location']=place
    s['world']['npcs']=[]
    for who in (s['player'],*people):s['world']['cast'][who].update(location=place,journey=None,activity='Available')


class InterpolTests(unittest.TestCase):
    def test_playable_profiles_and_stable_numbers(self):
        for who in interpol_cast.IDS:
            s=core.fresh(who)
            self.assertEqual(s['world']['location'],who+'_home')
            self.assertIn(who,core.PLAYERS)
            self.assertEqual(profile(s,who)['path']['stage'],'Totality')
            self.assertTrue(profile(s,who)['trait'])
            self.assertIn('Interpol',core.lore.character_tables()[who]['World knowledge'])
        self.assertGreater(int(phone_numbers.NUMBERS['fox']),int(phone_numbers.NUMBERS['charles']))
        self.assertEqual(grove.profile(core.fresh('fox'),'fox')['handle'],'')
        with self.assertRaises(ValueError):grove_accounts.require(core.fresh('fox'))

    def test_gordon_spot_fine_and_deduplication(self):
        s=core.fresh('garrett');locate(s,'blackhaven','gordon','rei')
        i=law.record_offence(s,'assault','rei',event_id='one-assault')
        self.assertEqual(i['status'],'fined')
        self.assertIn('on the spot',law.read(s)['fines'][0]['issuer'])
        law.record_offence(s,'assault','rei',event_id='one-assault')
        self.assertEqual(len(law.read(s)['fines']),1)
        law.tick(s);self.assertEqual(law.debt(s),800)

    def test_fox_discretion_and_civilian_limit(self):
        s=core.fresh('fox');locate(s,'blackhaven','gordon','ivan','emily')
        self.assertEqual(law.record_offence(s,'assault','ivan')['status'],'discretion')
        self.assertEqual(law.debt(s),0)
        self.assertEqual(law.record_offence(s,'assault','emily')['status'],'fined')
        self.assertEqual(law.debt(s),800)

    def test_attacking_the_commander_revokes_field_clearance(self):
        s=core.fresh('fox');locate(s,'interpol_hq','gordon')
        combat.start(s,'gordon','attack');combat.finish(s,'Conceded');combat.close(s)
        self.assertFalse(law.clearance(s,'fox'))
        self.assertEqual(combat.affiliation(s,'fox'),(None,0))
        with self.assertRaises(ValueError):law.enrol(s)
        with self.assertRaises(ValueError):law.begin(s,'blackhaven')
        with self.assertRaises(ValueError):town.travel(s,'interpol_briefing')

    def test_delayed_review_and_partial_payment(self):
        s=core.fresh('rei');locate(s,'rei_home')
        for who,actor in s['world']['cast'].items():
            if who!='rei':actor['location']='square'
        i=law.record_offence(s,'theft',event_id='private-unseen')
        self.assertEqual(i['status'],'unreported')
        law.record_offence(s,'coercion',documented=True)
        self.assertEqual(law.debt(s),0)
        s['world']['minute']+=60;law.tick(s);law.tick(s)
        self.assertEqual(law.debt(s),500)
        s['world']['money']=123;fine=law.read(s)['fines'][0]
        law.pay(s,fine['id']);self.assertEqual(law.debt(s),377);self.assertEqual(s['world']['money'],0)
        s['world']['money']=400;law.pay(s,fine['id']);self.assertEqual(law.debt(s),0)
        with self.assertRaises(ValueError):law.pay(s,fine['id'])

    def test_combat_attack_hook_but_not_spar(self):
        s=core.fresh('garrett');locate(s,'blackhaven','rei','gordon')
        combat.start(s,'rei','spar');combat.finish(s,'done');combat.close(s)
        self.assertFalse(law.read(s).get('incidents'))
        combat.start(s,'rei','attack')
        self.assertEqual(law.debt(s),800)
        self.assertIn('rei',s['combat']['ruptures'])

    def test_presence_gates_and_restricted_rooms(self):
        s=core.fresh('rei')
        with self.assertRaises(ValueError):law.enrol(s)
        with self.assertRaises(ValueError):town.travel(s,'interpol_briefing')
        locate(s,'interpol_hq');law.enrol(s)
        with self.assertRaises(ValueError):law.begin(s,'crow_operation')
        locate(s,'interpol_hq','gordon');law.begin(s,'blackhaven')
        self.assertTrue(core.hidden.contact(s,'gordon'))
        self.assertTrue(phone_numbers.saved_number(s,'gordon'))
        with self.assertRaises(ValueError):law.advance(s)
        law.travel_objective(s);self.assertTrue(law.here(s,'gordon'))
        law.advance(s);self.assertEqual(law.read(s)['files']['blackhaven']['step'],1)

    def test_gordon_team_travel_and_reload(self):
        s=core.fresh('gordon');locate(s,'interpol_hq','fox',minute=13*60)
        law.begin(s,'blackhaven');law.travel_objective(s)
        self.assertTrue(law.here(s,'fox'))
        self.assertIsNone(s['world']['cast']['fox']['journey'])
        restored=json.loads(json.dumps(s));law.advance(restored)
        self.assertEqual(law.read(restored)['files']['blackhaven']['step'],1)

    def test_fox_cannot_queue_public_reactions(self):
        import phone_apps as apps
        import grove_reactions
        s=core.fresh('gordon');data=apps.ensure(s)
        with self.assertRaises(ValueError):apps.queue_grove(s,'fox')
        post=apps._append(data,'gordon','An ordinary evening.',s['world']['minute'])
        post['image']='sample.png'
        data['grove_reactions']=[dict(post=post['id'],author='fox',kind='like',due=0)]
        grove_reactions.sync(s,data)
        self.assertNotIn('fox',post.get('liked_by',[]))
        self.assertFalse(any(j['author']=='fox' for j in data['grove_pending']))

    def test_operation_support_uses_real_trait_resources(self):
        s=core.fresh('fox');locate(s,'interpol_hq','gordon');law.begin(s,'blackhaven')
        law.travel_objective(s);law.advance(s);law.advance(s);law.advance(s)
        f=combat.active(s);self.assertEqual(f['ally'],'gordon')
        before=f['ally_resources']['energy']
        plan,_=combat.tactics.prepare(s)
        result=dict(fight_id=f['id'],turn=0,action='Guard while Gordon covers the witness.',style='Military CQC',mode='Guard',
            judgement=dict(player_feasible=True,complexity=40,advantage=0,enemy_mode=plan['mode'],enemy_art=plan['art'],enemy_action=plan['action'],reason='Physical observations support the attempt.'))
        combat.commit_turn(s,result)
        self.assertLess(f['ally_resources']['energy'],before)
        self.assertTrue(any('supports the operation' in line for line in f['log']))
        self.assertEqual(law.debt(s),0)
        combat.concede(s);combat.close(s)
        self.assertEqual(law.read(s)['files']['blackhaven']['step'],2)
        self.assertEqual(law.read(s)['files']['blackhaven']['attempts'],1)
        self.assertGreater(law.regroup_delay(s),0)
        law.regroup(s);self.assertEqual(law.regroup_delay(s),0)

    def test_full_campaign_reveals_in_order_and_roundtrips(self):
        s=core.fresh('fox')
        for key,spec in law.CASES.items():
            locate(s,'interpol_hq','gordon',minute=max(s['world']['minute'],8*60))
            law.begin(s,key)
            while law.read(s)['active']:
                step=law.objective(s)
                if s['world']['location']!=step['venue']:law.travel_objective(s)
                law.advance(s)
                if step['kind']=='combat':
                    f=combat.active(s)
                    if step.get('opponent'):
                        self.assertTrue(law.here(s,step['opponent']))
                        self.assertEqual(f['opponent_profile']['name'],step['enemy'])
                    combat.finish(s,'Victory — secured objective.')
                    combat.close(s)
                s=json.loads(json.dumps(s));core.town.ensure(s);combat.ensure(s)
            self.assertTrue(law.read(s)['files'][key]['complete'])
            if spec.get('reveal'):
                self.assertTrue(law.known_identity(s,'fox',spec['reveal']))
                self.assertTrue(law.known_identity(s,'gordon',spec['reveal']))
                self.assertFalse(law.known_identity(s,'emily',spec['reveal']))
        self.assertTrue(four_aces.knows_identities(s,'fox'))
        self.assertEqual(law.read(s)['custody']['crow']['location'],'interpol_containment')
        self.assertFalse(core.hidden.hq_access(s,'fox'))
        self.assertEqual(law.debt(s),0)
        self.assertEqual(len(law.read(s)['files']),9)

    def test_support_recovers_low_mana_and_respects_player_knockout(self):
        s=core.fresh('fox');locate(s,'interpol_hq','gordon');law.begin(s,'blackhaven')
        law.travel_objective(s);law.advance(s);law.advance(s);law.advance(s)
        f=combat.active(s);f['ally_resources']['energy']=17
        law.support_turn(s,f,random.Random(2))
        self.assertGreater(f['ally_resources']['energy'],17)
        f['player']['health']=0;before=copy.deepcopy(f['ally_resources'])
        law.support_turn(s,f,random.Random(3))
        self.assertEqual(f['ally_resources'],before)

    def test_one_reveal_does_not_leak_other_aces(self):
        s=core.fresh('fox');law.reveal(s,['fox'],'martos','test corroboration')
        self.assertFalse(four_aces.knows_identities(s,'fox'))
        self.assertNotIn('Martos',str(law.context(s,'fox',['emily'])))
        locate(s,'blackhaven','emily');law.share_identity(s,'emily','martos')
        text=str(law.context(s,'fox',['emily']))
        self.assertIn('Ace of Clubs',text);self.assertNotIn('Camila',text)
        with self.assertRaises(ValueError):law.share_identity(s,'emily','camila')
        import bubblegram_progression
        directory='\n'.join(bubblegram_progression.directory(s))
        self.assertIn('Martos Cabrera',directory);self.assertNotIn('Camila Lopez',directory)

    def test_discoveries_do_not_grant_insider_history(self):
        s=core.fresh('fox')
        for who in four_aces.IDS:law.reveal(s,['fox','gordon'],who,'case')
        context=four_aces.private_context('fox',['gordon'],s)
        self.assertIn('Established case discoveries',context)
        self.assertNotIn('Private Ace knowledge',context)

    def test_new_character_art_and_appearance_paths(self):
        from PIL import Image
        import character_appearance
        from messages_ui import PROFILE_DIR
        for who in interpol_cast.IDS:
            self.assertEqual(character_appearance.reference(who)['Recognisable features'],interpol_cast.CAST[who]['appearance'])
            with Image.open(PROFILE_DIR/(who+'.png')) as contact:
                self.assertEqual(contact.width,contact.height)
            with Image.open(core.ROOT/'assets/portraits'/(who+'-selection.png')) as portrait:
                self.assertEqual(portrait.mode,'RGBA')
                self.assertEqual(portrait.getpixel((0,0))[3],0)

    def test_old_save_additive_migration(self):
        s=core.fresh('rei');before=copy.deepcopy(s['world'])
        law.ensure(s);law.ensure(s)
        self.assertEqual(s['world'],before);self.assertEqual(law.debt(s),0)
        self.assertFalse(law.read(s)['files'])

    def test_pre_update_save_loads_without_reseeding_progress(self):
        s=core.fresh('rei');s['world']['money']=4321
        s['routes']['emily']['memory']='A retained conversation.'
        for who in interpol_cast.IDS:
            for bucket in ('routes','friendships','relationships','discoveries'):
                s.get(bucket,{}).pop(who,None)
            s['world']['cast'].pop(who,None)
            s.get('contact_profiles',{}).get('people',{}).pop(who,None)
        s.pop('interpol',None)
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'pre-interpol.json';core.save(s,path);loaded=core.load(path)
        self.assertEqual(loaded['world']['money'],4321)
        self.assertEqual(loaded['routes']['emily']['memory'],'A retained conversation.')
        for who in interpol_cast.IDS:
            self.assertIn(who,loaded['world']['cast']);self.assertIn(who,loaded['routes'])
            self.assertFalse(core.hidden.contact(loaded,who))
        self.assertEqual(law.debt(loaded),0)

    def test_biocreation_and_senses_have_distinct_costs(self):
        import combat_profiles as cp
        g=cp.make('gordon');f=cp.make('fox');r=combat.resources(g);t=combat.resources(f)
        combat.strike(g,f,r,t,'Trait','Military CQC',40,0,random.Random(1),0,False)
        self.assertEqual(r['max_energy']-r['energy'],19)
        self.assertEqual(t['max_energy']-t['energy'],3)


if __name__=='__main__':unittest.main()
