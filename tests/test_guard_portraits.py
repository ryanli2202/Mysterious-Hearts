import json
from pathlib import Path
import unittest
from PIL import Image
import game_core as core
import organisation_guards as guards
import guard_portraits as art
import rei_story
import campaign_dialogue
import combat
from test_major_campaigns import arrive, investigate, clear, win

class GuardPortraitTests(unittest.TestCase):
    def test_syndicate_posts_conversations_and_combat_use_current_assets(self):
        import guard_dialogue
        for venue, (faction, _) in guards.DEPLOYMENTS.items():
            if faction != 'syndicate':
                continue
            for kind in ('clubs', 'spades', 'affiliate'):
                with self.subTest(venue=venue, kind=kind):
                    s=core.fresh('ivan');arrive(s,venue)
                    name,row=next((n,r) for n,r in guards.npc_rows(s).items() if r['type']==kind)
                    guard_dialogue.open_session(s,name)
                    restored=json.loads(json.dumps(s))
                    self.assertEqual(art.resolve(restored,name,venue),art.path(kind))
                    slot=next(r for r in guards.slots(s,venue) if r['type']==kind)
                    guards.start(s,slot['id'],guards.profile(s,kind),'art-test',slot)
                    self.assertEqual(art.resolve(s,combat.active(s)['opponent'],venue),art.path(kind))
                    combat.active(s)['opponent_profile'].pop('portrait')
                    self.assertEqual(art.resolve(s,combat.active(s)['opponent'],venue),art.path(kind))

    def test_syndicate_scripted_fights_without_deployment_slots(self):
        for kind in ('clubs','spades','affiliate'):
            s=core.fresh('garrett');arrive(s,'market')
            guards.start(s,'scripted:'+kind,guards.profile(s,kind),'art-scripted')
            restored=json.loads(json.dumps(s))
            self.assertEqual(art.resolve(restored,'scripted:'+kind,'market'),art.path(kind))

    def test_every_type_has_a_transparent_asset(self):
        s=core.fresh('rei')
        for kind in guards.TYPES:
            self.assertEqual(guards.profile(s,kind)['portrait'],kind)
        for ident in art.IDS:
            with self.subTest(ident=ident),Image.open(art.path(ident)) as image:
                self.assertEqual(image.mode,'RGBA')
                alpha=image.getchannel('A');hist=alpha.histogram();total=image.width*image.height
                self.assertGreater(sum(hist[:8])/total,.10)
                self.assertGreater(sum(hist[220:])/total,.15)
                self.assertGreater(image.height,image.width)
        manifest=json.loads((art.ROOT/'assets/portraits/guards/manifest.json').read_text(encoding='utf-8'))
        self.assertEqual({r['id'] for r in manifest['portraits']},set(art.IDS))

    def test_named_posts_and_old_saved_encounters(self):
        s=core.fresh('rei');arrive(s,'site_01')
        name=next(iter(guards.npc_rows(s)))
        self.assertEqual(art.resolve(s,name,'site_01'),art.path('yokai'))
        guards.begin(s,scope='test')
        f=combat.active(s);f['opponent_profile'].pop('portrait')
        s=json.loads(json.dumps(s))
        self.assertEqual(art.resolve(s,f['opponent'],'site_01'),art.path('yokai'))

    def test_custom_name_does_not_change_archetype(self):
        s=core.fresh('rei');import job_apps
        job_apps.ensure(s)['gang']=dict(name='Test crew',role='Founder',rank=0,standing=0,members={})
        arrive(s,'crew_lot_west');s['world']['money']=100000;guards.buy(s,'crew_lot_west','Hideout')
        for category in ('awakened','unawakened','robotic'):
            guards.recruit(s,'Watch '+category,category,'crew_lot_west')
            row=guards.data(s)['roster'][-1]
            self.assertEqual(art.type_id(s,row['type']),'custom_'+category)
            guards.rename_type(s,row['type'],'Renamed '+category)
            self.assertEqual(guards.profile(s,row['type'])['portrait'],'custom_'+category)

    def test_richter_form_only_at_boss_scene_fight_and_aftermath(self):
        s=core.fresh('rei');arrive(s,'blackstone_hq')
        self.assertIsNone(art.resolve(s,'Joseph Richter','blackstone_hq'))
        self.assertIsNone(art.resolve(s,'Joseph Richter',None))
        investigate(s);clear(s,guards.BLACKSTONE,'rei:blackstone')
        campaign_dialogue.begin(s,'rei_story.confront')
        self.assertEqual(art.resolve(s,'Joseph Richter','blackstone_command'),art.path('richter_cybernetic'))
        while s.get('campaign_dialogue'):campaign_dialogue.next_line(s)
        self.assertEqual(combat.active(s)['opponent_profile']['portrait'],'richter_cybernetic')
        win(s);campaign_dialogue.activate_epilogue(s)
        self.assertEqual(art.resolve(s,'Joseph Richter','blackstone_command'),art.path('richter_cybernetic'))
        self.assertIsNone(art.resolve(s,'Joseph Richter','blackstone_hq'))

if __name__=='__main__':unittest.main()
