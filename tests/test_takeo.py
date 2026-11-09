import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import game_core as core
import hidden_cast as hidden
import phone_numbers
import takeo
import town
import world_loop
import crime_operations
import conversation_lore
import bubblegram_progression


class TakeoTests(unittest.TestCase):
    def state(self, rank=None, faction='Shinokami', strikes=0):
        s = core.fresh('rei')
        if rank is not None:
            s.setdefault('job_apps', {})['membership'] = dict(faction=faction, branch=faction, rank=rank, strikes=strikes)
        return s

    def test_contact_gate_and_revocation(self):
        for rank, faction, strikes, allowed in [(None,'Shinokami',0,False), (5,'Shinokami',0,False), (6,'Shinokami',0,True), (7,'Shinokami',0,True), (7,'Shinokami',2,False), (7,'Syndicate',0,False)]:
            with self.subTest(rank=rank, faction=faction, strikes=strikes):
                s=self.state(rank,faction,strikes)
                with self.assertRaises(ValueError): phone_numbers.add(s,phone_numbers.number(s,'takeo'))
                s['world']['location']=takeo.HQ
                hidden.mark_met(s,'takeo')
                self.assertEqual(hidden.contact(s,'takeo'),allowed)
                if allowed:
                    phone_numbers.add(s,phone_numbers.number(s,'takeo'))
                    s['job_apps']['membership']['strikes']=2
                    self.assertFalse(hidden.contact(s,'takeo'))
                    self.assertIsNone(phone_numbers.saved_number(s,'takeo'))
                else:
                    with self.assertRaises(ValueError): hidden.add_contact(s,'takeo')
                    with self.assertRaises(ValueError): phone_numbers.add(s,phone_numbers.number(s,'takeo'))

    def test_permanent_location_and_access(self):
        s=self.state(6)
        for minute in range(0,14*1440,60): self.assertEqual(world_loop.appointment('takeo',minute)[1],takeo.HQ)
        self.assertTrue(crime_operations.permitted(s,'rei','site_01'))
        self.assertFalse(crime_operations.permitted(self.state(5),'rei','site_01'))
        town.end_hangouts(s)
        town.travel(s,'site_01')
        crime_operations.enter(s,'site_01','reception')
        crime_operations.enter(s,'site_01','briefing')
        town.meet(s,'takeo')
        self.assertTrue(hidden.known(s,'takeo'))
        self.assertTrue(hidden.contact(s,'takeo'))
        self.assertFalse(town.romanceable(s,'takeo'))
        for fn in (town.summon,town.accept_hangout):
            with self.assertRaises(ValueError): fn(s,'takeo')
        with self.assertRaises(ValueError): world_loop.start_trip(s,'takeo','park')
        world_loop.advance(s,60)
        self.assertEqual(s['world']['cast']['takeo']['location'],takeo.HQ)

    def test_save_migration(self):
        s=self.state()
        for bucket in ('routes','friendships','discoveries'): s[bucket].pop('takeo',None)
        s['world']['cast'].pop('takeo')
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'save.json'; core.save(s,path); loaded=core.load(path)
        self.assertIn('takeo',loaded['routes'])
        self.assertEqual(loaded['world']['cast']['takeo']['location'],takeo.HQ)
        self.assertFalse(hidden.contact(loaded,'takeo'))

    def test_canon_and_art(self):
        self.assertEqual(bubblegram_progression.ESTABLISHED['takeo'][0],100)
        self.assertEqual(hidden.CAST['takeo']['height'],211)
        self.assertEqual(hidden.CAST['takeo']['mbti'],'Unknown')
        self.assertIn('Number 13',hidden.canon('takeo'))
        s=self.state(6); s['active']='takeo'
        s['world']['location']=takeo.HQ; hidden.mark_met(s,'takeo')
        self.assertIn(takeo.VOICE,core.build_messages(s,'Your report?')[0]['content'])
        self.assertIn(takeo.VOICE,conversation_lore.turn_focus(s,'takeo',['rei'],0,'report'))
        for prompt in (json.loads(core.build_messages(s,'Why did you leave military service?')[-1]['content'])['reference_for_reply'],
                       conversation_lore.turn_focus(s,'takeo',['rei'],0,'military service')):
            self.assertIn(takeo.HISTORY, prompt)
            self.assertIn(takeo.PERSONALITY, prompt)
            self.assertIn(takeo.ABILITY, prompt)
            self.assertIn(takeo.BOUNDARY, prompt)
        import vendetta_lore
        self.assertIn(takeo.ABILITY, vendetta_lore.speaker_context('takeo', ['rei'], s)['Own ability (private self-knowledge)'])
        self.assertNotIn(takeo.ABILITY, str(vendetta_lore.speaker_context('neo', ['rei'], s)))
        self.assertIn('takeo',conversation_lore.character_tables())
        import phone_apps, grove_photos, grove_reactions, meet_cute
        self.assertNotIn('takeo',meet_cute.HOOKS)
        with self.assertRaises(ValueError): phone_apps.queue_grove(s,'takeo')
        with Image.open(core.ROOT/'assets/portraits/takeo-selection.png') as image:
            self.assertEqual(image.mode,'RGBA')
            self.assertEqual(image.getchannel('A').getextrema(),(0,255))
        with Image.open(core.ROOT/'assets/profiles/takeo.png') as image:
            self.assertEqual(image.width,image.height)


if __name__ == '__main__': unittest.main()
