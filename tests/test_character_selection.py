import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import character_dossier as dossier
import character_origins as origins
import creator_drafts as drafts
import custom_library as library
import custom_protagonist as custom
import combat_profiles
import combat_moves
import game_core as core
import job_apps
import save_system
from test_custom_protagonist import PROFILE
from PIL import Image


class SelectionTests(unittest.TestCase):
    def test_authored_biographies_and_complete_known_facts(self):
        import character_biographies as bios
        import hidden_cast
        import story_calendar
        self.assertEqual(set(bios.BIOGRAPHIES), set(core.PLAYERS))
        for who in core.PLAYERS:
            p = dossier.starting(who)
            paragraphs = p['biography'].split('\n\n')
            self.assertEqual(len(paragraphs), 2, who)
            self.assertTrue(all(len(part.split()) >= 40 for part in paragraphs), who)
            self.assertIsInstance(p['details']['Age'], int, who)
            self.assertNotEqual(p['details']['Occupation / studies'], 'Unspecified', who)
            self.assertRegex(p['details']['MBTI'], r'^[IE][NS][FT][JP]', who)
            self.assertEqual(p['details']['Birthday'], story_calendar.BIRTHDAYS[who])
            if who in hidden_cast.CAST:
                height = hidden_cast.CAST[who]['height']
                self.assertEqual(p['details']['Height'], f'{height} cm' if isinstance(height, int) else height)
        for who, role in [('garrett','triad leader'),('rei','underground fighting champion'),('ivan','Syndicate executive')]:
            self.assertIn(role, dossier.starting(who)['details']['Occupation / studies'])
        self.assertEqual(dossier.starting('mavis')['details']['Birthday'], 'Unknown')
        self.assertEqual(dossier.starting('fox')['details']['Height'], 'Unspecified')
        import four_aces
        for who, person in four_aces.CAST.items():
            self.assertIn('Syndicate Ace of '+person['suit'], dossier.starting(who)['details']['Occupation / studies'])

    def test_edit_profile_conflict_and_explicit_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'saves'
            original=library.save_profile(PROFILE|{'portrait':'assets/generated/example.png'},root,separate=True)
            baseline=library.fingerprint(original)
            changed=library.save_profile(original|{'biography':'First edit'},root,expected=baseline)
            self.assertEqual(changed['profile_id'],original['profile_id'])
            with self.assertRaisesRegex(ValueError,'changed or was removed'):
                library.save_profile(original|{'biography':'Stale edit'},root,expected=baseline)
            separate=library.save_profile(original|{'biography':'Separate'},root,separate=True,expected=baseline)
            self.assertNotEqual(separate['profile_id'],original['profile_id'])
            self.assertIn(changed,library.enumerate_profiles(root)[0])

    def test_stale_draft_writes_preserve_latest_and_allow_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            old=drafts.save(root,drafts.new(),{'name':'Initial'})
            latest=drafts.autosave(root,old,{'name':'Other editor'})
            for operation in (lambda:drafts.autosave(root,old,{'name':'Stale'}),
                              lambda:drafts.save(root,old,{'name':'Stale'}),
                              lambda:drafts.pin(root,old,old['revisions'][0]['id'],True)):
                with self.assertRaisesRegex(ValueError,'another editor'): operation()
                self.assertEqual(drafts.read(root,old['id']),latest)
            copied=drafts.save(root,drafts.new(),{'name':'Stale'},'Independent copy')
            self.assertNotEqual(copied['id'],old['id'])

    def test_pinned_retention_failure_and_oldest_restore(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            doc = drafts.save(root, drafts.new(), {'name':'original'})
            ident = doc['revisions'][0]['id']
            doc = drafts.pin(root, doc, ident, True)
            for i in range(45): doc = drafts.save(root, doc, {'name':str(i)})
            self.assertIn(ident, [r['id'] for r in drafts.read(root,doc['id'])['revisions']])
            doc = drafts.autosave(root, doc, {'name':'working'})
            before = copy.deepcopy(doc)
            with patch.object(save_system,'atomic',side_effect=OSError('disk full')):
                with self.assertRaises(OSError): drafts.pin(root,doc,ident,False)
            self.assertEqual(doc,before)
            doc = drafts.pin(root,doc,ident,False)
            self.assertEqual(drafts.recovery(doc), {'name':'working'})
            doc = drafts.restore(root,doc,ident,{'name':'working'})
            self.assertEqual(doc['current'], {'name':'original'})
            self.assertTrue(any(r['snapshot']=={'name':'working'} for r in doc['revisions']))

    def test_canonical_preview_is_read_only_and_emily_matches(self):
        with patch.object(core,'save',side_effect=AssertionError('save')), patch.object(core,'request',side_effect=AssertionError('network')):
            for who in dict(core.PLAYERS):
                p=dossier.starting(who)
                self.assertEqual(p['combat']['stats'],combat_profiles.make(who)['stats'])
                for tab in ('Overview','Backstory','Details','Awakened'): self.assertTrue(dossier.text(p,tab))
            emily=dossier.starting('emily')
            self.assertEqual(emily['combat']['path']['stage'],'Ascension')
            self.assertIn('never prevents injury',emily['biography'])

    def test_saved_preview_preserves_progress_and_input(self):
        state=core.fresh('emily')
        combat_profiles.profile(state,'emily')['stats']['martial_skill']=92
        before=copy.deepcopy(state)
        p=dossier.saved(state,'slot-a')
        self.assertEqual(p['combat']['stats']['martial_skill'],92)
        self.assertEqual(state,before)
        self.assertIn('slot-a',p['label'])
        self.assertFalse(any(key.startswith('Starting ') for key in p['details']))
        state['job_apps']={'employment':'florist','jobs':{'florist':{'rank':2}},'heat':13,'reputation':9}
        p=dossier.saved(state,'job-slot')
        self.assertEqual(p['details']['Current employment'],job_apps.JOBS['florist']['ranks'][2])
        self.assertEqual(p['details']['Recorded reputation / heat'],'9 / 13')
        self.assertNotEqual(dossier.starting('emily')['combat']['stats']['martial_skill'],92)

    def test_read_only_library_duplicate_names_and_stable_edit(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'saves'
            raw=PROFILE|{'portrait':'assets/generated/example.png'}
            a=library.save_profile(raw,root,separate=True)
            b=library.save_profile(raw,root,separate=True)
            self.assertNotEqual(a['profile_id'],b['profile_id'])
            changed=library.save_profile(a|{'biography':'Public past.','private_history':'Private event.'},root)
            library.remember({'player':'custom_'+'a'*32,'custom_protagonist':a},root)
            files={p:p.read_bytes() for p in root.parent.rglob('*.json')}
            with patch.object(save_system,'atomic',side_effect=AssertionError('write')):
                profiles,errors=library.enumerate_profiles(root)
                self.assertEqual(len(profiles),2); self.assertFalse(errors)
            self.assertEqual(files,{p:p.read_bytes() for p in files})
            self.assertIn(changed,profiles)
            self.assertNotIn('Private event.',custom.background(changed))
            self.assertIn('Private event.',dossier.starting(a['profile_id'],changed)['biography'])
            (root.parent/'custom_characters'/'broken.json').write_text('{')
            self.assertEqual(len(library.enumerate_profiles(root)[1]),1)

    def test_draft_failure_and_reversible_restore(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder); doc=drafts.new(); one={'values':{'name':'One'}}; two={'values':{'name':'Two'}}
            doc=drafts.save(root,doc,one)
            revision=doc['revisions'][0]['id']
            doc=drafts.autosave(root,doc,two)
            self.assertEqual(drafts.recovery(drafts.read(root,doc['id'])),two)
            before=drafts.path(root,doc['id']).read_bytes()
            with patch.object(save_system,'atomic',side_effect=OSError('disk full')):
                with self.assertRaises(OSError): drafts.save(root,doc,two)
            self.assertEqual(before,drafts.path(root,doc['id']).read_bytes())
            doc=drafts.restore(root,doc,revision,two)
            self.assertIsNone(drafts.recovery(doc)); self.assertEqual(doc['current'],one)
            self.assertTrue(any(r['snapshot']==two for r in doc['revisions']))
            with self.assertRaises(ValueError): drafts.read(root,'../escape')

    def test_all_kits_exact_moves_and_no_reseed(self):
        for awakened in (False,True):
            for experience in origins.EXPERIENCES:
                arts,moves=origins.recommended(experience,['Boxing','Judo','Silat','Military CQC'],awakened)
                origin=origins.validate(dict(experience=experience,arts=arts,moves=moves))
                p=custom.validate(PROFILE|dict(awakened=awakened,awakening_trait='Sound',awakening_description='Bounded sound.',origin=origin))
                resolved=origins.resolve(origin,awakened)
                fighter=combat_profiles.make('custom_fixture',p)
                self.assertEqual(fighter['stats'],resolved['stats'])
                self.assertEqual(fighter['path']['stage'],resolved['stage'])
                self.assertEqual(set(fighter['moveset']['learned']),set(resolved['learned']))
                before=copy.deepcopy(fighter)
                combat_moves.initialise(fighter,'custom_fixture',p)
                self.assertEqual(fighter,before)
                self.assertEqual(fighter['path']['history'],[])
                if not awakened:
                    self.assertFalse(any(combat_moves.MOVES[m]['tier']=='master' for m in fighter['moveset']['learned']))

    def test_all_jobs_ranks_and_criminal_presets(self):
        for job in job_apps.JOBS:
            previous=-1
            for rank in range(4):
                result=origins.resolve(dict(job=job,job_rank=rank),True)
                self.assertEqual(result['employment']['title'],job_apps.JOBS[job]['ranks'][rank])
                self.assertGreater(result['stats']['fight_iq'],previous)
                previous=result['stats']['fight_iq']
        for crime in origins.CRIME:
            organisation=('Clubs' if crime in ('Established faction member','Faction specialist','Faction field leader') else
                          'lantern' if crime in ('Trusted crew member','Crew lieutenant','Crew captain') else None)
            resolved=origins.resolve(dict(crime=crime,organisation=organisation,experience='Exceptional Veteran'),True)
            self.assertEqual(resolved['experience'],'Exceptional Veteran')
            self.assertEqual(resolved['choices']['crime'],crime)

    def test_origin_once_story_isolation(self):
        with tempfile.TemporaryDirectory(dir=core.ROOT/'assets'/'generated') as folder:
            path=Path(folder)/'portrait.png'
            image=Image.new('RGBA',(8,8)); image.putpixel((4,4),(90,90,90,255)); image.save(path)
            values=PROFILE|{'origin':dict(job='florist',job_rank=3,crime='Faction specialist',organisation='Diamonds')}
            state=custom.create(values,path.relative_to(core.ROOT).as_posix())
            d=job_apps.ensure(state)
            self.assertEqual(d['jobs']['florist']['shifts'],0)
            self.assertEqual(d['membership']['assignments'],0)
            self.assertEqual(d['membership']['rank'],2)
            d['heat']=23; d['reputation']=7; d['employment']=None; state['world']['money']=2
            before=copy.deepcopy(state); origins.apply(state)
            self.assertEqual(state,before)
            custom.restore(json.loads(json.dumps(state)))
            self.assertEqual(state,before)


if __name__=='__main__': unittest.main()
