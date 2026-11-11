import copy
import json
import unittest
from unittest.mock import patch
import game_core as core
import groups
import guard_dialogue as gd
import organisation_guards as guards
import phone_numbers
from test_major_campaigns import arrive

class GuardDialogueTests(unittest.TestCase):
    def setUp(self):
        def reply(path, body):
            name=body['format']['properties']['lines']['items']['properties']['speaker']['enum'][0]
            return {'message':{'content':json.dumps(dict(narration='',lines=[dict(speaker=name,text='The visitor area is beside reception.')]))}}
        self.provider=patch.object(core,'request',side_effect=reply).start()
        self.addCleanup(patch.stopall)

    def state(self, player='rei', venue='site_04'):
        s=core.fresh(player);s.setdefault('job_apps',{});s.setdefault('rei_story',{});arrive(s,venue);guards.refresh(s)
        return s,next(iter(guards.npc_rows(s)))

    def test_guide_coverage_and_all_types_converse_without_contacts(self):
        self.assertTrue(set(guards.TYPES)<=gd.GUIDES.keys())
        for venue in guards.DEPLOYMENTS:
            s,_=self.state(venue=venue)
            for name in guards.npc_rows(s):
                gid=groups.open_local(s,name)
                result=gd.generate(s,name,gd.TOPICS['Directions'])
                groups.commit(s,gid,gd.TOPICS['Directions'],result)
                groups.sync_contacts(s);phone_numbers.ensure(s)
                self.assertNotIn(name,s.get('npc_chats',{}))
                self.assertNotIn('npc:'+name,s['groups'])
                self.assertNotIn(name,s['phone_numbers']['contacts'])
                with self.assertRaises(ValueError):groups.require_text_available(s,[name])
                with self.assertRaises(ValueError):groups.create_text(s,'test',[name,'rei'])

    def test_syndicate_descriptions_and_generated_context_match_masked_art(self):
        for kind in ('clubs','spades','affiliate'):
            with self.subTest(kind=kind):
                s,_=self.state()
                name=next(n for n,r in guards.npc_rows(s).items() if r['type']==kind)
                description=guards.npc_detail(s,name)[2]
                self.assertIn(guards.APPEARANCES[kind],description)
                self.assertIn('full-face',description.lower())
                groups.open_local(s,name)
                gd.generate(s,name,'What equipment are you wearing?')
                messages=self.provider.call_args.args[1]['messages']
                context=json.loads(messages[1]['content'])
                self.assertEqual(context['guard_appearance'],guards.APPEARANCES[kind])
                self.assertIn(guards.MASKED_PRESENTATION,messages[0]['content'])
                self.assertIn('older history',messages[0]['content'])
                profile=guards.profile(s,kind)
                profile.pop('appearance')
                profile.pop('portrait')
                self.assertEqual(guards.appearance_for_profile(profile),guards.APPEARANCES[kind])

    def test_yakuza_appearance_keeps_human_faces_and_robot_identity(self):
        for kind in ('kai_sentinel','kai_guard','yokai','tengu','oni'):
            with self.subTest(kind=kind):
                s,_=self.state(venue='hamayashi_house' if kind.startswith('kai_') else 'site_01')
                name=next(n for n,r in guards.npc_rows(s).items() if r['type']==kind)
                self.assertIn(guards.APPEARANCES[kind],guards.npc_detail(s,name)[2])
                self.assertNotIn(guards.MASKED_PRESENTATION,guards.npc_detail(s,name)[2])
                groups.open_local(s,name)
                gd.generate(s,name,'Describe your uniform.')
                messages=self.provider.call_args.args[1]['messages']
                self.assertEqual(json.loads(messages[1]['content'])['guard_appearance'],guards.APPEARANCES[kind])
                self.assertNotIn(guards.MASKED_PRESENTATION,messages[0]['content'])
                profile=guards.profile(s,kind)
                profile.pop('appearance');profile.pop('portrait')
                self.assertEqual(guards.appearance_for_profile(profile),guards.APPEARANCES[kind])

    def test_combat_narration_receives_current_mask_and_equipment(self):
        import combat
        import combat_engine as engine
        for kind in ('clubs','spades','affiliate'):
            s,_=self.state()
            guards.start(s,'design:'+kind,guards.profile(s,kind),'design-test')
            # Older saved fights do not contain the newly authored appearance field.
            combat.active(s)['opponent_profile'].pop('appearance')
            with patch('world_loop.advance'):
                record=engine.resolve(s,engine.request(s,'utility:guard'))
            self.assertEqual(record['opponent_appearance']['description'],guards.APPEARANCES[kind])
            with patch.object(combat,'ask_ai',return_value={}) as provider:
                with self.assertRaises(ValueError):engine.narrate(record)
            prompt=provider.call_args.args[0]
            self.assertIn(guards.APPEARANCES[kind],prompt)
            self.assertIn(guards.MASKED_PRESENTATION,prompt)

    def test_absolute_command_and_ace_exceptions(self):
        s,name=self.state();r=gd.row(s,name)
        for who in ('ivan','sylvanis','crow'):
            self.assertTrue(gd.authority(s,who,r)['can_command'])
        for who in ('ivan','sylvanis'):
            for ace in gd.ACES:
                self.assertFalse(gd.authority(s,who,r,target=ace)['can_command'])
        for ace in gd.ACES:
            a=gd.authority(s,ace,r)
            self.assertFalse(a['can_command']);self.assertEqual(a['respect'],'undying');self.assertEqual(a['fear'],'high')
        for venue in guards.BLACKSTONE:
            s,name=self.state(venue=venue)
            for r in guards.npc_rows(s).values():self.assertTrue(gd.authority(s,'Joseph Richter',r)['can_command'])
        self.assertFalse(gd.authority(s,'ivan',r)['can_command'])

    def test_other_leaders_members_and_civilians(self):
        import gang_leaders
        for faction,spec in gang_leaders.LEADERS.items():
            s,name=self.state(venue=spec['base']);r=gd.row(s,name)
            self.assertTrue(gd.authority(s,spec['name'],r)['can_command'])
        for leader,venue in (('takeo','site_01'),('gordon','interpol_hq'),('garrett','syndicate')):
            s,name=self.state(venue=venue);self.assertTrue(gd.authority(s,leader,gd.row(s,name))['can_command'])
        s,name=self.state(venue='hamayashi_house');s['rei_story']['hamayashi']='lead';r=gd.row(s,name)
        self.assertTrue(gd.authority(s,'rei',r)['can_command']);self.assertFalse(gd.authority(s,'Daichi Kurose',r)['can_command'])
        s,name=self.state();r=gd.row(s,name)
        self.assertEqual(gd.authority(s,'emily',r)['category'],'civilian')
        self.assertEqual(gd.authority(s,'takeo',r)['category'],'outside leader')
        s['job_apps']['membership']=dict(faction='Syndicate',branch='Clubs',rank=2)
        self.assertTrue(gd.authority(s,'rei',r)['can_command'])
        s['combat']['expelled']=['syndicate'];self.assertFalse(gd.authority(s,'rei',r)['can_command'])

    def test_stable_post_shift_and_rename(self):
        s,name=self.state();gid=groups.open_local(s,name);key=s['groups'][gid]['guard_session']
        s['world']['minute']+=1440
        with self.assertRaises(ValueError):gd.active(s,name)
        groups.reconcile(s);self.assertIsNone(s['active_group'])
        new=groups.open_local(s,name);self.assertNotEqual(key,s['groups'][new]['guard_session'])
        arrive(s,'site_05');guards.refresh(s)
        other=groups.open_local(s,next(iter(guards.npc_rows(s))))
        self.assertNotEqual(key,s['groups'][other]['guard_session'])

    def test_legacy_migration_preserves_history_and_normal_contacts(self):
        s,name=self.state();s['npc_chats']={name:dict(history=[dict(speaker=name,text='Old guard line')]),'Theo':dict(history=[])}
        s['groups']['npc:'+name]=dict(channel='text',members=[name],history=[dict(text='Old text')])
        s['groups']['mixed']=dict(channel='text',members=[name,'Theo'],history=[dict(text='Keep this')])
        s['active_group']='npc:'+name;s['last_hangout']='npc:'+name
        import messaging
        messaging.thread(s,'npc:'+name,True)['reason']=dict(text='old pending message')
        s['phone_numbers']=dict(directory={name:'12025559999'},contacts={name:dict(number='12025559999')})
        groups.sync_contacts(s)
        before=copy.deepcopy(s['guard_social']);groups.sync_contacts(s)
        self.assertEqual(before,s['guard_social']);self.assertIn('Theo',s['npc_chats'])
        self.assertEqual(s['groups']['mixed']['members'],['Theo'])
        self.assertEqual(s['groups']['mixed']['history'][0]['text'],'Keep this')
        self.assertEqual(s['guard_social']['legacy']['npc:'+name]['history'][0]['text'],'Old guard line')
        self.assertIsNone(s['active_group']);self.assertNotIn(name,s['phone_numbers']['directory'])
        self.assertNotIn('group:npc:'+name,s['messaging']['threads'])
        messaging.tick(s)
        s['phone_numbers']['directory'][name]='12025559999'
        with self.assertRaises(ValueError):phone_numbers.add(s,'12025559999')
        restored=json.loads(json.dumps(s));groups.sync_contacts(restored)
        self.assertEqual(restored['guard_social'],s['guard_social'])

    def test_generation_failure_duplicate_and_stale_replies(self):
        s,name=self.state();gid=groups.open_local(s,name)
        before=copy.deepcopy(s['groups'][gid]['history'])
        with patch.object(core,'request',side_effect=RuntimeError('offline')):
            with self.assertRaisesRegex(RuntimeError,'offline'): gd.generate(s,name,'Hello')
        self.assertEqual(before,s['groups'][gid]['history'])
        result=gd.generate(s,name,'Hello')
        gd.commit(s,name,'Hello',result)
        with self.assertRaises(ValueError):gd.commit(s,name,'Hello',result)
        result=gd.generate(s,name,gd.TOPICS['Directions'])
        s['job_apps']['membership']=dict(faction='Syndicate',branch='Clubs',rank=6)
        with self.assertRaises(ValueError):gd.commit(s,name,'Hello',result)
        result=gd.generate(s,name,gd.TOPICS['Directions']);groups.close_active(s,'Done')
        groups.open_local(s,name)
        with self.assertRaises(ValueError):gd.commit(s,name,'Hello',result)

    def test_commands_visitors_memory_and_warnings(self):
        s,name=self.state('ivan');r=gd.row(s,name)
        self.assertIn('operational',gd.act(s,name,'status'))
        self.assertIn('recognised',gd.act(s,name,'boundary'))
        s['world']['cast']['emily'].update(location=s['world']['location'],journey=None)
        gd.act(s,name,'admit','emily');self.assertIn('emily',gd.post(s,r)['visitors'])
        gd.act(s,name,'revoke','emily');self.assertNotIn('emily',gd.post(s,r)['visitors'])
        gd.act(s,name,'refer');gd.act(s,name,'refer');self.assertEqual(len(gd.post(s,r)['requests']),1)
        gd.act(s,name,'report');self.assertEqual(len(gd.post(s,r)['reports']),1)
        s,name=self.state();r=gd.row(s,name)
        for _ in range(4):gd.act(s,name,'boundary')
        self.assertEqual(gd.post(s,r)['warnings']['rei'],3);self.assertFalse(s['combat']['active'])
        with self.assertRaises(ValueError):gd.act(s,name,'status')
        gd.act(s,name,'appointment');gd.act(s,name,'appointment')
        self.assertEqual(len(gd.post(s,r)['requests']),1)
        self.assertIn('No visitor',gd.act(s,name,'credentials'))

    def test_disabled_and_combat_posts_unavailable(self):
        s,name=self.state();groups.open_local(s,name)
        guards.data(s)['disabled'].append('syndicate')
        with self.assertRaises(ValueError):gd.generate(s,name,'Hello')
        s,name=self.state();guards.begin(s)
        with self.assertRaises(ValueError):groups.open_local(s,name)

    def test_custom_types_owner_and_rename(self):
        s,name=self.state();arrive(s,'crew_lot_west')
        s['job_apps']['gang']=dict(name='Test crew',role='Founder',members={})
        d=guards.data(s);d['properties']['crew_lot_west']=dict(owner='Test crew',use='Hideout')
        for i,category in enumerate(('awakened','unawakened','robotic')):
            kind='custom:test:'+category;d['types'][kind]=['Test '+category,category,'MMA','',0,30]
            d['roster'].append(dict(id=str(i),type=kind,venue='crew_lot_west'))
        for name,r in guards.npc_rows(s).items():
            self.assertTrue(gd.authority(s,'rei',r)['can_command']);self.assertNotEqual(gd.guide(s,r)[0],'Neutral, professional')
            gid=groups.open_local(s,name);gd.commit(s,name,gd.TOPICS['Directions'],gd.generate(s,name,gd.TOPICS['Directions']))
            key=s['groups'][gid]['guard_session'];d['types'][r['type']][0]='Renamed'
            newname=next(n for n,v in guards.npc_rows(s).items() if v['id']==r['id'])
            new=groups.open_local(s,newname);self.assertEqual(key,s['groups'][new]['guard_session'])
        s['job_apps']['gang']=dict(name='Other',role='Founder')
        self.assertFalse(gd.authority(s,'rei',r)['can_command'])

    def test_background_snapshot_reply_commits_to_live_state(self):
        s,name=self.state();gid=groups.open_local(s,name)
        text=gd.TOPICS['Directions']
        result=groups.generate(copy.deepcopy(s),gid,text)
        groups.commit(s,gid,text,result)
        self.assertIn('visitor area',s['groups'][gid]['history'][-1]['text'])

    def test_real_save_load_and_history_continuity(self):
        import tempfile
        from pathlib import Path
        s,name=self.state();gid=groups.open_local(s,name)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json';path.write_text(json.dumps(s),encoding='utf-8')
            loaded=core.load(path)
        text=gd.TOPICS['Directions'];gd.commit(loaded,name,text,gd.generate(loaded,name,text))
        old=copy.deepcopy(loaded['groups'][gid]['history'])
        new=groups.open_local(loaded,name)
        self.assertEqual(loaded['groups'][new]['history'][:len(old)],old)

    def test_suggestions_and_post_changes_invalidate_generation(self):
        import suggestions
        s,name=self.state();gid=groups.open_local(s,name)
        for kind in ('main','personal','actions'):
            with patch.object(core,'request',side_effect=AssertionError('Must be local')):
                lines=suggestions.generate(s,('group',gid),kind)
            self.assertEqual(len(lines),4)
        reply=gd.TOPICS['Directions'];result=gd.generate(s,name,reply)
        gd.act(s,name,'report','A visitor needs help by the entrance.')
        with self.assertRaises(ValueError):gd.commit(s,name,reply,result)
        self.assertIn('visitor needs help',gd.post(s,gd.row(s,name))['reports'][-1]['text'])

    def test_conflicting_orders_and_authorisation_expiry(self):
        s,name=self.state('ivan');r=gd.row(s,name)
        s['world']['cast']['emily'].update(location=s['world']['location'],journey=None)
        gd.post(s,r)['visitors']['emily']=dict(by='sylvanis',minute=s['world']['minute'])
        with self.assertRaises(ValueError):gd.act(s,name,'revoke','emily')
        with self.assertRaises(ValueError):gd.act(s,name,'admit','emily')
        s['world']['minute']+=1440
        self.assertNotIn('emily',gd.post(s,r)['visitors'])
        gd.act(s,name,'admit','emily')
        # Promotion/expulsion affects the issuer when checking a recorded grant.
        s['combat']['expelled']=['syndicate']
        self.assertFalse(gd.authority(s,'ivan',r)['can_command'])

    def test_empty_narration_preserves_ai_reply_for_fox(self):
        s,name=self.state('fox','interpol_hq');gid=groups.open_local(s,name)
        response={'message':{'content':json.dumps(dict(narration='',lines=[dict(speaker=name,text='Which files do you need?')]))}}
        with patch.object(core,'request',return_value=response) as request:
            result=gd.generate(s,name,'I need files.')
        gd.commit(s,name,'I need files.',result)
        self.assertEqual(request.call_count,1)
        self.assertEqual(s['groups'][gid]['history'][-1]['text'],'Which files do you need?')
        self.assertNotEqual(result['lines'][0]['text'],gd.greeting(s,gd.row(s,name)))

    def test_all_topic_replies_use_provider_and_retry_malformed_output(self):
        s,name=self.state();groups.open_local(s,name)
        for line in gd.TOPICS.values():
            before=self.provider.call_count
            gd.generate(s,name,line)
            self.assertEqual(self.provider.call_count,before+1)
        valid={'message':{'content':json.dumps(dict(narration='',lines=[dict(speaker=name,text='Which record are you looking for?')]))}}
        with patch.object(core,'request',side_effect=[{'message':{'content':'invalid'}},valid]) as request:
            result=gd.generate(s,name,'I need files.')
        self.assertEqual(request.call_count,2)
        self.assertEqual(result['lines'][0]['text'],'Which record are you looking for?')

    def test_generated_context_and_authority_validation(self):
        s,name=self.state('ivan');groups.open_local(s,name)
        response={'message':{'content':json.dumps(dict(narration='The guard looks up.',lines=[dict(speaker=name,text='You have no authority here.')]))}}
        with patch.object(core,'request',return_value=response) as request:
            with self.assertRaisesRegex(ValueError,'could not be validated'):gd.generate(s,name,'Report.')
        self.assertEqual(request.call_count,2)
        payload=request.call_args.args[1]
        self.assertTrue(json.loads(payload['messages'][1]['content'])['authority']['can_command'])

if __name__=='__main__':unittest.main()
