import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game_core as core
import conversation_lore
import flashback_lore as lore
import flashback_visits as visits
from test_flashback_visits import fresh,reply


class FlashbackLoreTests(unittest.TestCase):
    def test_every_historical_sheet_has_an_independent_voice(self):
        for era,people in (('school',('rei','emily','sophie','marcus','Joseph Richter')),
                           ('hong-kong-school',('garrett','charles')),('missing-charles',('garrett','april'))):
            for who in people:
                person=lore.profile(era,who)
                self.assertTrue(person['character_reference']['present_concerns'])
                self.assertTrue(person['character_reference']['private_boundaries'])
                self.assertTrue(person['dialogue_guide']['unknown_response'])
                self.assertGreaterEqual(len(person['dialogue_guide']['examples']),2)
        self.assertEqual(lore.profile('hong-kong-school','garrett')['age'],16)
        self.assertIsNone(lore.profile('missing-charles','garrett')['age'])
        self.assertNotEqual(lore.profile('hong-kong-school','garrett')['dialogue_guide'],lore.profile('missing-charles','garrett')['dialogue_guide'])

    def test_every_visit_uses_only_its_era_profiles(self):
        with patch.object(conversation_lore,'character_tables',side_effect=AssertionError('Adult sheets accessed')):
            for player in ('rei','emily','sophie','garrett'):
                s=fresh(player);visits.enter(s)
                system,context,_=visits.prompt(s,'What shall we do?','speak')
                for person in [context['player'],*context['companions']]:
                    self.assertEqual(person,lore.profile(visits.area_for(player),person['id']))
                self.assertIn('never merge present-day dialogue_styles.json',system.lower())
                self.assertIn('not amendments',system)

    def test_future_question_does_not_inject_adult_save_lore(self):
        s=fresh('garrett');visits.enter(s)
        s['charles_quest']={'evidence':[{'finding':'FUTURE CANARY: laboratory reunion'}]}
        s['routes']['charles']['history']=[{'role':'assistant','content':'FUTURE CANARY'}]
        s['friendships']['charles']['future_note']='FUTURE CANARY'
        system,context,_=visits.prompt(s,'Are you working at the laboratory now?','speak')
        self.assertNotIn('FUTURE CANARY',json.dumps(context))
        self.assertIn('do not agree, predict, elaborate',system.lower())
        self.assertEqual(context['companions'][0]['dialogue_guide'],lore.profile('hong-kong-school','charles')['dialogue_guide'])

    def test_old_context_stays_in_journal_but_not_prompt_or_resumed_exchange(self):
        s=fresh();visits.enter(s);visits.select(s,['marcus'])
        saved=visits.record(s)
        old=dict(members=['marcus'],kind='speak',text='Old conversation',response=reply('marcus'))
        old['response']['lines'][0]['text']='FUTURE CANARY from an older guide'
        saved['history']=[copy.deepcopy(old)]
        saved['exchange']['lines']=old['response']['lines'];saved.pop('reference_revision')
        before=copy.deepcopy(s['world']);visits.enter(s)
        self.assertEqual(saved['history'],[old])
        self.assertNotIn('FUTURE CANARY',json.dumps(saved['exchange']))
        self.assertEqual(visits.prompt(s,'Hello','speak')[1]['recent'],[])
        visits.commit(s,visits.stamp(s),'A new conversation','speak',reply('marcus'))
        recent=visits.prompt(s,'And then?','speak')[1]['recent']
        self.assertEqual(len(recent),1);self.assertEqual(recent[0]['text'],'A new conversation')
        self.assertEqual(s['world'],before)

    def test_guide_revision_change_excludes_previous_context_without_deleting_it(self):
        s=fresh();visits.enter(s);visits.select(s,['marcus'])
        visits.commit(s,visits.stamp(s),'Hello','speak',reply('marcus'))
        old=copy.deepcopy(visits.record(s)['history'])
        with patch.object(lore,'revision',return_value='new-guide-revision'):
            visits.enter(s)
            self.assertEqual(visits.prompt(s,'Hello again','speak')[1]['recent'],[])
        self.assertEqual(visits.record(s)['history'],old)

    def test_missing_sheet_fails_closed_without_adult_fallback(self):
        with tempfile.TemporaryDirectory() as folder:
            try:
                lore._load.cache_clear()
                with patch.object(lore,'REFERENCES',Path(folder)/'absent.json'):
                    with self.assertRaisesRegex(ValueError,'present-day lore will not be substituted'):
                        lore.profile('school','rei')
            finally:lore._load.cache_clear()
        with self.assertRaises(ValueError):lore.profile('school','charles')

    def test_profile_return_values_cannot_mutate_the_source(self):
        person=lore.profile('school','emily');person['dialogue_guide']['voice']='adult voice'
        self.assertIn('stutter',lore.profile('school','emily')['dialogue_guide']['voice'])


if __name__=='__main__':unittest.main()
