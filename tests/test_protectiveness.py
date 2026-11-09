import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import game_core as core
import protectiveness
import social_world
import town


class ProtectivenessTests(unittest.TestCase):
    def test_all_targets_trigger_without_romantic_jealousy(self):
        for target, protector in protectiveness.PROTECTORS.items():
            with self.subTest(target=target):
                s = core.fresh('minsu')
                town.social_event(s, target, 'returned_flirt', [protector])
                self.assertEqual(s['emotions'][protector], 'guarded')
                self.assertEqual(protectiveness.context(s, protector)['witnessed'][0]['target'], target)
                self.assertFalse(s['relationships'].get(protector, {}).get('jealousy'))
                town.social_event(s, target, 'returned_flirt', [protector])
                self.assertEqual(len(s['protectiveness']), 1)

    def test_private_romance_and_friendly_events_do_not_trigger(self):
        s = core.fresh('garrett')
        town.social_event(s, 'emily', 'returned_flirt')
        town.betrayal(s, 'emily', 'romance')
        town.social_event(s, 'emily', 'none', ['rei'])
        self.assertNotIn('protectiveness', s)

    def test_physical_romance_is_witnessed_without_existing_partner(self):
        s = core.fresh('garrett')
        s['routes']['yuriko']['channel'] = 'in_person'
        with patch('town.present', side_effect=lambda state, who: who in ('yuriko', 'rei')):
            town.betrayal(s, 'yuriko', 'kiss')
        self.assertIn('rei:yuriko', s['protectiveness'])
        self.assertIn('protectiveness', social_world.knowledge_direction(s, ['rei']))
        self.assertEqual(protectiveness.context(s, 'garrett'), {})
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'story.json'
            core.save(s, path)
            self.assertEqual(core.load(path)['protectiveness'], s['protectiveness'])

    def test_protector_as_player_does_not_react_to_himself(self):
        s = core.fresh('rei')
        town.social_event(s, 'emily', 'returned_flirt', ['rei'])
        self.assertNotIn('protectiveness', s)

    def test_ivan_has_disapproval_and_others_have_distinct_ties(self):
        s = core.fresh('garrett')
        self.assertIn('openly disapproves', protectiveness.context(s, 'ivan')['guidance'][0])
        self.assertIn('younger sister', protectiveness.context(s, 'rei')['guidance'][0])
        self.assertIn('best friend Emily', protectiveness.context(s, 'rei')['guidance'][1])


if __name__ == '__main__':
    unittest.main()
