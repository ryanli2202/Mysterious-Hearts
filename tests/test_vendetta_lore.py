import copy
import json
import unittest
from unittest.mock import patch

import careers
import conversation_lore as lore
import game_core as core
import vendetta_lore as canon
import world_loop


class VendettaIntegrationTests(unittest.TestCase):
    def test_private_roster_does_not_become_public_directory(self):
        self.assertEqual(len(canon.PROFILES), 15)
        self.assertIn('Shinigami Protocol', canon.speaker_context('thirteen', ['rei'])['Own ability (private self-knowledge)'])
        self.assertNotIn('Shinigami Protocol', str(canon.speaker_context('rei', ['thirteen'])))
        public = lore.speaker_reference('emily', ['rei'], 0, 'Awakening')
        self.assertIn('Awakened', str(public['Vendetta AU']))
        self.assertNotIn('not awakened', str(public['Vendetta AU']))
        self.assertNotIn('Deathwind', str(public['Vendetta AU']))
        self.assertNotIn('Queen of Wind', str(lore.topic_reference('emily', 'Awakened')))
        self.assertIn('United Nations', str(public['Vendetta AU']))
        self.assertIn('Blisk', canon.PROFILES['alyssa'][0])
        self.assertIn('Blisk', canon.PROFILES['sylvanis'][0])

    def test_generalship_is_shared_only_between_siblings(self):
        private = canon.speaker_context('valentina', ['ivan'])
        self.assertIn('Shared command history', private)
        mixed = canon.speaker_context('valentina', ['ivan', 'rei'])
        self.assertNotIn('Shared command history', mixed)
        self.assertIn('Keep these facts from outsiders', mixed['Private command knowledge'])
        self.assertNotIn('no automatic knowledge of his rank', str(lore.character_tables()['valentina']))

    def test_actual_dialogue_prompt_uses_new_world_rules(self):
        s = core.fresh('rei'); s['active'] = 'emily'
        prompt = core.build_messages(s, 'What does Awakening mean?')[0]['content']
        self.assertIn('unified United Nations', prompt)
        self.assertIn('Critical Hit', prompt)
        self.assertNotIn('There are no Awakened', prompt)

    def test_crime_decisions_survive_save_without_leaking_or_repaying(self):
        for key, spec in careers.TRACKS.items():
            if key not in careers.CRIME_SITUATIONS: continue
            s = core.fresh(spec['player'])
            s['world']['minute'] = spec['hours'][0]*60
            s['world']['location'] = spec['venue']
            s['world']['cast'][s['player']].update(location=spec['venue'], journey=None)
            careers.begin(s, key); careers.choose(s, 0)
            s = json.loads(json.dumps(s))
            def advance(state, minutes):
                state['world']['minute'] += minutes
            with patch.object(world_loop, 'advance', advance):
                careers.choose(s, 2)
            entry = careers.ensure(s)['history'][-1]
            self.assertEqual(len(entry['decisions']), 2)
            self.assertIn('effects', entry)
            self.assertEqual(careers.context(s, [spec['player'], 'emily']), [])
            before = copy.deepcopy(s)
            with self.assertRaises(ValueError): careers.choose(s, 0)
            self.assertEqual(before, s)

    def test_pending_legacy_work_keeps_its_original_scenario(self):
        active = dict(track='joker', scenario=1, choices=[0])
        self.assertEqual(careers.current_situation(active), careers.TRACKS['joker']['situations'][2])


if __name__ == '__main__': unittest.main()
