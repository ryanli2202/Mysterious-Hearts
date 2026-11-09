import copy
import json
import unittest

import crime_sites as sites
import conversation_lore
import game_core as core
import hidden_cast
import phone_map
import social_world
import town


def go(s, key):
    if s['world']['location'] != key: town.travel(s, key)


class CitySitesTests(unittest.TestCase):
    def test_old_save_reads_do_not_mutate_and_names_are_not_searchable(self):
        s = core.fresh('rei'); before = copy.deepcopy(s)
        for key, spec in sites.SITES.items():
            self.assertTrue(sites.label(s,key).startswith('Unlabelled'))
            self.assertNotIn(key, phone_map.places(s,spec['name']))
            self.assertNotIn(key, phone_map.places(s,key))
        self.assertEqual(before,s)
        self.assertNotIn('site_07',phone_map.places(s,'Oculus'))

    def test_only_three_characters_start_with_oculus_affiliation(self):
        s=core.fresh('rei')
        for who in (*s['world']['cast'], 'Joseph Richter'):
            self.assertEqual(sites.affiliation_known(s,'site_07',who),who in sites.INSIDERS,who)
        self.assertIn('site_07',phone_map.places(core.fresh('ivan'),'Oculus'))
        self.assertIn('Syndicate', str(sites.context(s,'valentina','Oculus')))
        self.assertNotIn('Syndicate', str(sites.context(s,'garrett','Oculus')))
        for who in ('ivan','valentina','sylvanis','garrett','rei','emily','Dana Lin'):
            self.assertEqual('Syndicate-controlled' in str(conversation_lore.topic_reference(who,'Oculus')),who in sites.INSIDERS)

    def test_inspection_does_not_reveal_oculus_or_grant_entry(self):
        s=core.fresh('rei'); go(s,'site_07'); sites.inspect(s,'site_07')
        self.assertIn('site_07',phone_map.places(s,'Oculus'))
        self.assertFalse(sites.affiliation_known(s,'site_07'))
        go(s,'archive'); sites.research(s,'site_07'); go(s,'interpol_hq')
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError): sites.verify(s,'site_07')
        self.assertEqual(before,s)
        with self.assertRaises(ValueError): town.travel(s,hidden_cast.HQ)

    def test_each_affiliate_requires_evidence_and_survives_save(self):
        for key in sites.SITES:
            if key=='site_07': continue
            s=core.fresh('garrett')
            before=copy.deepcopy(s)
            with self.assertRaises(ValueError): sites.inspect(s,key)
            self.assertEqual(before,s)
            go(s,'interpol_hq')
            with self.assertRaises(ValueError): sites.verify(s,key)
            go(s,key); sites.inspect(s,key)
            self.assertFalse(sites.affiliation_known(s,key))
            go(s,'archive'); sites.research(s,key)
            self.assertFalse(sites.affiliation_known(s,key))
            go(s,'interpol_hq'); sites.verify(s,key)
            loaded=json.loads(json.dumps(s))
            self.assertTrue(sites.affiliation_known(loaded,key))
            self.assertFalse(sites.affiliation_known(loaded,key,'emily'))
            self.assertNotIn(sites.SITES[key]['faction'],str(sites.context(loaded,'emily',sites.SITES[key]['name'])))
            with self.assertRaises(ValueError): sites.verify(loaded,key)

    def test_general_can_enter_hq_but_cannot_smuggle_an_uninvited_guest(self):
        self.assertTrue(hidden_cast.hq_access(core.fresh('ivan'),'valentina'))
        s=core.fresh('ivan'); town.summon(s,'valentina')
        town.travel(s,hidden_cast.HQ)
        self.assertEqual(s['world']['cast']['valentina']['location'],hidden_cast.HQ)
        s=core.fresh('rei')
        with self.assertRaises(ValueError): town.travel(s,hidden_cast.HQ)
        s=core.fresh('ivan')
        s['world']['cast']['rei'].update(location=s['world']['location'],journey=None)
        s['world']['party']=['rei']
        location=s['world']['location']
        with self.assertRaises(ValueError): town.travel(s,hidden_cast.HQ)
        self.assertEqual(s['world']['location'],location)

    def test_dialogue_gets_speaker_knowledge_not_player_notebook(self):
        s=core.fresh('ivan')
        outsider=social_world.reference_for(s,'emily',['ivan'],'Oculus')
        insider=social_world.reference_for(s,'valentina',['ivan'],'Oculus')
        field='City site knowledge (private vantage point)'
        self.assertNotIn('Syndicate',str(outsider[field]))
        self.assertIn('Syndicate',str(insider[field]))


if __name__=='__main__': unittest.main()
