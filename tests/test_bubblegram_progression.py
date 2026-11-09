import copy
import json
import unittest
from unittest.mock import patch
import game_core as core
import job_apps as j
import bubblegram_progression as p
import town
import four_aces
from test_job_apps import place,advance


class CriminalProgressionTests(unittest.TestCase):
    def test_origins_one_time_migration_and_legacy_progress(self):
        for player in ('rei','minsu','garrett','ivan'):
            s=core.fresh(player); d=j.ensure(s)
            if player in ('garrett','ivan'):
                self.assertGreaterEqual(d['reputation'],85)
                self.assertEqual(d['gang']['role'],'Leader')
                d['reputation']=60; j.ensure(s); self.assertEqual(d['reputation'],60)
            else: self.assertEqual(p.stage(d),'Unknown')
        s=core.fresh('garrett'); s['job_apps']=dict(reputation=92,gang=dict(name='Saved crew',standing=12,role='Founder'),history=[],membership=None)
        d=j.ensure(s); self.assertEqual(d['gang']['name'],'Saved crew'); self.assertEqual(d['reputation'],95)
        self.assertEqual(d['leadership']['name'],'Red Dragons')
        saved=copy.deepcopy(d); j.ensure(s); self.assertEqual(saved,d)

    def test_invitation_is_gated_saved_and_not_a_membership(self):
        s=core.fresh('minsu'); d=j.ensure(s)
        d.update(reputation=39,completed=8,gang=dict(name='crew',standing=3,role='Founder'))
        with self.assertRaises(ValueError): j.accept(s,'syndicate')
        d['reputation']=40; d['heat']=30; j.ensure(s); self.assertFalse(d['invitations'])
        d['heat']=0; j.ensure(s); self.assertEqual(len(d['invitations']),2)
        self.assertIsNone(d['membership']); self.assertEqual(len(d['history']),2)
        restored=json.loads(json.dumps(s)); j.ensure(restored)
        self.assertEqual(restored['job_apps']['invitations'],d['invitations'])
        self.assertEqual(len(restored['job_apps']['history']),2)
        with self.assertRaises(ValueError): j.sponsor(s,'Clubs')

    def test_gangs_join_advance_leave_and_reserved_names(self):
        for key,spec in p.GANGS.items():
            s=core.fresh('minsu'); d=j.ensure(s)
            with self.assertRaises(ValueError): p.join(s,key)
            d.update(reputation=70,completed=20); p.join(s,key)
            self.assertEqual(d['gang']['id'],key)
            with self.assertRaises(ValueError): p.review_gang(s)
            d['gang']['standing']=16
            for _ in range(3): p.review_gang(s)
            self.assertEqual(p.gang_title(d['gang']),'Captain')
            p.leave(s); self.assertIsNone(d['gang']); self.assertEqual(len(d['gang_archive']),1)
            if key=='hamayashi': self.assertTrue(d['hamayashi_affiliated'])
            with self.assertRaises(ValueError): j.gang(s,spec['name'])
        s=core.fresh('ivan')
        with self.assertRaises(ValueError): p.leave(s)

    def test_reputation_caps_and_high_tier_work(self):
        s=core.fresh('minsu'); d=j.ensure(s); d['reputation']=20; place(s,'downtown')
        with patch.object(j.careers,'spend_time',advance):
            j.accept(s,'parcel'); j.resolve(s,0)
        self.assertEqual(d['reputation'],20)
        self.assertEqual(d['completed'],1)
        self.assertGreater(s['world']['money'],0)

    def test_directory_keeps_ace_identities_secret(self):
        s=core.fresh('minsu'); text=' '.join(p.directory(s))
        for who in four_aces.IDS: self.assertNotIn(four_aces.CAST[who]['name'],text)
        for alias in ('Ace of Clubs','Coloured Joker','The Crow','Flaming Prince'): self.assertIn(alias,text)
        j.ensure(s)['membership']=dict(faction='Syndicate',branch='Clubs',rank=5)
        text=' '.join(p.directory(s))
        for who in four_aces.IDS: self.assertIn(four_aces.CAST[who]['name'],text)

    def test_hamayashi_discovery_private_once_and_past_affiliation(self):
        s=core.fresh('minsu'); d=j.ensure(s); d.update(reputation=50,completed=10)
        p.join(s,'hamayashi'); p.leave(s)
        self.assertFalse(d['hamayashi_discovery']['return_known'])
        self.assertIn('unaware',p.context(s,'rei')['Hamayashi boundary'])
        place(s,'studio'); s['world']['cast']['rei'].update(location='market',journey=None)
        with self.assertRaises(ValueError): p.reveal_hamayashi(s)
        s['world']['cast']['rei'].update(location='studio')
        stats=town.character_stats(s,'rei'); stats.update(trust=85,closeness=75)
        p.reveal_hamayashi(s)
        self.assertEqual((stats['trust'],stats['closeness']),(45,45))
        self.assertEqual(s['emotions']['rei'],'enraged')
        self.assertTrue(d['hamayashi_discovery']['affiliation_known'])
        self.assertEqual(p.context(s,'emily'),{})
        with self.assertRaises(ValueError): p.reveal_hamayashi(s)
        self.assertEqual(stats['trust'],45)
        restored=json.loads(json.dumps(s)); self.assertIn('seriously damaged',p.context(restored,'rei')['Hamayashi discovery'])

    def test_return_discovery_without_affiliation_and_rei_player(self):
        s=core.fresh('minsu'); place(s,'studio'); s['world']['cast']['rei'].update(location='studio',journey=None)
        stats=town.character_stats(s,'rei'); before=copy.deepcopy(stats)
        p.reveal_hamayashi(s); self.assertEqual(stats,before)
        d=j.ensure(s); d.update(reputation=50,completed=10); p.join(s,'hamayashi')
        p.reveal_hamayashi(s); self.assertTrue(d['hamayashi_discovery']['affiliation_known'])
        rei=core.fresh('rei'); self.assertFalse(j.ensure(rei)['hamayashi_discovery']['return_known'])
        p.reveal_hamayashi(rei); self.assertEqual(rei['emotions']['rei'],'enraged')


if __name__=='__main__': unittest.main()
