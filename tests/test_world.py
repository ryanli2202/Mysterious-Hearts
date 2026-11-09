import consequences
import copy
import json
import tempfile
import unittest
from pathlib import Path
import game_core as c
import town
import world_loop as w

SCENE = {'narration':'A notification appears.', 'dialogue':'hello!', 'choices':['Hi!','How are you?','Busy today?','Talk later?'], 'memory':'They exchanged texts.'}

class WorldTests(unittest.TestCase):
    def test_ivan_chauffeur_and_old_trip_to_shared_home(self):
        s = c.fresh('ivan')
        self.assertEqual(w.trip_vehicle(s, 'ivan', 3), 'Bentley Flying Spur Mulliner')
        self.assertEqual(w.trip_vehicle(s, 'ivan', 4), w.GROUP_VAN)
        town.travel(s, 'home')
        world = s['world']
        self.assertEqual(world['journeys'][-1]['chauffeur'],w.IVAN_CHAUFFEUR)
        # Emulate a pre-instant-travel save midway through a drive.
        world['cast']['ivan']['journey']=copy.deepcopy(world['journeys'][-1])
        world['cast']['ivan']['location']=world['location']='car:ivan'
        world['journeys'][-1]['status']='in transit'
        for trip in (world['cast']['ivan']['journey'], world['journeys'][-1]):
            trip['destination'] = 'ivan_home'
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'old-drive.json'
            c.save(s, path)
            loaded = c.load(path)
        town.finish_drive(loaded)
        self.assertEqual(loaded['world']['location'], town.HOMES['valentina'])
        self.assertEqual(next(j for j in reversed(loaded['world']['journeys']) if j['driver']=='ivan')['status'], 'arrived')

    def test_every_physical_location_has_scene_art(self):
        from artwork import ASSETS, scene_art
        destinations = set(town.LOCATIONS) - {'home'}  # Resolved to the player's own home on travel.
        places = [key for key in destinations if not key.startswith('car:')]
        self.assertEqual(len({scene_art(key) for key in places}), len(places))
        for key in destinations:
            with self.subTest(location=key):
                name = scene_art(key)
                self.assertNotEqual(name, 'ui-header')
                self.assertTrue((ASSETS / (name + '.png')).is_file())
                self.assertEqual(scene_art(key, texting=True), 'ui-header')

    def test_selected_vehicle_and_first_home_visit(self):
        s=c.fresh('garrett')
        town.select_car(s,'Bentley Continental GT')
        town.travel(s,'cafe')
        self.assertEqual(s['world']['journeys'][-1]['vehicle'],'Bentley Continental GT')
        town.wait(s,15)
        self.assertIn('Bentley',str(town.arrival_notes(s,'amy')))
        town.meet(s,'amy')
        town.travel(s,'home','amy')
        town.finish_drive(s)
        self.assertIn('terrace',str(town.arrival_notes(s,'amy')))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json'; c.save(s,path); s=c.load(path)
        self.assertEqual(w.selected_car(s,'garrett'),'Bentley Continental GT')
        self.arrive(s,'square'); self.arrive(s,'home')
        self.assertFalse(town.arrival_notes(s,'amy'))

    def arrive(self,s,place):
        town.travel(s,place); town.finish_drive(s)

    def test_drive_is_persistent_location_with_passenger(self):
        s=c.fresh('rei'); self.arrive(s,'flowers'); town.meet(s,'emily')
        town.travel(s,'rei_home','emily')
        self.assertEqual(s['world']['location'],'rei_home')
        self.assertTrue(w.together(s,'emily'))
        self.assertFalse(c.is_texting(s))
        self.assertIn('Audi',s['world']['journeys'][-1]['vehicle'])
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'story.json'; c.save(s,path); s=c.load(path)
        town.finish_drive(s)
        self.assertEqual(s['world']['location'],'rei_home')
        self.assertEqual(s['world']['cast']['emily']['location'],'rei_home')
        self.assertEqual(next(j for j in reversed(s['world']['journeys']) if j['driver']=='rei')['status'],'arrived')
        self.assertFalse(c.is_texting(s))

    def test_schedule_departure_ends_hangout_and_arrives(self):
        s=c.fresh(); self.arrive(s,'flowers'); town.meet(s,'emily')
        s['world']['minute'] += 2*1440  # Monday, January 3, 2050
        for p in s['autonomy']['people'].values(): p['next_decision']=10**12
        w.advance(s,17*60-s['world']['minute']%1440)
        actor=s['world']['cast']['emily']
        self.assertEqual(actor['location'],'cafe')
        self.assertTrue(c.is_texting(s))
        self.assertIsNone(actor['journey'])
        w.advance(s,15)
        self.assertEqual(actor['location'],'cafe')
        with self.assertRaises(ValueError): town.meet(s,'emily')
        w.advance(s,19*60-s['world']['minute']%1440+15)
        self.assertEqual(actor['location'],'emily_home')

    def test_dynamic_followup_is_queued_without_a_canned_message(self):
        import messaging, autonomy
        from unittest.mock import patch
        s=c.fresh('rei'); t=messaging.thread(s,'emily')
        t['last_reply']=0; s['world']['minute']=900
        s['world']['cast']['emily'].update(location='emily_home',journey=None,activity='Quiet evening')
        n=len(s['routes']['emily']['history'])
        with patch.object(autonomy,'chance',return_value=0): messaging.tick(s)
        self.assertIsNotNone(t['reason'])
        self.assertEqual(len(s['routes']['emily']['history']),n)
        job=messaging.next_job(s)
        messaging.apply(s,job,dict(bubbles=['another thought'],moment='none',pause_minutes=0))
        self.assertEqual(s['routes']['emily']['unread'],1)
        messaging.send(s,'emily','Tell me more')
        self.assertEqual(t['followups'],0)

    def test_followups_for_inactive_routes_respect_sleep(self):
        import messaging, autonomy
        from unittest.mock import patch
        s=c.fresh(); s['active']='amy'; t=messaging.thread(s,'emily'); t['last_reply']=0
        s['world']['minute']=23*60
        s['world']['cast']['emily'].update(location='emily_home',journey=None,activity='Sleep')
        with patch.object(autonomy,'chance',return_value=0): messaging.tick(s)
        self.assertIsNone(t['reason'])
        s['world']['minute']=1440+9*60; s['world']['cast']['emily']['activity']='Quiet morning'
        with patch.object(autonomy,'chance',return_value=0): messaging.tick(s)
        self.assertIsNotNone(t['reason']); self.assertEqual(s['active'],'amy')

    def test_followup_waits_until_sender_finishes_driving(self):
        import messaging
        s=c.fresh(); messaging.initiate(s,'emily','Share a relevant update.')
        w.start_trip(s,'emily','cafe'); s['world']['minute']+=3
        self.assertIsNone(messaging.next_job(s))
        w.advance(s,15)
        self.assertIsNotNone(messaging.next_job(s))

    def test_invalid_travel_and_remote_meeting_do_not_mutate(self):
        s=c.fresh(); before=copy.deepcopy(s)
        with self.assertRaises(ValueError): town.travel(s,'car:emily')
        with self.assertRaises(ValueError): town.travel(s,'cafe','emily')
        with self.assertRaises(ValueError): town.meet(s,'emily')
        with self.assertRaises(ValueError): c.commit(s,'Hello',dict(SCENE,conversation_channel='in_person'))
        self.assertEqual(s,before)
        town.travel(s,'cafe'); before=copy.deepcopy(s)
        with self.assertRaises(ValueError): town.travel(s,'cafe')
        self.assertEqual(s,before)

    def test_homes_schedules_bonds_and_new_attractions(self):
        s=c.fresh('rei'); g=c.fresh('garrett')
        self.assertEqual(len(set(town.HOMES.values())),18); self.assertEqual(len(s['bond_details']),10)
        self.assertEqual(town.HOMES['ivan'], town.HOMES['valentina'])
        self.assertEqual(town.HOMES['yuriko'], town.HOMES['rei'])
        self.assertGreater(s['relationships']['emily']['attraction'],s['relationships']['sophie']['attraction'])
        for state in (s,g):
            self.assertGreater(state['relationships']['samantha']['attraction'],state['relationships']['amy']['attraction'])
        for who,rows in w.SCHEDULES.items():
            self.assertTrue(all(place in town.LOCATIONS for _,place,_ in rows))
            self.assertEqual(w.appointment(who,2*60)[1],w.HOUSES[who][0])
        s['relationships']['emily']['status']='official'
        town.betrayal(s,'sophie','a date')
        consequences.disclose(s, 0, 'emily')
        bond=s['bond_details']['emily:sophie']
        self.assertEqual(bond['tension'],35); self.assertIn('date',bond['events'][-1])
        self.assertTrue(bond['key_points'])

    def test_old_save_migration_keeps_progress_and_old_tension(self):
        s=c.fresh(); del s['world']['cast']; del s['world']['minute']; del s['bond_details']
        s['relationships']['emily']['attraction']=77
        s['girl_bonds']['emily:sophie']='tension from an old overlap'
        town.ensure(s)
        self.assertEqual(s['relationships']['emily']['attraction'],77)
        self.assertEqual(s['bond_details']['emily:sophie']['tension'],30)
        self.assertIn('old overlap',s['bond_details']['emily:sophie']['events'][0])
        before=copy.deepcopy(s); town.ensure(s); self.assertEqual(s,before)

    def test_shared_schedule_builds_bonds_without_erasing_tension(self):
        s=c.fresh()
        s['world']['minute']=2*1440+18*60
        # Deliberately arrange shared free time; dinner is no longer always at the café.
        for who,other in (('sophie','samantha'),('samantha','sophie')):
            s['world']['cast'][who].update(location='boxing_club',journey=None,activity='Hanging out')
            s['autonomy']['people'][who]['plan']=dict(kind='social',venue='boxing_club',until=s['world']['minute']+90,target=other)
        w.advance(s,31)
        bond=s['bond_details']['sophie:samantha']
        self.assertTrue(any('Crossed paths' in e for e in bond['events']))
        self.assertEqual(bond['closeness'],w.BONDS['sophie:samantha'][2]+1)
        count=len(bond['events']); w.advance(s,30)
        self.assertEqual(len(bond['events']),count)
        w.bond_event(s,'sophie','samantha','An unresolved argument.',20)
        w.advance(s,1440)
        self.assertEqual(bond['tension'],20)

    def test_long_wait_matches_small_steps(self):
        a=c.fresh(); c.commit(a,c.INCOMING_TEXT,SCENE); b=copy.deepcopy(a)
        w.advance(a,500)
        for _ in range(500): w.advance(b,1)
        self.assertEqual(a,b)



    def test_dynamic_followup_ignores_real_time_and_reading(self):
        import messaging
        s=c.fresh(); route=s['routes']['amy']; route['idle_wait']=100000
        t=messaging.thread(s,'amy'); t['last_reply']=s['world']['minute']
        start=s['world']['minute']
        for _ in range(100): w.idle_messages(s)
        self.assertIsNone(t['reason']); self.assertEqual(s['world']['minute'],start)
        t['followups']=2; route['unread']=0
        w.idle_messages(s); self.assertEqual(t['followups'],2)
        messaging.send(s,'amy','Hello again'); self.assertEqual(t['followups'],0)

    def test_fixed_costs_and_free_scene_openings(self):
        s=c.fresh(); start=s['world']['minute']
        c.commit(s,c.INCOMING_TEXT,SCENE)
        self.assertEqual(s['world']['minute'],start)
        c.commit(s,'word '*50,dict(SCENE,dialogue='reply '*150))
        self.assertEqual(s['world']['minute'],start)
        c.commit(s,'[Action] I wave.',SCENE)
        self.assertEqual(s['world']['minute'],start)
        # Physical hangouts also rely exclusively on the real-time clock.
        town.summon(s,'emily'); start=s['world']['minute']
        c.commit(s,'Hello',dict(SCENE,conversation_channel='in_person'))
        self.assertEqual(s['world']['minute'],start)
        c.commit(s,'[Action] I wave.',dict(SCENE,conversation_channel='in_person'))
        self.assertEqual(s['world']['minute'],start)
        self.assertFalse(hasattr(w,'FOLLOWUPS'))  # No fixed follow-up templates remain.
