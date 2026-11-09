import copy
import json
import unittest

import game_core as core
import contact_profiles as profiles
import memory_store as memory
import personal_details
import social_world as social


class LearnedContactTests(unittest.TestCase):
    def setUp(self):
        self.s = core.fresh('rei')

    def say(self, text, speaker='emily', owners=('emily', 'rei'), minute=500):
        memory.utterance(self.s, f'test:{minute}:{speaker}', text, speaker, owners, minute)

    def test_multiple_favourites_and_personal_fields_update(self):
        self.say('My favourite food is ramen and my favourite drink is green tea. My favourite book is Dune. I grew up in Brisbane. I enjoy drawing. I am allergic to peanuts.')
        view = profiles.view(self.s, 'emily', 'rei')
        self.assertEqual(view['favourites']['Food']['value'], 'ramen')
        self.assertEqual(view['favourites']['Drink']['value'], 'green tea')
        self.assertEqual(view['favourites']['Book']['value'], 'Dune')
        self.assertEqual(view['details']['Hometown']['value'], 'Brisbane')
        self.assertEqual(view['details']['Allergies']['value'], 'peanuts')
        self.assertEqual(profiles.field_value(view, 'Hobbies'), 'drawing')

    def test_correction_is_observer_specific_and_survives_reload(self):
        self.say('My favourite movie is Arrival.', owners=['emily', 'rei', 'sophie'])
        self.say('Actually, my favourite film is Spirited Away.', minute=600)
        self.s = json.loads(json.dumps(self.s))
        self.assertEqual(profiles.known_favourites(self.s, 'emily', 'rei')['Movie']['value'], 'Spirited Away')
        self.assertEqual(profiles.known_favourites(self.s, 'emily', 'sophie')['Movie']['value'], 'Arrival')
        self.assertEqual(profiles.known_favourites(self.s, 'emily', 'amy'), {})
        self.assertEqual(profiles.known_favourites(self.s, 'emily', 'emily')['Movie']['value'], 'Spirited Away')

    def test_questions_hypotheticals_hedges_quotes_are_not_facts(self):
        for text in ['My favourite food is ramen?', 'If my favourite food is ramen, what would you choose?',
                     'Maybe my favourite food is ramen.', 'She said my favourite food is ramen.',
                     'I think my favourite movie is Arrival.', 'Hello. My favourite food is ramen?']:
            with self.subTest(text=text): self.assertEqual(personal_details.extract(text), {})

    def test_removing_a_favourite_does_not_restore_canon(self):
        self.say("I don't have a favourite movie anymore.")
        self.assertEqual(profiles.known_favourites(self.s, 'emily', 'rei')['Movie']['value'], 'No favourite')

    def test_exact_personal_disclosure_reaches_all_listeners_only(self):
        quote = 'My grandmother taught me to mend teddy bears.'
        data = {'profile_notes': [dict(source='emily', subject='emily', quote=quote)]}
        social.record_notes(self.s, data, {'emily':quote}, owners=['rei', 'emily', 'sophie'])
        memory.sync(self.s)
        self.assertTrue(any(quote in r['text'] for r in profiles.view(self.s, 'emily', 'sophie')['discoveries']))
        self.assertFalse(any(quote in r['text'] for r in profiles.view(self.s, 'emily', 'amy')['discoveries']))
        context = social.conversation_knowledge(self.s, 'sophie', ['emily'])
        self.assertIn(quote, json.dumps(context))

    def test_same_fact_can_be_disclosed_later_to_another_listener(self):
        quote = 'My aunt taught me to knit.'
        data = {'profile_notes': [dict(source='emily', subject='emily', quote=quote)]}
        for listeners in (['rei','emily'], ['rei','emily','amy']):
            social.record_notes(self.s, data, {'emily':quote}, owners=listeners)
            memory.sync(self.s)
        self.assertTrue(any(quote in r['text'] for r in profiles.view(self.s, 'emily', 'amy')['discoveries']))

    def test_unspoken_model_note_is_rejected(self):
        social.record_notes(self.s, {'profile_notes': [dict(source='emily', subject='emily', quote='My favourite movie is Arrival.')]}, {'emily':'Hello.'})
        self.assertEqual(self.s.get('profile_notes', {}), {})

    def test_npc_only_exchange_does_not_reach_player(self):
        self.say('My favourite author is Jane Austen.', owners=['emily', 'amy'])
        self.assertEqual(profiles.known_favourites(self.s, 'emily', 'amy')['Author']['value'], 'Jane Austen')
        self.assertEqual(profiles.known_favourites(self.s, 'emily', 'rei')['Author']['value'], 'Frances Hodgson Burnett')

    def test_other_persons_claim_is_attributed_not_promoted(self):
        quote = 'Emily told me her favourite movie is Arrival.'
        social.record_notes(self.s, {'profile_notes':[dict(source='amy', subject='emily', quote=quote)]}, {'amy':quote})
        memory.sync(self.s)
        view = profiles.view(self.s, 'emily', 'rei')
        self.assertEqual(view['favourites']['Movie']['value'], 'Kiki’s Delivery Service')
        self.assertTrue(any(r['kind'] == 'belief' for r in view['discoveries']))

    def test_old_transcripts_gain_details_without_reindexing_or_mutation(self):
        memory.add(self.s, source='legacy-delivered', text='emily: I grew up in Brisbane.', owners=['rei','emily'],
                   subjects=['emily'], certainty='quoted speech', minute=500)
        before = copy.deepcopy(self.s)
        self.assertEqual(profiles.learned_details(self.s, 'emily', 'rei')['Hometown']['value'], 'Brisbane')
        self.assertEqual(before, self.s)

    def test_new_hobby_preserves_previous_hobbies(self):
        self.say('I enjoy drawing.')
        self.say('I enjoy cooking.', minute=600)
        self.assertEqual(profiles.learned_details(self.s, 'emily', 'rei')['Hobbies']['values'], ['drawing', 'cooking'])

    def test_async_reply_updates_contact_and_stores_broader_personal_note(self):
        import messaging
        line = 'My favourite drink is matcha. My aunt taught me to mend teddy bears.'
        result = dict(bubbles=[line], pause_minutes=0, moment='none', profile_notes=[
            dict(source='emily', subject='emily', quote='My aunt taught me to mend teddy bears.')])
        job = dict(who='emily', key='emily', group=False, ids=[], reason=None)
        self.assertTrue(messaging.apply(self.s, job, result))
        view = profiles.view(self.s, 'emily', 'rei')
        self.assertEqual(view['favourites']['Drink']['value'], 'matcha')
        self.assertTrue(any('teddy bears' in r['text'] for r in view['discoveries']))
        self.assertEqual(profiles.known_favourites(self.s, 'emily', 'amy'), {})


if __name__ == '__main__': unittest.main()
