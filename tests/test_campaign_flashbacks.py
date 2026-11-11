import copy
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import game_core as core
import campaign_dialogue as dialogue
import campaign_flashbacks as memories
import rei_story
import charles_quest
import combat
import simulation_clock
from test_major_campaigns import arrive
from flashback_helpers import finish_memories, finish_scene


class FlashbackTests(unittest.TestCase):
    def test_rei_gate_and_exactly_three_ordered_memories(self):
        s=core.fresh('rei')
        for venue in ('rei_home','archive'):
            arrive(s,venue);rei_story.advance(s)
        arrive(s,'rei_home')
        with self.assertRaisesRegex(ValueError,'mandatory flashback'):rei_story.advance(s)
        with self.assertRaises(ValueError):memories.start(s,'rei-school-suspension')
        finish_memories(s)
        self.assertEqual(s['campaign_flashbacks']['completed'],list(memories.SCENES)[:3])
        self.assertEqual(rei_story.data(s)['stage'],2)
        rei_story.advance(s)
        self.assertEqual(rei_story.data(s)['stage'],3)

    def test_garrett_gate_resume_and_world_isolation(self):
        s=core.fresh('garrett');arrive(s,'noodle_shop')
        with self.assertRaisesRegex(ValueError,'mandatory flashback'):charles_quest.advance(s,0)
        key=memories.pending(s);before=copy.deepcopy(s['world'])
        memories.start(s,key)
        with self.assertRaises(ValueError):memories.finish(s,key)
        dialogue.next_line(s)
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'flashback.json';core.save(s,path);s=core.load(path)
        self.assertEqual(s['campaign_dialogue']['cursor'],1)
        self.assertTrue(memories.portrait_path(s,'garrett').name.endswith('home.png'))
        clock=simulation_clock.SimulationClock();clock.reset(s,0)
        self.assertEqual(clock.tick(s,now=300),0)
        with self.assertRaises(ValueError):core.town.travel(s,'square')
        with self.assertRaises(ValueError):combat.guard(s)
        finish_scene(s)
        self.assertEqual(before,s['world'])
        self.assertIsNone(memories.portrait_path(s,'garrett'))
        self.assertIsNone(memories.pending(s))
        finish_memories(s);charles_quest.advance(s,0)
        self.assertEqual(charles_quest.read(s)['step'],1)
        s['charles_quest']['step']=9
        self.assertEqual(memories.pending(s),'garrett-school-brother')
        self.assertEqual(memories.venue(s,memories.pending(s)),'glasshouse_lab')

    def test_legacy_catchup_preserves_progress_and_contacts(self):
        s=core.fresh('garrett');s['charles_quest']=dict(charles_quest.read(s),step=11,ending='quiet alliance')
        before=copy.deepcopy(s['charles_quest']);friends=copy.deepcopy(s['friendships'])
        finish_memories(s)
        self.assertEqual(before,s['charles_quest']);self.assertEqual(friends,s['friendships'])
        s=core.fresh('rei');rei_story.data(s).update(stage=6,complete=True,richter=True,hamayashi='leave')
        before=copy.deepcopy(s['rei_story']);finish_memories(s)
        self.assertEqual(before,s['rei_story'])

    def test_location_party_and_wrong_player_rejected(self):
        s=core.fresh('garrett');key=memories.pending(s)
        arrive(s,'square')
        with self.assertRaises(ValueError):memories.start(s,key)
        arrive(s,'noodle_shop');s['world']['party']=['april']
        with self.assertRaises(ValueError):memories.start(s,key)
        with self.assertRaises(ValueError):memories.start(core.fresh('rei'),key)

    def test_old_inflight_conversation_finishes_before_catchup(self):
        s=core.fresh('rei');arrive(s,'rei_home');rei_story.data(s)['stage']=2
        s['campaign_dialogue']=dict(action='rei_story.advance',args=[0],beats=[dialogue.beat(narration='Saved old scene')],cursor=0,venue='rei_home',player='rei')
        dialogue.next_line(s)
        self.assertEqual(rei_story.data(s)['stage'],3)
        self.assertNotIn('_finishing_legacy_campaign_dialogue',s)
        self.assertIsNone(memories.pending(s))

    def test_artwork_and_authored_story_contract(self):
        root=core.ROOT/'assets'
        for key,scene in memories.SCENES.items():
            self.assertTrue((root/'ui'/(scene['background']+'.png')).is_file(),key)
            for stem in scene['portraits'].values():
                with Image.open(root/'portraits'/(stem+'.png')) as im:
                    self.assertEqual(im.mode,'RGBA',stem)
                    low,high=im.getchannel('A').getextrema()
                    self.assertEqual(low,0,stem);self.assertGreaterEqual(high,250,stem)
        text=str(memories.SCENES)
        for phrase in ('died by suicide','suspended','punches him','sixteen','Red Dragons','Mum and Dad died','april'):
            self.assertIn(phrase,text)


if __name__=='__main__':unittest.main()
