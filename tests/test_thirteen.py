import copy
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import game_core as core
import job_apps as jobs
import hidden_cast as hidden
import thirteen
import keisuke
import phone_numbers
import town
import world_loop
import crime_operations as ops
import conversation_lore as lore
from test_keisuke import join


class ThirteenTests(unittest.TestCase):
    def test_real_review_unlocks_second_contact_once(self):
        s=core.fresh('rei');join(s);d=jobs.ensure(s)
        self.assertTrue(phone_numbers.saved_number(s,keisuke.NAME))
        self.assertFalse(hidden.contact(s,'thirteen'))
        d['membership'].update(rank=3,assignments=18);d['reputation']=80
        jobs.review(s)
        self.assertEqual(d['membership']['rank'],4)
        self.assertTrue(hidden.contact(s,'thirteen'))
        self.assertTrue(hidden.known(s,'thirteen'))
        self.assertFalse(hidden.ensure(s)['thirteen']['met'])
        self.assertTrue(phone_numbers.saved_number(s,'thirteen'))
        self.assertFalse(hidden.contact(s,'takeo'))
        old=copy.deepcopy(s['routes']['thirteen']['history'])
        for _ in range(3):jobs.ensure(s);hidden.ensure(s);phone_numbers.ensure(s)
        self.assertEqual(s['routes']['thirteen']['history'],old)
        self.assertEqual(len(old),1)

    def test_gate_manual_number_meeting_suspension_and_rehabilitation(self):
        s=core.fresh('rei');join(s);d=jobs.ensure(s)
        s['world']['location']=thirteen.HQ
        hidden.mark_met(s,'thirteen')
        for rank,faction,strikes in ((3,'Shinokami',0),(7,'Syndicate',0),(4,'Shinokami',2)):
            d['membership'].update(rank=rank,faction=faction,branch=faction,strikes=strikes)
            self.assertFalse(hidden.contact(s,'thirteen'))
            with self.assertRaises(ValueError):phone_numbers.add(s,phone_numbers.NUMBERS['thirteen'])
            with self.assertRaises(ValueError):hidden.add_contact(s,'thirteen')
        d['membership'].update(rank=4,faction='Shinokami',branch='Shinokami',strikes=0)
        self.assertTrue(phone_numbers.saved_number(s,'thirteen'))
        d['membership']['strikes']=2
        self.assertIsNone(phone_numbers.saved_number(s,'thirteen'))
        self.assertFalse(hidden.contact(s,'thirteen'))
        d.update(reputation=80,heat=0);jobs.review(s)
        self.assertTrue(phone_numbers.saved_number(s,'thirteen'))

    def test_command_location_and_no_guest_clearance(self):
        s=core.fresh('rei');join(s);jobs.ensure(s)['membership'].update(rank=4)
        town.end_hangouts(s);town.travel(s,'site_02');ops.enter(s,'site_02','reception')
        self.assertFalse(ops.can_enter(s,'neo',thirteen.HQ))
        ops.enter(s,'site_02','briefing');town.meet(s,'thirteen')
        self.assertTrue(hidden.ensure(s)['thirteen']['met'])
        self.assertFalse(town.romanceable(s,'thirteen'))
        for minute in range(0,7*1440,60):self.assertEqual(world_loop.appointment('thirteen',minute)[1],thirteen.HQ)
        with self.assertRaises(ValueError):world_loop.start_trip(s,'thirteen','park')
        with self.assertRaises(ValueError):town.summon(s,'thirteen')
        self.assertFalse(ops.permitted(s,'rei','site_01'))
        self.assertTrue(ops.authority('thirteen','site_01'))
        self.assertTrue(ops.authority('thirteen','site_03'))
        self.assertFalse(ops.authority('thirteen','site_04'))

    def test_old_save_migration_preserves_rank(self):
        for rank in (0,4):
            s=core.fresh('rei');join(s);jobs.ensure(s)['membership']['rank']=rank
            for bucket in ('routes','friendships','discoveries'):s[bucket].pop('thirteen',None)
            s['world']['cast'].pop('thirteen')
            with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
                path=Path(folder)/'save.json';core.save(s,path);loaded=core.load(path)
            self.assertEqual(loaded['job_apps']['membership']['rank'],rank)
            self.assertEqual(hidden.contact(loaded,'thirteen'),rank==4)
            self.assertEqual(loaded['world']['cast']['thirteen']['location'],thirteen.HQ)

    def test_canon_privacy_voice_and_art(self):
        s=core.fresh('rei');join(s);jobs.ensure(s)['membership']['rank']=4
        hidden.ensure(s);s['active']='thirteen'
        for channel in ('text','in_person'):
            s['routes']['thirteen']['channel']=channel
            messages=core.build_messages(s,'What do you need?')
            self.assertIn(thirteen.VOICE,messages[0]['content'])
            self.assertIn(thirteen.BOUNDARY,lore.turn_focus(s,'thirteen',['rei'],0,'report'))
        self.assertEqual(thirteen.CAST['height'],194)
        self.assertIn('weakest child',thirteen.HISTORY)
        self.assertIn('supersedes',thirteen.HISTORY)
        self.assertNotIn('Neo',thirteen.PROFILE)
        import contact_profiles,phone_apps
        self.assertNotIn('Neo',str(contact_profiles.public(s,'thirteen','rei')))
        with self.assertRaises(ValueError):phone_apps.queue_grove(s,'thirteen')
        with Image.open(core.ROOT/'assets/portraits/thirteen-selection.png') as image:
            self.assertEqual(image.mode,'RGBA');self.assertEqual(image.getchannel('A').getextrema(),(0,255))
        with Image.open(core.ROOT/'assets/profiles/thirteen.png') as image:
            self.assertEqual(image.width,image.height);self.assertGreater(image.width,512)


if __name__=='__main__':unittest.main()
