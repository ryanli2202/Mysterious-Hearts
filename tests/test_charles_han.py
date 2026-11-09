import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as core
import town, world_loop, hidden_cast, character_types, conversation_lore
import charles_han as charles
import criminal_dynamics, laboratory_missions, phone_numbers


class CharlesTests(unittest.TestCase):
    def test_major_lab_resident_and_hidden_from_garrett(self):
        for player in ('rei','garrett','ivan'):
            s=core.fresh(player)
            self.assertTrue(character_types.is_major('charles'))
            self.assertFalse(character_types.is_town('charles'))
            self.assertIn('charles',s['routes']);self.assertIn('charles',s['friendships'])
            self.assertFalse(hidden_cast.known(s,'charles'))
            self.assertFalse(hidden_cast.contact(s,'charles'))
            self.assertFalse(town.romanceable(s,'charles'))
            self.assertEqual(s['world']['cast']['charles']['location'],charles.LAB)
            with self.assertRaises(ValueError):phone_numbers.number(s,'charles')
        s=core.fresh('ivan');town.travel(s,charles.LAB);town.meet(s,'charles')
        self.assertFalse(hidden_cast.contact(s,'charles'))
        self.assertTrue(hidden_cast.known(s,'charles'))
        with self.assertRaises(ValueError):hidden_cast.add_contact(s,'charles')
        self.assertTrue(laboratory_missions.private(s))

    def test_every_relocation_path_and_roundtrip(self):
        s=core.fresh('ivan');town.travel(s,charles.LAB);town.meet(s,'charles')
        for destination in ('park','syndicate_hq','square'):
            with self.assertRaises(ValueError):world_loop.start_trip(s,'charles',destination)
            with self.assertRaises(ValueError):world_loop.start_trip(s,'ivan',destination,('charles',))
        with self.assertRaises(ValueError):hidden_cast.discover_home(s,'charles')
        with self.assertRaises(ValueError):town.accept_hangout(s,'charles')
        for minute in range(0,7*1440,60):self.assertEqual(world_loop.appointment('charles',minute)[1],charles.LAB)
        s['world']['cast']['charles'].update(location='park',journey=dict(destination='square'))
        world_loop.ensure(s);self.assertEqual(s['world']['cast']['charles']['location'],charles.LAB)
        for bucket in ('routes','friendships','discoveries'):s[bucket].pop('charles',None)
        s['world']['cast'].pop('charles')
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            p=Path(folder)/'old.json';core.save(s,p);s=core.load(p)
        self.assertIn('charles',s['routes']);self.assertEqual(s['world']['cast']['charles']['location'],charles.LAB)
        self.assertFalse(hidden_cast.known(s,'charles'))

    def test_secrets_only_in_own_character_reference(self):
        s=core.fresh('rei');s['active']='garrett'
        prompt=str(core.build_messages(s,'Where is Charles?'))
        for secret in ('deliberately disappeared','infiltrated the Syndicate','white flame tiger'):
            self.assertNotIn(secret,prompt)
        for who in ('ivan','sylvanis','martos','takeo'):
            reference=str(conversation_lore.speaker_reference(who,['ivan'],3,'Charles',s))
            self.assertNotIn('infiltrated the Syndicate',reference)
        own=conversation_lore.speaker_reference('charles',['ivan'],0,'work',s)
        self.assertIn('infiltrated the Syndicate',own['Knowledge from experience (private vantage point)'])
        self.assertIn('never volunteered',own['How much to share'])
        self.assertIn('191 cm',conversation_lore.character_tables()['charles']['Appearance'])
        self.assertIn('Likes',conversation_lore.character_tables()['charles'])
        import contact_profiles,phone_apps
        profile=str(contact_profiles.public(s,'charles','rei'))
        self.assertNotIn('infiltrat',profile);self.assertNotIn('avenge',profile)
        with self.assertRaises(ValueError):phone_apps.queue_grove(s,'charles')
        from PIL import Image
        for path in ('assets/portraits/charles-selection.png','assets/profiles/charles.png'):
            with Image.open(core.ROOT/path) as im:self.assertEqual(im.size,(1920,1080))

        with Image.open(core.ROOT/'assets/portraits/charles-selection-v2.png') as im:
            self.assertEqual(im.mode,'RGBA')
            self.assertEqual(im.getchannel('A').getextrema()[0],0)
            self.assertGreater(im.height,im.width)
