import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as core
import flashback_visits as visits
import campaign_flashbacks
import combat
import world_loop
from simulation_clock import SimulationClock


def fresh(player='rei'):
    s=core.fresh(player)
    s['world']['cast'][player].update(journey=None,activity='Relaxing',location=s['world']['location'])
    return s


def reply(who):
    return dict(narration='A breeze lifts the edge of the sketchbook.',lines=[dict(speaker=who,text='Come sit with me. What would you like to make?')])


class FlashbackVisitTests(unittest.TestCase):
    def test_exact_access_and_cast(self):
        for who in core.PLAYERS:
            s=fresh(who)
            if who in ('rei','emily','sophie','garrett'):
                visits.enter(s)
                expected={'charles'} if who=='garrett' else {'rei','emily','sophie','marcus'}-{who}
                self.assertEqual(set(visits.active(s)['members']),expected)
                self.assertEqual(set(visits.portraits(s)),expected|{who})
            else:
                with self.assertRaises(ValueError):visits.enter(s)
                self.assertNotIn('flashback_memories',s)

    def test_talk_action_and_exit_never_change_live_story(self):
        for player in ('rei','emily','sophie','garrett'):
            s=fresh(player);before=copy.deepcopy(s)
            visits.enter(s);who=visits.available(s)[-1];visits.select(s,[who])
            for kind in ('speak','action'):
                visits.commit(s,visits.stamp(s),'Share a story',kind,reply(who))
            visits.leave(s)
            after={k:v for k,v in s.items() if k not in ('flashback_visit','flashback_memories')}
            self.assertEqual(before,after)
            visits.enter(s)
            self.assertEqual(len(visits.record(s)['history']),2)
            self.assertEqual(visits.active(s)['members'],[who])

    def test_clock_pauses_without_fraction_or_catchup(self):
        s=fresh();s['world'].update(time_mode='fast',clock_fraction=.4)
        clock=SimulationClock();clock.reset(s,0);before=copy.deepcopy(s['world'])
        visits.enter(s)
        self.assertEqual(clock.tick(s,now=1200),0)
        self.assertEqual(before,s['world'])
        with self.assertRaises(ValueError):world_loop.advance(s,20)
        with self.assertRaises(ValueError):core.town.travel(s,'cafe')
        with self.assertRaises(ValueError):combat.guard(s)
        visits.leave(s);clock.reset(s,1200)
        self.assertEqual(clock.tick(s,now=1200),0)
        self.assertEqual(s['world']['minute'],before['minute'])

    def test_real_save_resume_and_independent_campaign(self):
        s=fresh('garrett');pending=campaign_flashbacks.pending(s)
        self.assertIsNotNone(pending)
        visits.enter(s)
        visits.commit(s,visits.stamp(s),'How was your day?','speak',reply('charles'))
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'memory.json';core.save(s,path);loaded=core.load(path)
        self.assertEqual(visits.active(loaded),visits.active(s))
        self.assertEqual(visits.record(loaded),visits.record(s))
        self.assertEqual(campaign_flashbacks.pending(loaded),pending)
        self.assertIsNone(loaded.get('campaign_dialogue'))
        self.assertNotIn('marcus',loaded['world']['cast'])

    def test_stale_duplicate_cancelled_and_changed_group_responses(self):
        s=fresh();visits.enter(s);visits.select(s,['marcus']);stamp=visits.stamp(s)
        visits.commit(s,stamp,'Hello','speak',reply('marcus'))
        with self.assertRaises(ValueError):visits.commit(s,stamp,'Hello','speak',reply('marcus'))
        stamp=visits.stamp(s);visits.select(s,['emily'])
        with self.assertRaises(ValueError):visits.commit(s,stamp,'Hello','speak',reply('marcus'))
        stamp=visits.stamp(s);visits.leave(s);visits.enter(s)
        with self.assertRaises(ValueError):visits.commit(s,stamp,'Hello','speak',reply('emily'))
        self.assertEqual(len(visits.record(s)['history']),1)

    def test_prompt_contains_only_historical_context(self):
        s=fresh('garrett');s['spoiler']='TOP SECRET FUTURE';s['world']['future_secret']='TOP SECRET FUTURE'
        visits.enter(s)
        system,context,schema=visits.prompt(s,'Hello','speak')
        self.assertNotIn('TOP SECRET FUTURE',json.dumps(context))
        self.assertEqual(context['player']['age'],16)
        self.assertEqual(context['companions'][0]['age'],21)
        self.assertIn('not time travel',system);self.assertIn('nonsexual',system)
        self.assertNotIn('world',context);self.assertEqual(schema['properties']['lines']['items']['properties']['speaker']['enum'],['charles'])

    def test_provider_adapter_and_invalid_output_are_atomic(self):
        s=fresh();visits.enter(s);visits.select(s,['marcus']);before=copy.deepcopy(s)
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(reply('marcus'))}}) as request:
            result=visits.generate(s,'Hello','speak')
        self.assertEqual(s,before);self.assertEqual(result,reply('marcus'))
        self.assertEqual(request.call_args.args[0],'/api/chat')
        for bad in (reply('charles'),dict(reply('marcus'),world={}),dict(narration='Here',lines=[])):
            with self.assertRaises(ValueError):visits.commit(s,visits.stamp(s),'Hello','speak',bad)
        self.assertEqual(s,before)

    def test_validation_blocks_wrong_members_and_interrupted_campaign(self):
        s=fresh();visits.enter(s)
        for members in ([],['rei'],['charles'],['Joseph Richter']):
            with self.assertRaises(ValueError):visits.select(s,members)
        visits.leave(s)
        s['campaign_dialogue']={'cursor':0}
        with self.assertRaises(ValueError):visits.enter(s)
        s['campaign_dialogue']=None;s['world']['cast']['rei']['journey']={'to':'cafe'}
        with self.assertRaises(ValueError):visits.enter(s)

    def test_portrait_override_clears_on_exit(self):
        s=fresh('emily');visits.enter(s)
        for who in ('rei','emily','sophie','marcus'):
            path=campaign_flashbacks.portrait_path(s,who)
            self.assertEqual(path.name,who+'-high-school.png');self.assertTrue(path.is_file())
        visits.leave(s)
        self.assertIsNone(campaign_flashbacks.portrait_path(s,'emily'))


if __name__=='__main__':unittest.main()
