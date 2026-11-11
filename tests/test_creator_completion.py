import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from PIL import Image
import creator_writing as writing
import character_packages as packages
import character_identity as identity
import creator_combat as kits
import combat_profiles
import combat_moves
import combat_workshop as workshop
import character_origins as origins
import custom_protagonist as custom
import game_core as core
from test_custom_protagonist import PROFILE
from test_enhanced_combat import AMP


def armed():
    arts,learned=origins.recommended('Veteran',['Boxing','Judo'])
    return PROFILE|dict(awakened=True,awakening_trait='Resonance',awakening_description='Contact sound pressure with finite range and cost.',
                        trait_amplifications=workshop.validate_amplifications([AMP]),
                        origin=dict(experience='Veteran',arts=arts,moves=learned))


class CompletionTests(unittest.TestCase):
    def test_awakened_without_trait_is_valid_and_distinct(self):
        p=custom.validate(PROFILE|dict(awakened=True,trait_enabled=False,origin=dict(experience='Veteran',arts=['Boxing'])))
        combat=combat_profiles.make('custom_traitless',p)
        self.assertTrue(combat['awakened']); self.assertIsNone(combat['trait'])
        self.assertEqual(combat['stats']['trait_refinement'],0)
        self.assertFalse(combat['moveset']['amplifications']); self.assertFalse(combat['moveset']['unique'])

    def test_professional_contributions_and_branch_boundaries(self):
        base=origins.resolve({},True)
        for job in __import__('job_apps').JOBS:
            previous=base['stats']
            for rank in range(4):
                p=dict(job=job,job_rank=rank)
                result=origins.resolve(p,True)
                self.assertTrue(all(result['stats'][k]>previous[k] for k in previous))
                duplicate=origins.resolve(p|dict(prior_job=job,prior_rank=rank),True)
                self.assertEqual(result['stats'],duplicate['stats']); previous=result['stats']
        for background in origins.BACKGROUNDS: origins.resolve(dict(background=background),False)
        for branch in __import__('job_apps').BRANCHES:
            for crime in ('Established faction member','Faction specialist','Faction field leader'):
                result=origins.resolve(dict(organisation=branch,crime=crime),True)
                self.assertEqual(result['choices']['organisation'],branch)

    def test_locks_format_and_age_conflicts_preserve_source(self):
        s=dict(values=dict(age='25'),extra=dict(biography='Born in Brisbane. A careful artist.'),writing=dict(locks=[dict(field='biography',mode='Exact',text='Born in Brisbane.')]))
        before=copy.deepcopy(s)
        for value,mode in [('A fighter.','Rewrite'),('Born in Brisbane. A 30-year-old artist.','Rewrite'),('Born in Brisbane. A famous artist.','Format')]:
            with self.assertRaises(ValueError): writing.apply(s,'biography',value,mode)
        self.assertEqual(s,before)
        result=writing.apply(s,'biography','Born in Brisbane.\nA careful artist.','Format')
        self.assertEqual(result['writing'],s['writing'])

    def test_randomisation_and_stale_lifecycle(self):
        s=dict(values=dict(mbti='INFP',hairstyle='Long',interests='Art'),writing=dict(locks=[dict(field='mbti',mode='Fact',text='INFP')]))
        new=writing.randomise(s,['mbti','hairstyle'],4)
        self.assertEqual(new['values']['mbti'],'INFP'); self.assertEqual(new['values']['interests'],'Art')
        self.assertNotEqual(writing.token(s,'a',1),writing.token(s,'a',2))
        self.assertNotEqual(writing.token(s,'a',1),writing.token(s,'b',1))

    def test_provider_is_explicit_and_format_cannot_add_facts(self):
        s=dict(values=dict(name='Alex',age='25'),extra=dict(biography='An artist.'))
        with patch('combat.ask_ai',return_value={'text':'An artist.\n'}) as provider:
            result=writing.propose(s,'biography','Format'); self.assertEqual(provider.call_count,1)
            writing.apply(s,'biography',result,'Format')
        with patch('combat.ask_ai',side_effect=RuntimeError('Offline')):
            with self.assertRaises(RuntimeError): writing.propose(s,'biography','Expand')
        self.assertEqual(s['extra']['biography'],'An artist.')

    def test_identity_and_sample_do_not_send_private_fields(self):
        p=PROFILE|dict(identity=dict(public_name='River',alias='Night Owl',legal_public=False),private_history='SECRET',biography='An artist.')
        view=identity.visible(p); self.assertNotIn('Alex Rivers',json.dumps(view)); self.assertNotIn('SECRET',json.dumps(view))
        self.assertEqual(identity.visible(p,'underworld')['name'],'Night Owl')
        s=dict(custom_protagonist=p,world=dict(job='Chef')); before=copy.deepcopy(s)
        with patch('combat.ask_ai',return_value={'text':'Hello, River.'}) as ai:
            writing.sample(p,[dict(role='user',text='Hello')])
            self.assertNotIn('SECRET',ai.call_args.args[0]); self.assertNotIn('Night Owl',ai.call_args.args[0])
        self.assertEqual(s,before)
        identity.disclose(s,'neo','history'); self.assertEqual(identity.dialogue(s,'neo')['disclosed_history'],'SECRET')
        self.assertNotIn('disclosed_history',identity.dialogue(s,'rei'))
        self.assertEqual(identity.dialogue(json.loads(json.dumps(s)),'neo')['employment'],'Chef')

    def test_packages_roundtrip_privacy_and_untrusted_approval(self):
        with tempfile.TemporaryDirectory(dir=custom.ROOT/'assets'/'generated') as directory:
            root=Path(directory); image=root/'portrait.png'; picture=Image.new('RGBA',(8,8),(1,2,3,0)); picture.putpixel((4,4),(1,2,3,255)); picture.save(image)
            p=armed()|dict(portrait=image.relative_to(custom.ROOT).as_posix(),private_history='SECRET',identity=dict(public_name='River',alias='Owl',legal_public=False))
            for private in (False,True):
                out=root/str(private); packages.export(p,out,private); result=packages.inspect(out)['profile']
                self.assertEqual(bool(result.get('private_history')),private)
                self.assertNotIn('trait_amplifications',result); self.assertNotIn('profile_id',result)
                if not private: self.assertEqual(result['name'],'River'); self.assertFalse(result['identity']['alias'])
            self.assertEqual(p['private_history'],'SECRET')
            with self.assertRaises(FileExistsError): packages.export(p,out,True)

    def test_package_paths_versions_and_bad_images(self):
        with tempfile.TemporaryDirectory() as directory:
            target=Path(directory)/'bad'
            for extra in ('../portrait.png','script.exe','folder/portrait.png'):
                with zipfile.ZipFile(target,'w') as z:
                    z.writestr('character.json','{}'); z.writestr(extra,b'bad')
                with self.assertRaises(ValueError): packages.inspect(target)
            with zipfile.ZipFile(target,'w') as z:
                z.writestr('character.json',json.dumps(dict(format='MH-character',version=99,profile=PROFILE))); z.writestr('portrait.png',b'bad')
            with self.assertRaises(ValueError): packages.inspect(target)
            for manifest in ([],None,dict(format='MH-character',version=True)):
                with zipfile.ZipFile(target,'w') as z:
                    z.writestr('character.json',json.dumps(manifest)); z.writestr('portrait.png',b'bad')
                with self.assertRaises(ValueError): packages.inspect(target)

    def test_origin_founder_returning_and_credentials(self):
        with tempfile.TemporaryDirectory(dir=custom.ROOT/'assets'/'generated') as directory:
            image=Path(directory)/'p.png'; picture=Image.new('RGBA',(8,8),(1,2,3,0)); picture.putpixel((4,4),(1,2,3,255)); picture.save(image)
            p=PROFILE|dict(origin=dict(crime='Small-crew founder',crew_name='Evening Birds',prior_job='photographer',prior_rank=3))
            s=custom.create(p,image.relative_to(custom.ROOT).as_posix())
            self.assertIsNone(s['job_apps']['employment']); self.assertEqual(s['job_apps']['gang']['role'],'Founder')
            prior=s['job_apps']['jobs']['photographer']; self.assertEqual(prior['shifts'],0); self.assertTrue(prior['origin_portfolio'])
            self.assertIn('leadership',prior['certificates']); before=copy.deepcopy(s); origins.apply(s); self.assertEqual(s,before)

    def test_signature_validation_seeding_and_no_cooldown(self):
        p=armed(); amp=p['trait_amplifications'][0]['id']
        raw=[dict(name='Echo '+str(i),description='Contact sound strike.',role='attack',tags=['precision'],aspects=[amp],range=1,stamina=9+i,mana=12,hits=1,environment='Contact only',setup='None',counter='Guard',counter_kind='none') for i in range(3)]
        with patch('combat.ask_ai',return_value={'skills':raw}): batch=kits.generate(p,'attack','silver rings')
        self.assertEqual(len(batch['candidates']),3)
        clones=copy.deepcopy(batch['candidates'])
        for candidate in clones: candidate['stamina']=9
        with self.assertRaises(ValueError): kits.distinct_candidates(clones)
        p['starting_signature']=kits.accept(p,batch,1)
        validated=custom.validate(p); state=kits.sandbox(validated)
        cp=state['combat']['profiles']['custom_practice']; self.assertEqual(len(cp['moveset']['unique']),1)
        self.assertNotIn('workshops',state['combat'])
        for _ in range(3): combat_profiles.profile(state,'custom_practice')
        self.assertEqual(len(cp['moveset']['unique']),1)
        bad=copy.deepcopy(p); bad['starting_signature']['skill']['mana']=0
        with self.assertRaises(ValueError): custom.validate(bad)
        bad=copy.deepcopy(p); bad['awakening_description']='Changed domain'
        with self.assertRaises(ValueError): custom.validate(bad)

    def test_signature_role_and_tier_restrictions(self):
        p=armed(); p['origin']['experience']='Newcomer'; p['origin']['arts']=[]; p['origin']['moves']=[]
        with self.assertRaises(ValueError): kits.signature_context(p)
        p=armed(); p['trait_amplifications'][0]['compatible']=['attack']
        with self.assertRaises(ValueError): kits.generate(p,'counter')

    def test_practice_has_no_world_or_progress_mutations(self):
        p=armed(); before=copy.deepcopy(p); s=kits.sandbox(p)
        path=copy.deepcopy(s['combat']['profiles']['custom_practice']['path'])
        with patch('combat.complete_exchange',side_effect=AssertionError('live completion')),patch('combat_identity.observe',side_effect=AssertionError('knowledge')):
            for _ in range(3): kits.exchange(s,'utility:recover')
        self.assertEqual(s['world']['minute'],0); self.assertEqual(p,before)
        self.assertEqual(s['combat']['profiles']['custom_practice']['path'],path)
        self.assertNotIn('workshops',s['combat'])

    def test_interaction_matches_selection_and_specialisation(self):
        p=armed(); p['specialisation']=p['trait_amplifications'][0]['id']; cp=combat_profiles.make('custom_test',p)
        m=cp['moveset']['learned'][0]; a=cp['moveset']['amplifications'][0]
        explained=kits.interaction(cp,m,a['id']); actual=combat_moves.selection(cp,m,a['id'])
        for k,v in explained['amplified'].items(): self.assertEqual(actual[k],v)
        self.assertEqual(a['mana'],7); self.assertEqual(p['trait_amplifications'][0]['mana'],8)

    def test_authored_activities_are_atomic_once_only_and_private(self):
        import trait_activities as activities,autonomy
        s=core.fresh('garrett'); p=combat_profiles.profile(s,'garrett'); p['moveset']['amplifications']=workshop.validate_amplifications([AMP])
        s['world']['location']='park'; before=copy.deepcopy(s)
        with self.assertRaises(ValueError): activities.execute(s,'work_precision','work')
        self.assertEqual(s,before)

    def test_work_application_cost_access_and_bounded_outcome(self):
        import trait_activities as activities,job_apps,autonomy
        s=core.fresh('garrett'); p=combat_profiles.profile(s,'garrett'); p['moveset']['amplifications']=workshop.validate_amplifications([AMP])
        job_apps.apply(s,'barista'); venue=job_apps.JOBS['barista']['venue']
        s['world']['location']=venue; s['world']['cast']['garrett'].update(location=venue,journey=None)
        s['world']['minute']=job_apps.JOBS['barista']['hours'][0]*60
        before=copy.deepcopy(s); craft=job_apps.profile(s,'barista')['craft']; money=s['world']['money']
        result=activities.execute(s,'work_precision','work-one')
        self.assertEqual(job_apps.profile(s,'barista')['craft'],craft+1); self.assertEqual(s['world']['money'],money)
        self.assertEqual(job_apps.profile(s,'barista')['shifts'],0)
        after=copy.deepcopy(s); self.assertEqual(activities.execute(s,'work_precision','work-one'),result); self.assertEqual(s,after)
        self.assertGreater(s['world']['minute'],before['world']['minute'])
        s['world']['location']='park'; s['world']['cast']['garrett'].update(location='park',journey=None)
        result=activities.execute(s,'explore_observe','one'); after=copy.deepcopy(s)
        self.assertEqual(activities.execute(s,'explore_observe','one'),result); self.assertEqual(s,after)
        reloaded=json.loads(json.dumps(s))
        with self.assertRaises(ValueError): activities.execute(reloaded,'explore_observe','two')
        s=core.fresh('garrett'); s['world']['location']='park'; s['world']['cast']['garrett'].update(location='park',journey=None); autonomy.person(s,'garrett')['energy']=0
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError): activities.execute(s,'explore_observe','low')
        self.assertEqual(s,before)


if __name__=='__main__': unittest.main()
