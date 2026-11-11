import copy
import json
import queue
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import autonomy
import game_core as core
import grove
import messaging
import phone_apps as apps
import scheduled_events
import town
import world_loop as world
from simulation_clock import SimulationClock


class InlineThread:
    def __init__(self, target, **kwargs): self.target=target
    def start(self): self.target()


class ClockTests(unittest.TestCase):
    def setUp(self):
        self.s=core.fresh('rei')
        # Existing integration scenarios exercise the selectable 40-minute day.
        self.s['world']['time_mode']='fast'
        self.clock=SimulationClock()
        self.clock.reset(self.s,0)

    def game(self):
        return SimpleNamespace(state_data=self.s,in_game=True,busy=False,suggestion_job=None,
                               persist=Mock(),render=Mock(),bind=Mock())

    def test_all_day_lengths_and_default(self):
        for mode, seconds in ((None,7200),('slow',14400),('normal',7200),('fast',2400),('faster',900)):
            with self.subTest(mode=mode):
                s=core.fresh('rei')
                if mode is not None: s['world']['time_mode']=mode
                clock=SimulationClock(); clock.reset(s,0)
                with patch.object(world,'advance') as advance:
                    self.assertEqual(clock.tick(s,now=seconds),1440)
                self.assertEqual(sum(call.args[1] for call in advance.call_args_list),1440)

    def test_half_speed_switch_and_save_restore(self):
        self.s['world']['time_mode']='normal'
        self.clock.set_mode(self.s,'slow',now=2)
        self.assertAlmostEqual(self.s['world']['clock_fraction'],.4)
        self.assertEqual(self.clock.tick(self.s,now=8),1)
        self.assertEqual(self.s['world']['minute'],481)
        restored=json.loads(json.dumps(self.s))
        self.assertEqual(restored['world']['time_mode'],'slow')
        self.assertEqual(self.clock.tick(restored,now=10000),0)
        self.assertEqual(self.clock.tick(restored,now=10010),1)
        self.clock.set_mode(restored,'normal',now=10010)
        self.assertEqual(self.clock.tick(restored,now=10020),2)

    def test_mode_switch_preserves_fraction_and_pause_has_no_catchup(self):
        self.s['world'].pop('time_mode')
        self.clock.set_mode(self.s,'fast',now=2)  # 0.4 game minutes at normal speed.
        self.clock.set_mode(self.s,'paused',now=3)  # Another 0.6 minutes at fast speed.
        self.assertEqual(self.s['world']['minute'],481)
        self.assertEqual(self.clock.tick(self.s,now=10000),0)
        self.clock.set_mode(self.s,'faster',now=20000)
        self.clock.tick(self.s,now=20005)
        self.assertEqual(self.s['world']['minute'],489)

    def test_saved_pause_stops_sleep_and_preserves_fraction(self):
        town.travel(self.s,'home'); autonomy.advance_player(self.s,'nap')
        autonomy.advance_player(self.s,'sleep_faster')
        self.clock.set_mode(self.s,'paused',now=0)
        self.s['world']['clock_fraction']=.5
        restored=json.loads(json.dumps(self.s))
        self.clock.tick(restored,now=10000)
        self.clock.tick(restored,now=20000)
        self.assertEqual(restored['world']['minute'],480)
        self.assertEqual(restored['world']['clock_fraction'],.5)
        self.clock.set_mode(restored,'normal',now=20000)
        self.clock.tick(restored,now=20005)
        self.assertEqual(restored['world']['minute'],492)

    def test_forty_real_minutes_is_exactly_one_day_with_all_ticks(self):
        start=self.s['world']['minute']; seen=[]
        original=messaging.tick
        def observe(state):
            seen.append(state['world']['minute'])
            original(state)
        with patch.object(messaging,'tick',side_effect=observe):
            self.assertEqual(self.clock.tick(self.s,now=2400),1440)
        self.assertEqual(self.s['world']['minute'],start+1440)
        self.assertEqual(seen,list(range(start+1,start+1441)))

    def test_subsecond_polls_do_not_drift_or_charge_actions(self):
        with patch.object(world,'advance') as advance:
            for i in range(1,24001): self.clock.tick(self.s,now=i/10)
        self.assertEqual(sum(c.args[1] for c in advance.call_args_list),1440)
        self.assertLess(self.s['world']['clock_fraction'],1e-8)

    def test_menu_and_reloaded_save_do_not_accumulate_offline_time(self):
        self.clock.tick(self.s,now=1)
        self.clock.tick(self.s,active=False,now=2)
        self.clock.tick(self.s,active=True,now=10000)
        self.assertEqual(self.s['world']['minute'],480)
        restored=json.loads(json.dumps(self.s))
        self.clock.tick(restored,now=20000)
        self.clock.tick(restored,now=20001)
        self.assertEqual(restored['world']['minute'],481)
        self.assertAlmostEqual(restored['world']['clock_fraction'],.2)

    def test_midnight_processes_2359_then_0000_without_morning_skip(self):
        self.s['world']['minute']=1438
        observed=[]
        original=scheduled_events.tick
        def tick(state):
            observed.append(state['world']['minute'])
            original(state)
        with patch.object(scheduled_events,'tick',side_effect=tick):
            self.clock.tick(self.s,now=10/3)
        self.assertEqual(observed,[1439,1440])
        self.assertIn('00:00',world.clock(self.s))
        self.assertEqual(world.dates.story_date(1440).day,2)

    def test_poll_keeps_time_and_message_worker_running_during_scene_generation(self):
        from game import Game
        game=self.game()
        game.busy=True; game.pending='A spoken reply'
        game.simulation_clock=self.clock
        game.events=queue.Queue(); game.message_pump=SimpleNamespace(tick=Mock())
        for name in ('capture_draft','update_phone_notification','after','wait_status','poll'):
            setattr(game,name,Mock())
        game.sounds=SimpleNamespace(observe=Mock()); game.status=Mock()
        game.notification_popups=SimpleNamespace(observe=Mock())
        with patch('simulation_clock.time.monotonic',return_value=5): Game.poll(game)
        self.assertEqual(self.s['world']['minute'],483)
        game.message_pump.tick.assert_called_once()
        self.assertEqual(game.pending,'A spoken reply')

    def test_waiting_message_is_generated_and_delivered_by_background_pump(self):
        self.s['world']['cast']['emily'].update(location='flowers',activity='Flower-shop shift')
        messaging.send(self.s,'emily','How is your morning?')
        self.assertIsNone(messaging.next_job(self.s))
        self.clock.tick(self.s,now=30)
        game=self.game(); game.busy=True; game.suggestion_job={'pending':True}
        pump=messaging.MessagePump(game)
        result=dict(bubbles=['Good! Just taking a break.'],moment='none',pause_minutes=0)
        with patch.object(messaging,'generate',return_value=result), patch.object(messaging.threading,'Thread',InlineThread):
            pump.tick(); pump.tick()
        self.assertFalse(messaging.thread(self.s,'emily')['pending'])
        self.assertEqual(self.s['routes']['emily']['dialogue'],result['bubbles'][0])

    def test_grove_posts_and_player_replies_drain_without_clock_jumps(self):
        data=apps.ensure(self.s)
        data['grove_next']={who:10**9 for who in apps.contacts(self.s)}
        data['grove_next']['emily']=481
        self.clock.tick(self.s,now=5/3)
        self.assertEqual(data['grove_pending'][0]['author'],'emily')
        game=self.game(); game.busy=True; game.suggestion_job={'pending':True}
        pump=grove.GrovePump(game)
        def generate(state,job): return dict(text='A little flower update.',parent=job['parent'])
        with patch.object(pump.photos,'tick'), patch.object(grove,'generate',side_effect=generate), patch.object(grove.threading,'Thread',InlineThread):
            pump.tick(); pump.tick()
            post=data['posts'][-1]
            apps.post(self.s,'Those look lovely!',post['id'])
            reply=data['posts'][-1]
            pump.tick(); pump.tick()
        self.assertEqual(data['posts'][-1]['parent'],reply['id'])
        self.assertEqual(data['posts'][-1]['author'],'emily')
        self.assertEqual(self.s['world']['minute'],481)

    def test_calendar_reminders_and_attendance_follow_real_time(self):
        event=scheduled_events.create(self.s,'Tea',world.dates.START.isoformat(),'09:05','cafe',['emily'],30)
        self.clock.tick(self.s,now=65/.6)
        self.assertEqual(event['reminded'],[60,15])
        self.assertEqual(self.s['world']['cast']['emily']['location'],'cafe')
        town.travel(self.s,'cafe')
        self.clock.tick(self.s,now=96/.6)
        self.assertEqual(event['memory_phase'],'completed')

    def test_sleep_and_travel_do_not_advance_clock(self):
        town.summon(self.s,'emily')
        town.travel(self.s,'home','emily')
        self.assertTrue(world.together(self.s,'emily'))
        self.assertEqual(self.s['world']['minute'],480)
        self.assertTrue(all(a['journey'] is None for a in self.s['world']['cast'].values()))
        energy=autonomy.person(self.s,'rei')['energy']
        autonomy.advance_player(self.s,'nap')
        self.assertEqual(self.s['world']['minute'],480)
        self.clock.tick(self.s,now=100)
        self.assertGreater(autonomy.person(self.s,'rei')['energy'],energy)
        self.assertNotEqual(autonomy.status(self.s,'rei'),'Asleep')

    def test_home_actions_leave_time_to_clock_but_work_consumes_a_shift(self):
        town.travel(self.s,'home')
        town.home_action(self.s,town.HOME_ACTIONS['rei'][0])
        town.travel(self.s,'cafe'); town.work(self.s)
        self.assertEqual(self.s['world']['minute'],540)

    def test_hangout_actions_leave_time_to_running_or_paused_clock(self):
        import groups
        for mode in ('fast', 'paused'):
            with self.subTest(mode=mode):
                s = core.fresh('rei')
                s['world']['time_mode'] = mode
                for who in ('rei', 'emily', 'sophie'):
                    s['world']['cast'][who].update(location='cafe', journey=None)
                s['world']['location'] = 'cafe'
                gid = groups.open_group(s, ['emily', 'sophie'])
                clock = SimulationClock()
                clock.reset(s, 0)
                before = s['world']['minute']
                result = dict(narration='Emily smiles as you lift your cup.',
                    choices=[], suggestions_deferred=True,
                    lines=[dict(speaker='Emily Fields', text='Cheers!')],
                    emotions={'rei':'content', 'emily':'content', 'sophie':'content'},
                    bond_moments={'emily':'none', 'sophie':'none'},
                    social_target='none', social_event='none')
                groups.commit(s, gid, core.ACTION_PREFIX+'I lift my cup.', result)
                self.assertEqual(s['world']['minute'], before)
                self.assertEqual(s['groups'][gid]['history'][-3]['kind'], 'action')
                clock.tick(s, now=5)
                self.assertEqual(s['world']['minute'], before + (3 if mode == 'fast' else 0))

    def test_clock_batch_matches_small_steps_for_entire_world(self):
        other=copy.deepcopy(self.s); other_clock=SimulationClock(); other_clock.reset(other,0)
        self.clock.tick(self.s,now=200)
        for second in range(1,201): other_clock.tick(other,now=second)
        self.assertAlmostEqual(self.s['world'].pop('clock_fraction'),other['world'].pop('clock_fraction'))
        self.assertEqual(self.s,other)

    def test_sleep_speed_only_accelerates_until_waking(self):
        town.travel(self.s,'home'); autonomy.advance_player(self.s,'nap')
        autonomy.advance_player(self.s,'sleep_faster')
        # First 8 1/3 seconds finish the 60-minute nap; the rest run at 1x.
        self.clock.tick(self.s,now=25)
        self.assertEqual(self.s['world']['minute'],550)
        self.assertEqual(self.s['world']['sleep_speed'],1)

    def test_sleep_speed_can_change_and_waking_restores_normal_time(self):
        town.travel(self.s,'home'); autonomy.advance_player(self.s,'sleep')
        autonomy.advance_player(self.s,'sleep_fast')
        self.clock.tick(self.s,now=10)
        self.assertEqual(self.s['world']['minute'],504)
        autonomy.advance_player(self.s,'sleep_normal')
        self.clock.tick(self.s,now=20)
        self.assertEqual(self.s['world']['minute'],510)
        autonomy.advance_player(self.s,'sleep_faster')
        autonomy.advance_player(self.s,'wake')
        self.clock.tick(self.s,now=30)
        self.assertEqual(self.s['world']['minute'],516)

    def test_awake_player_cannot_speed_up_or_skip(self):
        for action in ('sleep_fast','sleep_faster','sleep_skip'):
            with self.assertRaises(ValueError): autonomy.advance_player(self.s,action)
        self.assertEqual(self.s['world']['minute'],480)

    def test_skip_sleep_matches_all_normal_ticks_across_midnight(self):
        town.travel(self.s,'home'); self.s['world']['minute']=23*60
        autonomy.advance_player(self.s,'sleep')
        messaging.send(self.s,'emily','Good morning when you wake up!')
        apps.sync(self.s)
        other=copy.deepcopy(self.s)
        world.advance(other,480)
        other['world'].update(sleep_speed=1,clock_fraction=0.)
        autonomy.person(other,'rei')['sleep_until']=None
        seen=[]
        original=messaging.tick
        def tick(state):
            seen.append(state['world']['minute']); original(state)
        with patch.object(messaging,'tick',side_effect=tick):
            autonomy.advance_player(self.s,'sleep_skip')
        self.assertEqual(self.s,other)
        self.assertEqual(seen,list(range(1381,1861)))
        self.assertTrue(apps.ensure(self.s)['grove_pending'])
        self.assertIsNotNone(messaging.next_job(self.s))

    def test_sleep_speed_survives_save_without_offline_advancement(self):
        town.travel(self.s,'home'); autonomy.advance_player(self.s,'nap')
        autonomy.advance_player(self.s,'sleep_fast')
        restored=json.loads(json.dumps(self.s))
        self.clock.tick(restored,now=10000)
        self.clock.tick(restored,now=10010)
        self.assertEqual(restored['world']['minute'],504)
