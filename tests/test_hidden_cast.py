from date_fixtures import next_morning
import json
import tempfile
import unittest
from pathlib import Path
import game_core as c
import town
from date_fixtures import finish_date, afternoon_state
import hidden_cast as h

class HiddenCastTests(unittest.TestCase):
    def test_sylvanis_headquarters_access_and_public_encounter(self):
        for player in c.playable_cast.ORIGINAL:
            s = c.fresh(player)
            self.assertEqual(h.contact(s, 'sylvanis'), player == 'ivan')
            self.assertEqual(h.visible_place(s, h.HQ), player == 'ivan')
            if player != 'ivan':
                with self.assertRaises(ValueError):
                    town.travel(s, h.HQ)
                with self.assertRaises(ValueError):
                    h.request_hq_invitation(s)
            else:
                self.assertEqual(town.character_stats(s, 'sylvanis')['status'], 'hostile coworkers')
                town.travel(s, h.HQ)
                town.finish_drive(s)
                town.summon(s, 'valentina')
                self.assertEqual(s['world']['cast']['valentina']['location'], h.HQ)
        s = afternoon_state('rei')
        s['autonomy']['people']['sylvanis']['next_decision']=10**12
        town.travel(s, 'arena')
        town.finish_drive(s)
        # A chance encounter can still occur; his ordinary afternoon is now private lab work.
        s['world']['cast']['sylvanis'].update(location='arena', journey=None, activity='Watching a sparring round')
        town.meet(s, 'sylvanis')
        h.add_contact(s, 'sylvanis')
        with self.assertRaises(ValueError): h.request_hq_invitation(s)
        s['hq_invitations']=['rei']
        s['world']['location']=h.HQ
        s['world']['cast']['rei']['location']=h.HQ
        with tempfile.TemporaryDirectory(dir=c.ROOT/'.test-tmp') as folder:
            path = Path(folder)/'guest.json'
            c.save(s,path);s=c.load(path)
        self.assertNotIn('hq_invitations',s)
        self.assertEqual(s['world']['location'],'syndicate_office')
        with self.assertRaises(ValueError):town.travel(s,h.HQ)
        for who in h.SYNDICATE_MEMBERS:self.assertTrue(h.hq_access(s,who))

    def test_vendetta_residents_can_be_befriended_then_dated(self):
        for player in c.playable_cast.ORIGINAL:
            for who, profile in h.VENDETTA_CAST.items():
                with self.subTest(player=player, contact=who):
                    s = c.fresh(player)
                    if player == 'ivan' and who == 'valentina':
                        self.assertTrue(h.contact(s, who))
                        self.assertEqual(s['active'], who)
                        self.assertIn('strictly platonic', c.build_messages(s, c.INCOMING_TEXT)[0]['content'])
                        bond = town.character_stats(s, who)
                        town.social_event(s, who, 'returned_flirt')
                        self.assertEqual((bond['status'], bond['trust'], bond['closeness'], bond['attraction']),
                                         ('close siblings', 98, 95, 0))
                        self.assertNotIn(who, s['relationships'])
                        continue
                    town.travel(s, profile['area'])
                    town.finish_drive(s)
                    town.meet(s, who)
                    h.add_contact(s, who)
                    for day in range(3):
                        if day:
                            next_morning(s)
                        town.conversation_progress(s, who)
                    stats = town.character_stats(s, who)
                    self.assertEqual(stats['status'], 'friends')
                    self.assertEqual(stats['attraction'], profile['attraction'])
                    if not town.romanceable(s,who):
                        for _ in range(3):town.social_event(s,who,'returned_flirt')
                        self.assertNotIn(who,s['relationships'])
                        with self.assertRaises(ValueError):town.relationship(s,who,'date')
                        continue
                    if who in town.MALE_ROUTES:
                        self.assertNotIn(who, s['relationships'])
                        for _ in range(3):
                            town.social_event(s, who, 'returned_flirt')
                        self.assertEqual(s['relationships'][who]['status'], 'mutual interest')
                    h.discover_home(s, who)
                    town.travel(s, s['world']['cast'][who]['location'])
                    town.finish_drive(s)
                    finish_date(s, who)
                    self.assertEqual(s['relationships'][who]['status'], 'dating')

    def test_discovery_contact_home_and_roundtrip(self):
        for who,p in h.CAST.items():
            if who == 'crow': continue  # Headquarters-only mystery has dedicated access tests.
            s=afternoon_state(); s['active']=who
            self.assertFalse(h.contact(s,who))
            with self.assertRaises(ValueError): c.build_messages(s,'hello')
            with self.assertRaises(ValueError): h.add_contact(s,who)
            with self.assertRaises(ValueError): town.travel(s,town.HOMES[who])
            town.travel(s,s['world']['cast'][who]['location']); town.finish_drive(s); town.meet(s,who)
            self.assertTrue(h.known(s,who)); self.assertTrue(h.contact(s,who))
            self.assertIn(p['personality'],c.build_messages(s,'Hello')[0]['content'])
            with self.assertRaises(ValueError): h.discover_home(s,who)
            h.add_contact(s,who)
            for day in range(3):
                town.conversation_progress(s,who)
                if day<2: next_morning(s)
            h.discover_home(s,who)
            self.assertTrue(h.visible_place(s,town.HOMES[who]))
            town.travel(s,town.HOMES[who]); town.finish_drive(s)
            self.assertEqual(s['world']['location'],town.HOMES[who])
            with tempfile.TemporaryDirectory() as folder:
                path=Path(folder)/'story.json'; c.save(s,path)
                self.assertEqual(c.load(path),s)

    def test_old_save_migration_and_no_initial_spoilers(self):
        s=c.fresh(); del s['discoveries']
        for who in h.CAST:
            s['routes'].pop(who); s['world']['cast'].pop(who)
            s['relationships'].pop(who,None); s['friendships'].pop(who,None)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json'; c.save(s,path); loaded=c.load(path)
        self.assertEqual(loaded['routes']['emily'],s['routes']['emily'])
        town.wait(loaded,200)
        context=town.context(loaded)
        for who,p in h.CAST.items():
            self.assertIn(who,loaded['routes'])
            self.assertNotIn('"'+who+'"',context)
            self.assertNotIn(p['home'],context)
            self.assertFalse(h.known(loaded,who))

    def test_platonic_routes_and_overlap_bonds(self):
        s=afternoon_state()
        for who in h.CAST:
            if who not in h.ROMANCE:
                with self.assertRaises(ValueError): town.relationship(s,who,'date')
                self.assertEqual(town.character_stats(s,who)['attraction'],0)
        town.travel(s,s['world']['cast']['lena']['location']); town.finish_drive(s); town.meet(s,'lena')
        h.add_contact(s, 'lena')
        s['relationships']['emily']['status']='official'
        finish_date(s, 'lena')
        import consequences
        consequences.disclose(s, 0, 'emily')
        self.assertEqual(s['relationships']['emily']['status'],'strained')
        self.assertTrue(any('lena' in k for k in s['bond_details']))
