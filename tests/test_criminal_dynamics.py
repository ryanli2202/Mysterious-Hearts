import copy
import json
import unittest
import criminal_dynamics as dynamics
import crime_diplomacy as diplomacy
import game_core as core
import hidden_cast
import phone_map
import town
import world_loop


class CriminalDynamicsTests(unittest.TestCase):
    def test_relations_and_once_only_save_upgrade(self):
        for player, target, expected in [('garrett','syndicate',15), ('garrett','shinokami',15), ('ivan','dragons',15), ('ivan','shinokami',55)]:
            s = core.fresh(player)
            b = diplomacy.ensure(s)
            self.assertEqual(diplomacy.relation(b,target), expected)
            b['relations'][target] += 8
            s = json.loads(json.dumps(s))
            self.assertEqual(diplomacy.relation(diplomacy.ensure(s),target), expected+8)
        s = core.fresh('garrett'); b = diplomacy.ensure(s)
        b.pop('faction_relations_v1'); b['relations']['syndicate'] = 43
        self.assertEqual(diplomacy.ensure(s)['relations']['syndicate'],23)

    def test_plan_is_compartmentalised(self):
        for who in dynamics.INNER:
            self.assertIn('Confidential strategy', dynamics.context(who,['ivan']))
            for listeners in (['ivan','takeo'], ['emily'], ['valentina'], []):
                context = dynamics.context(who,listeners)
                self.assertNotIn('Confidential strategy',context)
                self.assertNotIn('Glasshouse',str(context))
        for who in ('takeo','thirteen','Keisuke Hachimura','garrett','Nessa Quinn'):
            self.assertNotIn('Confidential strategy',dynamics.context(who,['ivan']))
        self.assertEqual(dynamics.context('emily',['ivan']),{})

    def test_hidden_location_guards_and_real_visit(self):
        s = core.fresh('rei')
        before = copy.deepcopy(s)
        self.assertNotIn(dynamics.LAB,phone_map.places(s,'Glasshouse'))
        self.assertEqual(s,before)
        with self.assertRaises(ValueError): town.travel(s,dynamics.LAB)
        s = core.fresh('ivan')
        self.assertIn(dynamics.LAB,phone_map.places(s,'Glasshouse'))
        with self.assertRaises(ValueError): dynamics.laboratory_briefing(s)
        world = s['world']; world['cast']['rei'].update(location=world['location'],journey=None)
        world['party'] = ['rei']
        with self.assertRaises(ValueError): town.travel(s,dynamics.LAB)
        world['party'] = []; town.travel(s,dynamics.LAB)
        self.assertEqual(world['location'],dynamics.LAB)
        self.assertEqual(world['npcs'],[])
        self.assertIn('betray',dynamics.laboratory_briefing(s))
        self.assertIn('Red Magic',dynamics.laboratory_briefing(s))
        self.assertEqual(world_loop.appointment('sylvanis',13*60)[1], dynamics.LAB)

    def test_drug_duration_and_doctrine(self):
        self.assertIn('few minutes',dynamics.DRUGS)
        self.assertIn('more harmful',dynamics.DRUGS)
        self.assertIn('refuse narcotics',dynamics.DOCTRINES['dragons'])
        import crime_operations as ops
        self.assertIn('Blue Magic',ops.CASES['site_04'][0])
        import conversation_lore
        s = core.fresh('ivan')
        self.assertIn('Confidential strategy',conversation_lore.speaker_reference('sylvanis',['ivan'],0,'business',s)['Criminal dynamics'])


    def test_jack_clearance_is_personal_and_revocable(self):
        for branch in ('Clubs','Hearts','Diamonds','Spades'):
            s = core.fresh('rei')
            for rank, strikes, allowed in ((5,0,False),(6,0,True),(7,0,True),(6,2,False)):
                s.setdefault('job_apps', {})['membership'] = dict(faction='Syndicate',branch=branch,rank=rank,strikes=strikes)
                self.assertEqual(dynamics.lab_access('rei',s),allowed)
                self.assertEqual(dynamics.LAB in phone_map.places(s,'Glasshouse'),allowed)
                self.assertFalse(dynamics.lab_access('emily',s))
        s['job_apps']['membership'] = dict(faction='Shinokami',branch='Shinokami',rank=7,strikes=0)
        self.assertFalse(dynamics.lab_access('rei',s))
        s['job_apps']['membership'] = dict(faction='Syndicate',branch='Spades',rank=6,strikes=0)
        town.travel(s,dynamics.LAB)
        self.assertIn('Blue Magic',dynamics.laboratory_briefing(s))
        self.assertNotIn('betray',dynamics.laboratory_briefing(s))
        context=dynamics.context('sylvanis',['rei'],s)
        self.assertIn('Private supply knowledge',context)
        self.assertNotIn('Confidential strategy',context)
        s['world']['cast']['ivan'].update(location=dynamics.LAB,journey=None)
        s['player']='ivan'
        # Save-local Jack membership must not transfer to another cast member.
        with self.assertRaises(ValueError): dynamics.laboratory_briefing(s)
        s['player']='rei'; s['job_apps']['membership']['rank']=5
        with self.assertRaises(ValueError): dynamics.laboratory_briefing(s)
        world_loop.ensure(s)
        self.assertEqual(s['world']['location'],'syndicate_office')
        for who in dynamics.INNER: self.assertTrue(dynamics.lab_access(who,s))

    def test_liaison_fear_and_research_routine(self):
        for who in ('crow','sylvanis','takeo','thirteen'):
            context = dynamics.context(who,['ivan'])
            self.assertIn('does not talk to Mishima',context['Diplomatic liaison'])
        for who in ('Nessa Quinn','garrett','Mina Cho'):
            self.assertIn('fear the Shinokami',dynamics.context(who,['ivan'])['Larger powers'])
        for day in range(7):
            for hour in range(8,23):
                expected=dynamics.LAB if 10 <= hour < 18 else 'syndicate_hq'
                self.assertEqual(world_loop.appointment('sylvanis',day*1440+hour*60)[1],expected)
