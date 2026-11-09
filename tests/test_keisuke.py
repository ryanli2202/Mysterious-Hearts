import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import game_core as core
import job_apps as jobs
import keisuke
import town
import groups
import crime_operations
import phone_numbers
import character_types
import town_npc_system
import hidden_cast


def join(s):
    d=jobs.ensure(s)
    d.update(reputation=55,completed=10,gang=dict(name='Test crew',role='Founder',standing=3))
    d['connections']['Shinokami']=3
    jobs.sponsor(s,'Shinokami')


class KeisukeTests(unittest.TestCase):
    def test_immediate_join_and_first_contact(self):
        for player in ('rei','garrett','minsu'):
            s=core.fresh(player)
            self.assertNotIn(keisuke.NAME,phone_numbers.ensure(s)['contacts'])
            with self.assertRaises(ValueError): phone_numbers.add(s,phone_numbers.NUMBERS[keisuke.NAME])
            join(s)
            self.assertEqual(jobs.ensure(s)['membership']['rank'],0)
            self.assertEqual(jobs.ensure(s)['membership']['contact'],keisuke.NAME)
            self.assertTrue(phone_numbers.saved_number(s,keisuke.NAME))
            self.assertFalse(hidden_cast.contact(s,'takeo'))
            thread=s['groups']['npc:'+keisuke.NAME]
            self.assertEqual(thread['history'][0]['text'],keisuke.INTRO)
            self.assertEqual(thread['unread'],1)
            before=copy.deepcopy(thread)
            for _ in range(3): jobs.ensure(s);phone_numbers.ensure(s);town.ensure(s)
            self.assertEqual(thread,before)
            s['job_apps']['membership']['strikes']=2
            self.assertTrue(phone_numbers.saved_number(s,keisuke.NAME))
            with self.assertRaises(ValueError):jobs.faction_assignment(s)

    def test_depot_presence_and_assignment(self):
        s=core.fresh('rei');join(s)
        town.end_hangouts(s);town.travel(s,'site_02')
        crime_operations.enter(s,'site_02','reception')
        for minute in (0,600,1439,8*1440):
            s['world']['minute']=minute
            self.assertEqual(town.npc_details(s,keisuke.NAME),keisuke.PROFILE)
        groups.open_local(s,keisuke.NAME)
        self.assertEqual(s['groups'][s['active_group']]['members'],[keisuke.NAME])
        town.end_hangouts(s)
        jobs.faction_assignment(s)
        self.assertEqual(jobs.ensure(s)['pending']['liaison'],keisuke.NAME)
        self.assertEqual(jobs.ensure(s)['pending']['venue'],keisuke.HIDEOUT)
        town.travel(s,'site_01')
        self.assertNotIn(keisuke.NAME,town.ensure(s)['npcs'])
        self.assertNotIn(keisuke.NAME,s['world']['cast'])

    def test_existing_save_introduction_and_history(self):
        s=core.fresh('rei');join(s)
        s['npc_chats'][keisuke.NAME]['history'].append(dict(speaker='rei',text='Existing report.'))
        s['npc_chats'][keisuke.NAME].pop('shinokami_introduced')
        s['npc_chats'][keisuke.NAME]['history'].pop(0)
        s['groups'].pop('npc:'+keisuke.NAME)
        s['phone_numbers']['contacts'].pop(keisuke.NAME)
        with tempfile.TemporaryDirectory(dir=core.ROOT/'.test-tmp') as folder:
            path=Path(folder)/'save.json';core.save(s,path);loaded=core.load(path)
        self.assertEqual(loaded['npc_chats'][keisuke.NAME]['history'][0]['text'],'Existing report.')
        self.assertEqual(sum(r.get('text')==keisuke.INTRO for r in loaded['npc_chats'][keisuke.NAME]['history']),1)
        self.assertTrue(phone_numbers.saved_number(loaded,keisuke.NAME))

    def test_town_voice_context_and_assets(self):
        s=core.fresh('rei');join(s)
        self.assertEqual(character_types.kind(keisuke.NAME),character_types.TOWN)
        self.assertFalse(town.romanceable(s,keisuke.NAME))
        self.assertNotIn(keisuke.NAME,s['routes'])
        result=dict(narration='A short message arrives.',lines=[dict(speaker=keisuke.NAME,text='Tell me what happened.')],emotions={'rei':'content',keisuke.NAME:'content'})
        with patch.object(core,'request',return_value={'message':{'content':json.dumps(result)}}) as request:
            town_npc_system.generate(s,[keisuke.NAME],{'player_reply':'What happens next?'},texting=True)
        payload=json.loads(request.call_args.args[1]['messages'][1]['content'])
        person=payload['residents'][keisuke.NAME]
        self.assertIn(keisuke.VOICE,person['background'])
        self.assertEqual(person['Shinokami liaison context']['rank'],0)
        with Image.open(core.ROOT/'assets/portraits/keisuke-hachimura-selection.png') as image:
            self.assertEqual(image.mode,'RGBA');self.assertEqual(image.getchannel('A').getextrema(),(0,255))
        with Image.open(core.ROOT/'assets/profiles/Keisuke Hachimura.png') as image:
            self.assertEqual(image.width,image.height)

    def test_story_portrayal_in_text_and_spoken_generation(self):
        s=core.fresh('rei');join(s)
        # An old cordial answer is retained as history, not authoritative character guidance.
        s['npc_chats'][keisuke.NAME]['history'].append(dict(speaker=keisuke.NAME,text='I used to do depot errands.'))
        before=copy.deepcopy(s)
        result=dict(narration='Keisuke replies.',lines=[dict(speaker=keisuke.NAME,text='That does not excuse it.')],
                    emotions={'rei':'content',keisuke.NAME:'guarded'})
        for texting in (True,False):
            with patch.object(core,'request',return_value={'message':{'content':json.dumps(result)}}) as request:
                town_npc_system.generate(s,[keisuke.NAME],{'player_reply':'Why should I follow you?',
                    'recent_exchange':s['npc_chats'][keisuke.NAME]['history']},texting=texting)
            payload=json.loads(request.call_args.args[1]['messages'][1]['content'])
            reference=payload['residents'][keisuke.NAME]['background']
            for fact in ('police officer', 'killed his leader', 'Number Thirteen', 'successor organisation',
                         'submission to greater strength', 'not completed Mysterious Hearts history'):
                self.assertIn(fact,reference)
            self.assertIn(keisuke.SOURCE_BOUNDARY,reference)
            self.assertIn('private',reference)
        self.assertEqual(s,before)  # Source beats and model generation must not execute story events.

    def test_existing_intro_is_preserved_when_portrayal_changes(self):
        s=core.fresh('rei');join(s)
        old='Hachimura. Your sponsorship is confirmed. Keep your reports clear.'
        for history in (s['npc_chats'][keisuke.NAME]['history'],s['groups']['npc:'+keisuke.NAME]['history']):
            history[0]['text']=old
        before=copy.deepcopy(s['groups']['npc:'+keisuke.NAME])
        keisuke.ensure(s);town.ensure(s)
        self.assertEqual(s['groups']['npc:'+keisuke.NAME],before)
        self.assertEqual(s['npc_chats'][keisuke.NAME]['history'][0]['text'],old)


if __name__=='__main__':unittest.main()
