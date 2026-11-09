import unittest

import game_core as core
import contact_profiles as profiles
import conversation_lore as lore


class StartingFavouritesTests(unittest.TestCase):
    def test_reference_row_is_parsed_without_inventing_tastes(self):
        emily = lore.everyday_favourites('emily')
        self.assertEqual(emily['Dinner'], 'Mushroom risotto')
        self.assertEqual(emily['Movie'], 'Kiki’s Delivery Service')
        self.assertEqual(emily['Author'], 'Frances Hodgson Burnett')
        self.assertEqual(lore.everyday_favourites('april')['Author'], 'Ursula K. Le Guin')
        self.assertNotIn('Music', emily)
        self.assertEqual(lore.everyday_favourites('unknown'), {})

    def test_close_contacts_know_favourites_on_first_open(self):
        for player, subject in [('rei', 'emily'), ('rei', 'sophie'), ('garrett', 'april'),
                                ('garrett', 'rei'), ('minsu', 'amy'), ('minsu', 'sophie'),
                                ('rei', 'yuriko'), ('ivan', 'valentina')]:
            with self.subTest(player=player, subject=subject):
                s = core.fresh(player)
                facts = profiles.view(s, subject, player)['favourites']
                self.assertEqual(facts['Movie']['value'], lore.everyday_favourites(subject)['Movie'])
                self.assertEqual(facts['Movie']['provenance'], 'Known from your shared history')
                self.assertNotIn('Movie', profiles.public(s, subject, player))

    def test_knowledge_is_reciprocal_and_applies_to_npcs(self):
        s = core.fresh('garrett')
        for observer, subject in [('emily', 'rei'), ('sophie', 'emily'), ('emily', 'sophie')]:
            facts = profiles.context(s, observer)[subject]['Favourites already known before the story']
            self.assertEqual(facts, lore.everyday_favourites(subject))
        self.assertNotIn('Favourites already known before the story', profiles.context(s, 'amy')['emily'])

    def test_existing_save_and_later_hurt_do_not_erase_knowledge(self):
        s = core.fresh('rei')
        s.pop('contact_profiles')
        s['relationships']['emily'].update(trust=0, closeness=0)
        self.assertEqual(profiles.view(s, 'emily', 'rei')['favourites']['Drink']['value'], 'Honey chamomile tea')

    def test_new_closeness_does_not_invent_a_disclosure(self):
        s = core.fresh('minsu')
        s['relationships']['emily'].update(trust=100, closeness=100)
        self.assertEqual(profiles.view(s, 'emily', 'minsu')['favourites'], {})
        s['profile_notes'] = {'emily': [dict(source='emily', quote='My favorite movie is Arrival.', minute=500)]}
        self.assertEqual(profiles.view(s, 'emily', 'minsu')['favourites']['Movie']['value'], 'Arrival')

    def test_self_and_custom_fields_take_precedence_without_publicizing_canon(self):
        s = core.fresh('rei')
        self.assertEqual(profiles.view(s, 'rei', 'rei')['favourites']['Movie']['value'], 'In the Mood for Love')
        profiles.edit(s, 'rei', 'Movies', 'Arrival', 'private')
        self.assertEqual(profiles.view(s, 'rei', 'rei')['public']['Movies'], 'Arrival')
        self.assertNotIn('Movies', profiles.context(s, 'garrett')['rei'])

    def test_every_protagonist_knows_own_private_reference_without_discovery(self):
        for player in ('rei', 'garrett', 'minsu', 'ivan'):
            with self.subTest(player=player):
                s = core.fresh(player)
                own = profiles.view(s, player, player)
                self.assertEqual(own['self_reference']['Your private history'], lore.character_tables()[player]['Confidence'])
                self.assertEqual(profiles.field_value(own, 'Movies', own=True), lore.everyday_favourites(player)['Movie'])
                self.assertNotIn('Not shared', profiles.field_value(own, 'Music', own=True))
                other = 'emily' if player != 'ivan' else 'valentina'
                self.assertEqual(profiles.view(s, player, other)['self_reference'], {})
                self.assertNotIn('Your private history', profiles.context(s, other)[player])

    def test_own_edits_even_empty_override_reference_defaults(self):
        s = core.fresh('rei')
        profiles.edit(s, 'rei', 'Movies', '', 'private')
        self.assertEqual(profiles.field_value(profiles.view(s, 'rei', 'rei'), 'Movies', own=True), '')


if __name__ == '__main__': unittest.main()
