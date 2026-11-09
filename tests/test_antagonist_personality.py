"""Personality direction survives non-combat topics and each conversation route."""
import unittest
from unittest.mock import patch
import game_core as core
import groups
import hidden_cast
import messaging
import town


class AntagonistPersonalityTests(unittest.TestCase):
    def test_baseline_reaches_every_conversation_route_without_combat_cue(self):
        markers = {'sylvanis': 'Sylvanis remains erratic and violence-driven',
                   'crow': 'ambition and hunger for power in every conversation'}
        for cue in ('How has your day been?', 'The report is ready.', 'Our proposal failed.'):
            s = core.fresh('ivan')
            town.travel(s, hidden_cast.HQ)
            s['world']['cast']['sylvanis'].update(location=hidden_cast.HQ, journey=None)
            groups.open_group(s, ['crow', 'sylvanis'])
            gid = s['active_group']
            for channel in ('text', 'in_person'):
                s['groups'][gid]['channel'] = channel
                for who, marker in markers.items():
                    with self.subTest(cue=cue, channel=channel, who=who, route='solo'):
                        s['active'] = who
                        s['routes'][who]['channel'] = channel
                        self.assertIn(marker, core.build_messages(s, cue)[0]['content'])
                s['groups'][gid]['channel'] = channel
                with patch.object(core, 'request', side_effect=RuntimeError('captured')) as request:
                    with self.assertRaisesRegex(RuntimeError, 'captured'):
                        groups.generate(s, gid, cue)
                system = request.call_args.args[1]['messages'][0]['content']
                for marker in markers.values():
                    self.assertIn(marker, system)
            for is_group in (False, True):
                for who, marker in markers.items():
                    with self.subTest(cue=cue, who=who, route='queued', group=is_group):
                        job = dict(who=who, key=gid if is_group else who, group=is_group,
                                   text=cue, ids=[], reason='reply')
                        with patch.object(core, 'request', side_effect=RuntimeError('captured')) as request:
                            with self.assertRaisesRegex(RuntimeError, 'captured'):
                                messaging.generate(s, job)
                        self.assertIn(marker, request.call_args.args[1]['messages'][0]['content'])
