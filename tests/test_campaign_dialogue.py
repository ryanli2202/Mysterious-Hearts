import copy
import json
import unittest
from unittest.mock import patch, Mock
import tempfile
from pathlib import Path
import game_core as core
import campaign_dialogue as dialogue
import organisation_guards as guards
import rei_story
import combat
import simulation_clock
from test_major_campaigns import arrive, clear, investigate, win
from flashback_helpers import finish_scene

class CampaignDialogueTests(unittest.TestCase):
    def test_action_choices_and_legacy_saves_are_not_speech(self):
        s=core.fresh('rei');arrive(s,'rei_home')
        dialogue.begin(s,'rei_story.advance',(0,))
        b=next(b for b in s['campaign_dialogue']['beats'] if b.get('action'))
        self.assertEqual(b['player'],'')
        self.assertEqual(b['action'],rei_story.SCENES[0][3][0])
        b['player']=b.pop('action')
        dialogue.normalize_actions(s['campaign_dialogue'])
        self.assertEqual(b['player'],'')
        self.assertIn('action',b)
        # Real spoken answers and confrontation dialogue remain speech.
        d=dict(action='charles_quest.advance',beats=[dialogue.beat('Our father’s chipped teacup')])
        dialogue.normalize_actions(d)
        self.assertTrue(d['beats'][0]['player'])

    def test_gamemaster_schema_and_invalid_response(self):
        b=dialogue.action_beat('Compare copies','Authorship remains unverified.')
        with patch.object(combat,'ask_ai',return_value={'narration':'Garrett compares the copies.'}) as ai:
            self.assertEqual(dialogue.generate_action_narration('garrett','archive',b),'Garrett compares the copies.')
            self.assertIn('Authorship remains unverified.',ai.call_args.args[0])
            self.assertIn('Do not invent evidence',ai.call_args.args[0])
        with patch.object(combat,'ask_ai',return_value={'narration':''}):
            with self.assertRaises(ValueError):dialogue.generate_action_narration('rei','archive',b)

    def test_async_narration_caches_and_discards_stale_results(self):
        b=dialogue.action_beat('Copy records','The dates are uncertain.')
        d=dict(player='rei',venue='archive',beats=[b],cursor=0)
        game=Mock(state_data={'campaign_dialogue':d},_campaign_narration_job=None)
        def start(**kwargs):
            return Mock(start=kwargs['target'])
        with patch.object(dialogue.threading,'Thread',side_effect=start), patch.object(dialogue,'generate_action_narration',return_value='Rei copies the dated records.') as generate, patch.object(dialogue,'show'):
            dialogue.request_narration(game,d,b)
            dialogue.request_narration(game,d,b)
            self.assertEqual(generate.call_count,1)
            game.after.call_args.args[1]()
            self.assertEqual(b['gm_narration'],'Rei copies the dated records.')
            game.persist.assert_called_once()
            b.pop('gm_narration');game._campaign_narration_job=None
            dialogue.request_narration(game,d,b)
            game.state_data={}
            game.after.call_args.args[1]()
            self.assertNotIn('gm_narration',b)
            self.assertEqual(game.persist.call_count,1)

    def test_scene_only_commits_after_final_line_and_reload(self):
        s=core.fresh('rei');arrive(s,'rei_home')
        dialogue.begin(s,'rei_story.advance',(0,))
        self.assertEqual(rei_story.data(s)['stage'],0)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'story.json';core.save(s,path);s=core.load(path)
        dialogue.next_line(s)
        self.assertEqual(rei_story.data(s)['stage'],0)
        finish_scene(s)
        self.assertEqual(rei_story.data(s)['stage'],1)
        with self.assertRaises(ValueError):dialogue.next_line(s)

    def test_narration_failure_keeps_action_without_committing_outcome(self):
        s=core.fresh('rei');arrive(s,'rei_home')
        dialogue.begin(s,'rei_story.advance',(0,));dialogue.next_line(s)
        d=s['campaign_dialogue'];d['cursor']=len(d['beats'])-1;b=d['beats'][-1];b['_request_narration']=True
        game=Mock(state_data=s,_campaign_narration_job=None)
        with patch.object(dialogue.threading,'Thread',side_effect=lambda **kw: Mock(start=kw['target'])), patch.object(dialogue,'generate_action_narration',side_effect=RuntimeError('offline')), patch.object(dialogue,'show'):
            dialogue.request_narration(game,d,b)
            game.after.call_args.args[1]()
        self.assertIn('unavailable',b['_narration_error'])
        self.assertEqual(b['player'],'')
        self.assertEqual(rei_story.data(s)['stage'],0)
        self.assertNotIn('gm_narration',b)

    def test_clock_and_travel_pause_during_script(self):
        s=core.fresh('rei');arrive(s,'rei_home');dialogue.begin(s,'rei_story.advance',(0,))
        clock=simulation_clock.SimulationClock();clock.reset(s,0);before=s['world']['minute']
        self.assertEqual(clock.tick(s,now=300),0);self.assertEqual(before,s['world']['minute'])
        with self.assertRaises(ValueError):core.town.travel(s,'square')
        with self.assertRaises(ValueError):combat.guard(s)

    def test_richter_portrait_dialogue_then_real_fight_then_apology(self):
        s=core.fresh('rei');investigate(s);clear(s,guards.BLACKSTONE,'rei:blackstone')
        dialogue.begin(s,'rei_story.confront')
        self.assertFalse(combat.active(s))
        self.assertIn('Joseph',str(s['campaign_dialogue']['beats']))
        finish_scene(s)
        self.assertEqual(combat.active(s)['opponent'],'Joseph Richter')
        win(s);dialogue.activate_epilogue(s)
        self.assertTrue(any('sorry' in str(b) for b in s['campaign_dialogue']['beats']))

    def test_failed_preflight_never_reveals_reconciliation(self):
        s=core.fresh('garrett');import charles_quest
        s['charles_quest']=dict(charles_quest.read(s),step=9);arrive(s,'glasshouse_lab');s['world']['minute']=20*60
        before=copy.deepcopy(s)
        with self.assertRaises(ValueError):dialogue.begin(s,'charles_quest.advance',(0,))
        self.assertEqual(before,s)

if __name__=='__main__':unittest.main()
