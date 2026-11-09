import unittest
from unittest.mock import patch
import hidden_cast
import personality_types as personality
import romantic_types as romance
import sexuality


class PersonalityTypesTests(unittest.TestCase):
    def test_complete_cast_profiles_and_preferences(self):
        self.assertEqual(set(personality.PROFILES), set(sexuality.CANON))
        self.assertEqual(set(personality.PREFERENCES), set(sexuality.CANON))
        for who in sexuality.CANON:
            for row in (personality.PROFILES[who], personality.PREFERENCES[who]):
                self.assertEqual(set(row), set(personality.FIELDS))
                for key in ('interests', 'personality_traits', 'lifestyle'):
                    self.assertGreaterEqual(len(row[key]), 2, (who, key))
            for hobby in hidden_cast.CAST.get(who, {}).get('hobbies', ()):
                self.assertIn(hobby, personality.PROFILES[who]['interests'])

    def test_protagonists_retain_secondary_interests(self):
        self.assertTrue({'science', 'medicine', 'video games', 'anime', 'taekwondo', 'food reviewing'} <= set(personality.PROFILES['minsu']['interests']))
        self.assertTrue({'drawing', 'poetry', 'cooking', 'martial arts'} <= set(personality.PROFILES['rei']['interests']))
        self.assertTrue({'singing', 'piano', 'repairs', 'martial arts'} <= set(personality.PROFILES['ivan']['interests']))
        self.assertTrue({'cooking', 'jeet kune do', 'sanda'} <= set(personality.PROFILES['garrett']['interests']))

    def test_partial_coverage_and_extra_hobbies(self):
        want = dict(interests=('sports', 'science', 'games', 'food'))
        actual = dict(interests=('taekwondo', 'anime'))
        self.assertEqual(personality.breakdown(want, actual)['interests'], .25)
        actual['interests'] += ('science', 'video games', 'food reviewing')
        self.assertEqual(personality.breakdown(want, actual)['interests'], 1)
        actual['interests'] += ('unrelated interest', 'taekwondo')
        self.assertEqual(personality.breakdown(want, actual)['interests'], 1)
        # A shared domain does not claim that running is literally taekwondo.
        self.assertEqual(personality.breakdown(dict(interests=('taekwondo',)), dict(interests=('running',)))['interests'], 0)

    def test_named_shared_hobbies_match_domains_case_insensitively(self):
        for who in ('neo', 'alyssa'):
            result = personality.breakdown(dict(interests=('cooking', 'games', 'crafts')), personality.PROFILES[who])
            self.assertEqual(result['interests'], 1)
        self.assertIn('art', personality.expand_interests(('botanical sketching',)))

    def test_four_dimensions_weights_and_probability_endpoints(self):
        want = {key: ('wanted',) for key in personality.FIELDS}
        other = {key: ('different',) for key in personality.FIELDS}
        self.assertEqual(personality.score(want, other), 0)
        for key, weight in personality.WEIGHTS.items():
            self.assertAlmostEqual(personality.score(want, dict(other, **{key: ('wanted',)})), weight)
        with patch.dict(romance.CANON, {'observer': want}), patch.dict(romance.TRAITS, {'match': want, 'miss': other}):
            self.assertAlmostEqual(romance.probability('observer', 'match', 'personality'), .85)
            self.assertAlmostEqual(romance.probability('observer', 'miss', 'personality'), .15)
            self.assertEqual(romance.affection_step('observer', 'match', 1, draw=.5), 1)
            self.assertEqual(romance.affection_step('observer', 'miss', 1, draw=.5), 0)
            self.assertEqual(romance.affection_step('observer', 'miss', 1, draw=.1), 1)
            self.assertEqual(romance.affection_step('observer', 'match', 1, draw=.9), 0)
            self.assertEqual(romance.affection_step('observer', 'match', -2, draw=.9), -2)

    def test_unknown_duplicate_and_directional_matching(self):
        self.assertAlmostEqual(personality.score({}, {}), .5)
        self.assertEqual(personality.breakdown(dict(interests=('science', 'science')), dict(interests=('science',)))['interests'], 1)
        self.assertEqual(personality.breakdown(dict(interests=('science',)), dict(interests=('science', 'games')))['interests'], 1)
        self.assertEqual(personality.breakdown(dict(interests=('science', 'games')), dict(interests=('science',)))['interests'], .5)
        self.assertEqual(personality.breakdown(dict(interests=('science',)), dict(interests=()))['interests'], .5)

    def test_dialogue_receives_expanded_private_preferences(self):
        text = romance.direction('minsu', ['sophie'])
        self.assertIn('personality_traits', text)
        self.assertIn('personality_fit', text)
        self.assertIn('do not grant knowledge', text)
        self.assertGreater(romance.match('sophie', 'minsu', 'personality'), 0)


if __name__ == '__main__':
    unittest.main()
