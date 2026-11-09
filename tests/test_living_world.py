import copy
import json
import unittest
import game_core as core
import town
import weather
import living_world as living
import consequences
import world_loop

class LivingWorldTests(unittest.TestCase):
    def test_forecast_matches_future_and_reload(self):
        s=core.fresh(); minute=1430
        f=weather.forecast(minute)
        self.assertEqual(f['hourly'][2],weather.at(minute+120))
        self.assertEqual(f['daily'][1],weather.daily(1))
        self.assertEqual(f,weather.forecast(minute))
        self.assertEqual(weather.at(0)['light'],'night')
        self.assertTrue(all(w['low']<=w['temperature']<=w['high'] for w in f['hourly']))
        before=copy.deepcopy(s); weather.forecast(s['world']['minute']); self.assertEqual(s,before)

    def test_additive_migration_and_project_progress(self):
        s=core.fresh('rei'); s.pop('living_world')
        old=copy.deepcopy(s['relationships']); town.ensure(s)
        self.assertEqual(old,s['relationships'])
        first=living.project(s,'emily')
        s['world']['minute']+=6*1440
        self.assertEqual(living.project(s,'emily')['stage'],0)  # Clock jumps alone do not do project work.
        living.ensure(s)['projects']['emily']['work_minutes']=360
        self.assertEqual(living.project(s,'emily')['stage'],3)
        self.assertFalse(living.project(s,'emily')['helped'])
        self.assertEqual(first['stage'],0)

    def test_help_requires_presence_and_cannot_repeat(self):
        s=core.fresh('rei')
        with self.assertRaises(ValueError): living.participate(s,'emily')
        town.summon(s,'emily'); living.participate(s,'emily')
        self.assertTrue(living.project(s,'emily')['helped'])
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError): living.participate(s,'emily')
        self.assertEqual(before,s)

    def test_actual_visits_make_rituals_and_keepsakes(self):
        s=core.fresh('rei')
        for day in range(3):
            s['world']['minute']=day*1440+840
            s['world']['location']='cinema'
            s['world']['cast']['rei']['location']='cinema'
            town.summon(s,'emily')
            s['world']['party']=['emily']
            living.visit(s)
        self.assertEqual(len(living.ensure(s)['rituals']['emily:cinema']),3)
        self.assertTrue(living.context(s,['emily'])['shared_rituals'])
        self.assertFalse(living.context(s,['sophie'])['shared_rituals'])
        self.assertFalse(living.context(s,['emily','sophie'])['shared_rituals'])
        self.assertEqual(len(living.ensure(s)['keepsakes']),3)
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError): living.visit(s)
        self.assertEqual(before,s)

    def test_mystery_is_gated_persistent_and_bounded(self):
        s=core.fresh('garrett')
        with self.assertRaises(ValueError): living.investigate(s)
        s['charles_lead']='traced'
        for index,(_,venue,*_) in enumerate(living.MYSTERY):
            s['world']['minute']+=1440
            s['world']['location']=venue
            living.investigate(s)
            self.assertEqual(len(living.ensure(s)['mystery']),index+1)
        restored=json.loads(json.dumps(s))
        self.assertEqual(living.ensure(s),living.ensure(restored))
        with self.assertRaises(ValueError): living.investigate(s)

    def test_private_betrayal_and_explicit_disclosure(self):
        s=core.fresh('rei'); s['relationships']['emily']['status']='official'
        town.betrayal(s,'sophie','a date')
        self.assertEqual(s['relationships']['emily']['status'],'official')
        self.assertFalse(s['relationships']['emily']['known_betrayals'])
        report=living.ensure(s)['reports'][0]
        self.assertNotIn(report['text'],town.context(s,'emily'))
        consequences.disclose(s,0,'emily')
        self.assertEqual(s['relationships']['emily']['status'],'strained')
        self.assertIn(report['text'],town.context(s,'emily'))
        self.assertNotIn(report['text'],town.context(s,'amy'))
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError): consequences.disclose(s,0,'emily')
        self.assertEqual(before,s)

    def test_physical_witness_and_legacy_knowledge(self):
        s=core.fresh('rei'); s['relationships']['emily']['status']='official'
        town.summon(s,'emily'); town.summon(s,'sophie')
        s['routes']['sophie']['channel']='in_person'
        town.betrayal(s,'sophie','kiss')
        self.assertEqual(s['relationships']['emily']['status'],'strained')
        self.assertEqual(living.ensure(s)['reports'][0]['known']['emily'],'witnessed in person')
        s['relationships']['amy']['known_betrayals'].append('Previously disclosed event')
        town.ensure(s)
        self.assertIn('Previously disclosed event',town.context(s,'amy'))

    def test_individual_routines_and_weather_shelter(self):
        # Weekday after work, avoiding the authored quiet-home day.
        minute=4*1440+18*60
        places={world_loop.appointment(who,minute)[1] for who in ('lena','naomi','celeste','dev','rosa','elliot')}
        self.assertGreater(len(places),3)
        rainy=next(day for day in range(100) if day%3 and not world_loop.dates.free_day(world_loop.dates.story_date(day*1440)) and weather.shelter(day*1440))
        import leisure
        self.assertNotIn(world_loop.appointment('elliot',rainy*1440+18*60)[1],leisure.OUTDOORS)

    def test_public_bulletins_have_preparation_and_aftermath(self):
        s=core.fresh()
        s['world']['minute']=3*1440
        self.assertTrue(any('Preparing' in n['title'] for n in living.news(s)))
        s['world']['minute']=6*1440
        self.assertTrue(any('Afterward' in n['title'] for n in living.news(s)))

if __name__=='__main__': unittest.main()
