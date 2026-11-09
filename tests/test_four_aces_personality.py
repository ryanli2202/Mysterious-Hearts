"""Distinct Ace direction reaches real prompt builders without granting disclosure."""
import unittest
from unittest.mock import patch

import conversation_lore
import four_aces
import game_core as core
import groups
import hidden_cast
import messaging
import personality_types
import town


class AcePersonalityTests(unittest.TestCase):
    def test_all_voices_reach_solo_group_and_queued_prompts(self):
        state = core.fresh('ivan')
        town.travel(state, hidden_cast.HQ)
        for who in four_aces.IDS:
            state['world']['cast'][who].update(location=hidden_cast.HQ, journey=None)
        groups.open_group(state, list(four_aces.IDS))
        gid = state['active_group']
        for cue in ('How has your day been?', 'Our proposal failed.'):
            for channel in ('text', 'in_person'):
                state['groups'][gid]['channel'] = channel
                for who, direction in four_aces.CHARACTER_DIRECTION.items():
                    state['active'] = who
                    state['routes'][who]['channel'] = channel
                    self.assertIn(direction, str(core.build_messages(state, cue)))
                with patch.object(core, 'request', side_effect=RuntimeError('captured')) as request:
                    with self.assertRaisesRegex(RuntimeError, 'captured'):
                        groups.generate(state, gid, cue)
                for direction in four_aces.CHARACTER_DIRECTION.values():
                    self.assertIn(direction, str(request.call_args))
            for who, direction in four_aces.CHARACTER_DIRECTION.items():
                for is_group in (False, True):
                    job = dict(who=who, key=gid if is_group else who, group=is_group,
                               text=cue, ids=[], reason='reply')
                    with patch.object(core, 'request', side_effect=RuntimeError('captured')) as request:
                        with self.assertRaisesRegex(RuntimeError, 'captured'):
                            messaging.generate(state, job)
                    self.assertIn(direction, str(request.call_args))

    def test_voice_does_not_require_trust_or_disclose_identity(self):
        for who, direction in four_aces.CHARACTER_DIRECTION.items():
            for audience in (['rei'], ['ivan'], ['ivan', 'rei']):
                for level in range(4):
                    ref = conversation_lore.speaker_reference(who, audience, level, 'Hello')
                    self.assertEqual(ref['Individual personality and voice'], direction)
                    self.assertNotIn('Writer-only Ace identity', ref)
                    self.assertIn('Do not reveal or confirm', ref['Vendetta AU']['Ace disclosure boundary'])
            self.assertIn(direction, conversation_lore.character_tables()[who]['Familiar'])
        traits = [personality_types.PROFILES[who]['personality_traits'] for who in four_aces.IDS]
        self.assertEqual(len(set(traits)), 4)


if __name__ == '__main__':
    unittest.main()
