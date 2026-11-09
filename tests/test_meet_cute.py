import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from datetime import timedelta

import game_core as core
import hidden_cast
import meet_cute as mc
import phone_apps
import scheduled_events
import story_calendar
import town


class MeetCuteTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('rei')
        self.s['world']['minute']=3*1440+10*60
        self.publish()

    def publish(self):
        mc.publish(self.s,'A quiet meal and a sketchbook.',list(mc.interest_options(self.s)),
                   list(mc.HOOKS[self.s['player']]),['portrait'],'Open to either','Evenings',False)

    def matched(self,who='lena',turns=0):
        m=mc._match(self.s,who,'Hello. What are you drawing?',mc.ensure(self.s)['profile'])
        m['turns']=turns
        return m

    def advance(self,minutes=200):
        self.s['world']['minute']+=minutes
        mc.tick(self.s)

    def test_protagonist_interest_whitelist_and_atomic_validation(self):
        expected={'rei':('Drawing','Poetry','Cooking'), 'garrett':('Cooking','Jeet Kune Do','Sanda'),
                  'minsu':('Science','Video games','Anime','Taekwondo','Reviewing food'),
                  'ivan':('Singing','Piano','Music','Modelling')}
        for player,interests in expected.items():
            self.s=core.fresh(player); self.publish()
            before=copy.deepcopy(mc.ensure(self.s)['profile'])
            self.assertEqual(mc.interest_options(self.s),interests)
            with self.assertRaises(ValueError):
                mc.publish(self.s,'Bio',['Invented hobby'],list(mc.HOOKS[player]),['portrait'],'Open to either','Evenings')
            self.assertEqual(mc.ensure(self.s)['profile'],before)
            with self.assertRaises(ValueError):
                mc.preferences(self.s,17,40,'Everyone','Open to either','Preferred')

    def test_feed_is_bounded_repeatable_and_excludes_family_and_nonparticipants(self):
        feed=mc.feed(self.s)
        self.assertLessEqual(len(feed),5)
        self.assertEqual(feed,mc.feed(self.s))
        all_seen=[]
        while mc.feed(self.s):
            who=mc.feed(self.s)[0]['who']; all_seen.append(who); mc.skip(self.s,who)
        self.assertNotIn('rei',all_seen)
        self.assertNotIn('yuriko',all_seen)
        self.assertNotIn('sylvanis',all_seen)
        self.assertNotIn('rosa',all_seen)
        self.assertLessEqual(len(all_seen),5)
        self.s['world']['minute']+=1440
        self.assertTrue(mc.feed(self.s))

    def test_filters_must_have_vs_preferred_and_cast_availability(self):
        mc.preferences(self.s,24,26,'Women','Open to either','Preferred')
        self.assertTrue(all(p['age']>=24 and p['gender']=='Women' for p in mc.feed(self.s)))
        mc.preferences(self.s,18,40,'Everyone','Open to either','Must have','Poetry')
        self.assertEqual(mc.feed(self.s),[])
        mc.preferences(self.s,18,40,'Everyone','Open to either','Preferred','Poetry')
        self.assertTrue(mc.feed(self.s))
        self.s['world']['minute']=600
        self.assertFalse(mc.eligible(self.s,'valentina'))
        self.assertTrue(mc.eligible(self.s,'lena'))

    def test_hidden_profile_like_and_match_do_not_unlock_contact_or_location(self):
        mc.preferences(self.s,24,24,'Women','Open to either','Preferred')
        self.assertIn('lena',[p['who'] for p in mc.feed(self.s)])
        public=mc.public_profile(self.s,'lena')
        self.assertNotIn('home',public)
        self.assertNotIn('location',public)
        self.assertNotIn(hidden_cast.CAST['lena']['interior'],json.dumps(public))
        mc.like(self.s,'lena','Ask me about','Your film photography caught my interest. What do you enjoy photographing around old town?')
        with self.assertRaises(ValueError):mc.like(self.s,'lena','Photo','Another like')
        self.advance()
        m=mc.match(self.s,'lena')
        self.assertEqual(m['messages'][0]['author'],'you')
        self.assertFalse(hidden_cast.known(self.s,'lena'))
        self.assertFalse(hidden_cast.contact(self.s,'lena'))
        self.assertFalse(hidden_cast.visible_place(self.s,'lena_home'))
        self.assertFalse(hidden_cast.ensure(self.s)['lena']['met'])

    def test_incoming_likes_respect_pause_and_mutual_acceptance(self):
        mc.pause(self.s,True)
        self.advance(250)
        self.assertEqual(mc.ensure(self.s)['likes'],[])
        mc.pause(self.s,False); mc.tick(self.s)
        incoming=[x for x in mc.ensure(self.s)['likes'] if x['status']=='incoming']
        self.assertEqual(len(incoming),1)
        item=incoming[0]
        self.assertIn(item['target'],('Photo',*mc.PROMPTS))
        self.assertNotIn(item['who'],mc.ensure(self.s)['matches'])
        mc.incoming_action(self.s,item['id'],True)
        self.assertIn(item['who'],mc.ensure(self.s)['matches'])
        with self.assertRaises(ValueError):mc.incoming_action(self.s,item['id'],True)

    def test_pause_keeps_existing_chat_and_block_invalidates_pending(self):
        m=self.matched()
        mc.pause(self.s,True)
        mc.send(self.s,'lena','What do you like taking photos of?')
        ident=m['pending']['id']
        mc.unmatch(self.s,'lena',True)
        self.assertFalse(mc.commit_reply(self.s,'lena',ident,'Late reply'))
        with self.assertRaises(ValueError):mc.send(self.s,'lena','Hello again')
        mc.pause(self.s,False)
        self.assertNotIn('lena',[p['who'] for p in mc.feed(self.s)])

    def test_numbers_require_agreement_and_do_not_mark_a_physical_meeting(self):
        m=self.matched()
        with self.assertRaises(ValueError):hidden_cast.introduce_online(self.s,'lena')
        mc.request_numbers(self.s,'lena'); self.advance()
        self.assertEqual(m['proposal']['status'],'declined')
        self.assertFalse(hidden_cast.contact(self.s,'lena'))
        m['turns']=3
        mc.request_numbers(self.s,'lena'); self.advance()
        self.assertEqual(m['proposal']['status'],'accepted')
        self.assertTrue(hidden_cast.contact(self.s,'lena'))
        self.assertTrue(hidden_cast.known(self.s,'lena'))
        self.assertFalse(hidden_cast.ensure(self.s)['lena']['met'])
        self.assertFalse(hidden_cast.visible_place(self.s,'lena_home'))

    def test_date_needs_consent_and_works_before_number_exchange(self):
        m=self.matched(turns=3)
        day=(story_calendar.story_date(mc.now(self.s))+timedelta(days=1)).isoformat()
        mc.propose_date(self.s,'lena','cafe',day,'17:00')
        self.assertEqual(self.s.get('scheduled_events',[]),[])
        with self.assertRaises(ValueError):scheduled_events.create(self.s,'Bypass',day,'17:00','cafe',['lena'],source='meet_cute')
        self.advance()
        self.assertEqual(m['proposal']['status'],'accepted')
        event=self.s['scheduled_events'][-1]
        self.assertEqual(event['source'],'meet_cute')
        self.assertFalse(hidden_cast.contact(self.s,'lena'))
        with self.assertRaises(ValueError):scheduled_events.create(self.s,'Wrong place',day,'20:00','lena_home',['lena'],source='meet_cute')
        self.s['world']['minute']=event['start']
        for who in ('rei','lena'):
            self.s['world']['cast'][who].update(location='cafe',journey=None)
        self.s['world']['location']='cafe'
        with patch('groups.form',return_value='test-date'):
            scheduled_events.join(self.s,event)
        self.assertTrue(hidden_cast.ensure(self.s)['lena']['met'])
        self.assertTrue(m['first_meeting'])
        self.assertFalse(hidden_cast.visible_place(self.s,'lena_home'))

    def test_unmatch_cancels_upcoming_date(self):
        m=self.matched(turns=3)
        day=(story_calendar.story_date(mc.now(self.s))+timedelta(days=1)).isoformat()
        mc.propose_date(self.s,'lena','cafe',day,'17:00'); self.advance()
        mc.request_numbers(self.s,'lena'); self.advance()
        mc.unmatch(self.s,'lena')
        self.assertTrue(self.s['scheduled_events'][-1]['cancelled'])

    def test_generation_privacy_context_and_failed_response(self):
        m=self.matched(); mc.send(self.s,'lena','Tell me about film photography.')
        ident=m['pending']['id']
        mc.request_numbers(self.s,'lena')
        with patch.object(core,'request',return_value={'message':{'content':json.dumps({'text':'I like the surprises on a film roll. What do you draw?'})}}) as request:
            reply=mc.generate(self.s,'lena',ident)
        payload=json.loads(request.call_args.args[1]['messages'][1]['content'])
        self.assertNotIn('occupation',payload['player'])
        self.assertNotIn(hidden_cast.CAST['lena']['interior'],json.dumps(payload))
        self.assertNotIn('world',payload)
        self.assertEqual(payload['history'][-1]['text'],'Tell me about film photography.')
        self.assertTrue(mc.commit_reply(self.s,'lena',ident,reply))
        self.assertFalse(mc.commit_reply(self.s,'lena',ident,reply))
        self.assertEqual(mc.context(self.s,['emily']),{})
        self.assertIn('lena',phone_apps.conversation_context(self.s,['lena'])['meet_cute'])

    def test_profile_snapshot_is_not_rewritten_by_edits(self):
        m=self.matched()
        before=copy.deepcopy(m['profile'])
        mc.publish(self.s,'A revised bio',['Cooking'],['A','B','C'],['portrait'],'Casual dating','Mornings')
        self.assertEqual(m['profile'],before)

    def test_grove_picker_ownership_publish_and_restore(self):
        import grove_gallery
        own = grove_gallery.photos(self.s, 'rei')[0]
        other = grove_gallery.photos(self.s, 'garrett')[0]
        ident = 'grove:'+str(own['id'])
        self.assertIn(ident, mc.photos(self.s))
        self.assertNotIn('grove:'+str(other['id']), mc.photos(self.s))
        mc.publish(self.s, 'A sketchbook.', ['Drawing'], ['A','B','C'],
                   [ident, 'portrait'], 'Open to either', 'Evenings')
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as tmp:
            path = Path(tmp)/'save.json'
            core.save(self.s, path)
            loaded = core.load(path)
        self.assertEqual(mc.ensure(loaded)['profile']['photos'], [ident, 'portrait'])
        self.assertEqual(mc.photos(loaded)[ident], mc.photos(self.s)[ident])

    def test_grove_missing_and_outside_paths_are_not_selectable(self):
        posts = [dict(id=1, image='../outside.png', text='Outside', parent=None),
                 dict(id=2, image='assets/grove/missing.png', text='Missing', parent=None),
                 dict(id=3, image='meet_cute.py', text='Not a photo', parent=None)]
        with patch('grove_gallery.photos', return_value=posts):
            self.assertEqual(mc.grove_photos(self.s, 'rei'), {})
            with self.assertRaises(ValueError):
                mc.publish(self.s, 'Bio', ['Drawing'], ['A','B','C'],
                           ['grove:1'], 'Open to either', 'Evenings')

    def test_character_profile_uses_own_grove_and_portrait_fallback(self):
        available = mc.grove_photos(self.s, 'emily', character_only=True)
        self.assertTrue(available)
        profile = mc.public_profile(self.s, 'emily')
        self.assertIn(profile['photo'], [p['path'] for p in available.values()])
        self.assertEqual(profile, mc.public_profile(self.s, 'emily'))
        with patch('grove_gallery.photos', return_value=[]):
            self.assertTrue(mc.public_profile(self.s, 'emily')['photo'].endswith('emily-selection.png'))

    def test_every_character_has_reviewed_archive_photo(self):
        for who in mc.HOOKS:
            with self.subTest(who=who):
                self.assertGreaterEqual(len(mc.grove_photos(self.s, who, character_only=True)), 2)

    def test_profile_carousel_contains_only_distinct_character_photos(self):
        for who in mc.HOOKS:
            if not mc.eligible(self.s, who):
                continue
            with self.subTest(who=who):
                profile = mc.public_profile(self.s, who)
                paths = profile['photos']
                self.assertGreaterEqual(len(paths), 2)
                self.assertEqual(len(paths), len(set(paths)))
                self.assertEqual(profile['photo'], paths[0])
                self.assertEqual(set(paths), {p['path'] for p in mc.grove_photos(self.s, who, character_only=True).values()})
        with patch('grove_gallery.photos', return_value=[]):
            profile = mc.public_profile(self.s, 'emily')
            self.assertEqual(profile['photos'], [profile['photo']])

    def test_character_photos_require_subject_evidence(self):
        import grove_gallery
        posts = grove_gallery.photos(self.s, 'garrett')
        food = next(p for p in posts if p['archive_key'] == 'garrett:02-noodle-closeup')
        self.assertFalse(grove_gallery.shows_character(food, 'garrett'))
        with patch('grove_gallery.photos', return_value=[food]):
            self.assertTrue(mc.public_profile(self.s, 'emily')['photo'].endswith('emily-selection.png'))
        for context, expected in [({}, False), ({'mode':'Photo of hobby'}, False),
                                  ({'mode':'Selfie'}, True),
                                  ({'mode':'Selfie', 'subjects':[{'id':'rei'}]}, False),
                                  ({'mode':'Group photo', 'subjects':[{'id':'garrett'}]}, True)]:
            post = dict(author='garrett', photo_context=context)
            self.assertEqual(grove_gallery.shows_character(post, 'garrett'), expected)
            self.assertFalse(grove_gallery.shows_character(dict(author='rei', photo_context={'mode':'Selfie'}), 'garrett'))

    def test_save_load_pending_match_and_online_discovery(self):
        m=self.matched(turns=3)
        mc.request_numbers(self.s,'lena'); self.advance()
        mc.send(self.s,'lena','What is your next photo project?')
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as tmp:
            path=Path(tmp)/'save.json'
            core.save(self.s,path); loaded=core.load(path)
        self.assertEqual(loaded['meet_cute'],self.s['meet_cute'])
        self.assertTrue(hidden_cast.contact(loaded,'lena'))
        self.assertFalse(hidden_cast.ensure(loaded)['lena']['met'])

    def test_exclusivity_cannot_skip_normal_relationship_requirements(self):
        m=self.matched(turns=5)
        mc.request_exclusive(self.s,'lena'); self.advance()
        self.assertEqual(m['proposal']['status'],'declined')
        self.assertIsNone(mc.ensure(self.s)['exclusive_with'])

    def test_exclusivity_uses_established_relationship_and_pauses_discovery(self):
        m=self.matched(turns=5)
        mc.request_numbers(self.s,'lena'); self.advance()
        self.s['relationships']['lena'].update(status='dating',trust=100,closeness=100,attraction=100)
        mc.request_exclusive(self.s,'lena'); self.advance()
        self.assertEqual(m['proposal']['status'],'accepted')
        self.assertEqual(self.s['relationships']['lena']['status'],'official')
        self.assertTrue(mc.ensure(self.s)['paused'])
        self.assertEqual(mc.feed(self.s),[])

    def test_full_world_clock_delivers_likes_without_ai_and_does_not_backfill(self):
        self.s['world']['minute']=3*1440+10*60
        mc.ensure(self.s)['next_incoming']=mc.now(self.s)+1
        town.loop.advance(self.s,2)
        before=len(mc.ensure(self.s)['likes'])
        self.assertEqual(before,1)
        mc.tick(self.s);mc.tick(self.s)
        self.assertEqual(len(mc.ensure(self.s)['likes']),before)

    def test_old_unpublished_save_has_no_app_activity(self):
        s=core.fresh('rei')
        s.pop('meet_cute',None)
        mc.tick(s)
        self.assertNotIn('meet_cute',s)
        self.assertEqual(mc.feed(s),[])


if __name__=='__main__':unittest.main()
