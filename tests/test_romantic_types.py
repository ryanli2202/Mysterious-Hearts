import unittest
from unittest.mock import patch
import romantic_types as types
import sexuality
import town
import game_core
import character_appearance
import social_world
import conversation_lore


class RomanticTypesTests(unittest.TestCase):
    def test_canon_covers_cast_and_all_dimensions(self):
        self.assertEqual(set(types.CANON), set(sexuality.CANON))
        for who in types.CANON:
            self.assertEqual(set(types.CANON[who]), set(types.PHYSICAL_FIELDS + types.PERSONALITY_FIELDS))
            for phase in ('physical', 'personality'):
                self.assertTrue(.15 <= types.probability(who, 'rei', phase) <= .85)

    def test_physical_and_personality_are_independent(self):
        with patch.dict(types.TRAITS, {'target': dict(types.TRAITS['rei'])}):
            before = types.match('emily', 'target', 'physical')
            types.TRAITS['target'].update({key: ('nonmatching',) for key in types.PERSONALITY_FIELDS})
            self.assertEqual(types.match('emily', 'target', 'physical'), before)
            self.assertEqual(types.match('emily', 'target', 'personality'), 0)
            self.assertEqual(types.affection_step('emily', 'target', 1, draw=.5), 0)
            self.assertEqual(types.affection_step('emily', 'target', 1, draw=.1), 1)
        self.assertEqual(types.affection_step('emily', 'rei', 1, draw=.5), 1)
        self.assertEqual(types.affection_step('emily', 'rei', 1, draw=.9), 0)
        self.assertEqual(types.affection_step('emily', 'rei', -2, draw=0), -2)

    def test_unknown_is_neutral(self):
        self.assertEqual(types.match('unknown', 'unknown', 'physical'), .5)

    def test_existing_history_and_orientation_are_preserved(self):
        s = game_core.fresh('rei')
        self.assertEqual(s['relationships']['emily']['attraction'], 58)
        s['relationships']['emily']['attraction'] = 71
        town.ensure(s)
        self.assertEqual(s['relationships']['emily']['attraction'], 71)
        self.assertFalse(town.romanceable(s, 'yuriko'))
        self.assertFalse(town.romanceable(s, 'garrett'))
        self.assertIn('Canonical romantic types', sexuality.direction('rei', ['emily']))

    def test_initial_attraction_is_directional_and_zero_stays_zero(self):
        self.assertEqual(types.initial_attraction('emily', 'rei', 20), 34)
        self.assertEqual(types.initial_attraction('emily', 'rei', 0), 0)
        self.assertLess(types.initial_attraction('emily', 'minsu', 20), 34)

    def test_each_detailed_dimension_changes_only_physical_fit(self):
        for field in character_appearance.DETAIL_FIELDS:
            with self.subTest(field=field), patch.dict(types.TRAITS, {'target': dict(types.TRAITS['rei'])}):
                types.TRAITS['target'][field] = types.CANON['emily'][field]
                before = types.match('emily', 'target', 'physical')
                personality = types.match('emily', 'target', 'personality')
                types.TRAITS['target'][field] = ('nonmatching-feature',)
                self.assertAlmostEqual(before - types.match('emily', 'target', 'physical'), 1 / 7)
                self.assertEqual(personality, types.match('emily', 'target', 'personality'))
                types.TRAITS['target'][field] = None
                self.assertAlmostEqual(before - types.match('emily', 'target', 'physical'), .5 / 7)

    def test_document_preserves_authored_appearances_and_supplies_dialogue(self):
        for who, guide in conversation_lore.character_tables().items():
            if guide.get('Appearance'):
                self.assertEqual(character_appearance.reference(who)['Recognisable features'], guide['Appearance'])
        s = game_core.fresh('rei')
        reference = social_world.appearance_reference(s, 'emily', ['rei'], '', texting=True)
        self.assertEqual(reference['People']['rei'], character_appearance.reference('rei'))
        self.assertIn('no live view', reference['Guidance'])
        self.assertNotIn('sylvanis', reference['People'])
        self.assertIsNone(character_appearance.traits('elliot')['eyes'])
        self.assertIsNone(character_appearance.traits('alyssa')['body_type'])
        self.assertEqual(character_appearance.traits('neo')['eyes'], ('grey-green',))

    def test_alternative_features_do_not_require_every_item(self):
        with patch.dict(types.TRAITS, {'target': dict(types.TRAITS['rei'])}):
            types.TRAITS['target']['hair'] = ('black',)
            full = types.match('emily', 'target', 'physical')
            types.TRAITS['target']['hair'] = types.CANON['emily']['hair']
            self.assertEqual(full, types.match('emily', 'target', 'physical'))


if __name__ == '__main__':
    unittest.main()
