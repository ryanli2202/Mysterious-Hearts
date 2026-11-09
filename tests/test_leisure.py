import copy
import json
import unittest
from unittest.mock import patch

import autonomy
import game_core as core
import leisure
import world_loop as world


class LeisureTests(unittest.TestCase):
    def tearDown(self):
        world.appointment.cache_clear()

    def test_outings_are_varied_and_public_over_two_weeks(self):
        selections=[]
        for who in leisure.PREFERENCES:
            venues={leisure.choose(who,day*1440+slot*60) for day in range(14) for slot in (11,14,17)}
            self.assertGreaterEqual(len(venues),4,who)
            self.assertTrue(venues<=set(leisure.PREFERENCES[who]))
            self.assertTrue(venues<=core.town.LOCATIONS.keys())
            selections.extend(leisure.choose(who,day*1440+14*60) for day in range(14))
        self.assertGreaterEqual(len(set(selections)),15)
        self.assertLess(selections.count('cafe')/len(selections),.12)

    def test_rain_uses_multiple_indoor_destinations(self):
        with patch('weather.shelter',return_value=True):
            places={leisure.choose(who,14*60) for who in leisure.PREFERENCES}
        self.assertFalse(places & leisure.OUTDOORS)
        self.assertGreaterEqual(len(places),6)

    def test_recent_visits_and_crowds_discourage_repeating_a_venue(self):
        s=core.fresh('rei')
        first=leisure.social_destination(s,'emily','sophie')
        autonomy.person(s,'emily')['recent_venues']=[first]
        self.assertNotEqual(leisure.social_destination(s,'emily','sophie'),first)
        for actor in s['world']['cast'].values(): actor['location']=first
        self.assertNotEqual(leisure.social_destination(s,'emily','sophie'),first)
        restored=json.loads(json.dumps(s))
        self.assertEqual(leisure.social_destination(s,'emily','sophie'),leisure.social_destination(restored,'emily','sophie'))

    def test_peer_plans_share_destination_and_fit_the_location(self):
        s=core.fresh('rei'); s['world']['minute']=14*60
        for who,p in s['autonomy']['people'].items():
            p.update(next_decision=10**12,next_initiation=10**12)
        for who,other in (('emily','sophie'),('sophie','emily')):
            s['world']['cast'][who].update(location=world.HOUSES[who][0],activity='Free time')
            p=autonomy.person(s,who)
            p['relationships']={other:dict(interest=80,closeness=70,trust=70,tension=0)}
        autonomy.person(s,'emily')['next_decision']=0
        def chance(*parts): return 0 if parts[-1]=='peer' else 1
        with patch.object(autonomy,'chance',side_effect=chance): autonomy.tick(s)
        a=autonomy.person(s,'emily')['plan']; b=autonomy.person(s,'sophie')['plan']
        self.assertEqual(a['venue'],b['venue'])
        self.assertEqual(a['activity'],leisure.ACTIVITIES[a['venue']])
        self.assertEqual(a['activity'],b['activity'])

    def test_weekend_routines_actually_move_characters_between_outings(self):
        s=core.fresh('rei')
        for p in s['autonomy']['people'].values(): p.update(next_decision=10**12,next_initiation=10**12)
        s['world']['minute']=10*60+59
        world.advance(s,1)
        for who in ('amy','april','samantha','minsu'):
            self.assertEqual(s['world']['cast'][who]['location'],world.appointment(who,11*60)[1])
        world.advance(s,180)
        for who in ('amy','april','samantha','minsu'):
            self.assertEqual(s['world']['cast'][who]['location'],world.appointment(who,14*60)[1])

    def test_work_sleep_and_agreed_plans_keep_priority(self):
        weekday=2*1440
        self.assertEqual(world.appointment('emily',weekday+10*60)[1],'flowers')
        self.assertEqual(world.appointment('minsu',weekday+10*60)[1],'campus')
        self.assertEqual(world.appointment('amy',weekday+2*60)[2],'Sleep')
        s=core.fresh('rei')
        s['world']['minute']=11*60-1
        s['world']['cast']['emily'].update(location='chess',activity='Hanging out')
        s['world']['location']='chess'; s['world']['cast']['rei']['location']='chess'
        autonomy.person(s,'emily')['plan']=dict(kind='visit',venue='chess',until=12*60,target='rei',accepted=True)
        world.advance(s,2)
        self.assertEqual(s['world']['cast']['emily']['location'],'chess')
