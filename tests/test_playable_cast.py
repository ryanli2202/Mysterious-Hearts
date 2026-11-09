"""Playable-roster integration and original-start regression checks."""
import json
from pathlib import Path
import tempfile
import unittest

import game_core as core
import playable_cast as cast
import careers
import phone_apps
import phone_personalization
import town


class PlayableCastTests(unittest.TestCase):
    def test_roster_and_exclusions(self):
        import character_types
        self.assertEqual(set(core.PLAYERS), character_types.MAJOR_CHARACTERS - cast.EXCLUDED)
        self.assertEqual(len(core.PLAYERS), 28)
        for who in cast.EXCLUDED:
            with self.assertRaises(ValueError): core.fresh(who)

    def test_original_starts_unchanged(self):
        baseline = json.loads((Path(__file__).parent / 'fixtures/original_protagonist_starts.json').read_text(encoding='utf-8'))
        for who, expected in baseline.items():
            with self.subTest(player=who):
                state = json.loads(json.dumps(core.fresh(who)))
                actual = {k: state[k] for k in expected if k != 'world'}
                actual['world'] = {k: state['world'][k] for k in expected['world']}
                # New residents are additive strangers; the original fixture remains authoritative for existing ties.
                for new_who in ('fox','gordon'):
                    self.assertEqual(actual['friendships'][new_who]['status'],'strangers')
                    self.assertFalse(actual['discoveries'][new_who]['met'])
                    actual['friendships'].pop(new_who)
                    actual['discoveries'].pop(new_who)
                self.assertEqual(actual, expected)

    def test_every_new_protagonist_can_live_work_and_reload(self):
        with tempfile.TemporaryDirectory(dir=core.ROOT / '.test-tmp') as folder:
            for who in cast.STARTS:
                with self.subTest(player=who):
                    s = core.fresh(who)
                    self.assertNotEqual(s['active'], who)
                    self.assertNotIn(who, phone_apps.contacts(s))
                    self.assertTrue(core.hidden.visible_place(s, town.HOMES[who]))
                    phone_personalization.ensure(s)
                    town.home_action(s, town.HOME_ACTIONS[who][0])
                    key, = careers.available(s)
                    spec = careers.TRACKS[key]
                    town.travel(s, spec['venue']); town.finish_drive(s)
                    # Place this session inside its hours without waiting overnight.
                    s['world']['minute'] = max(10, spec['hours'][0])*60
                    s['autonomy']['people'][who]['sleep_until'] = None
                    careers.start_project(s, key)
                    before = s['world']['money']
                    careers.begin(s, key)
                    careers.choose(s, 0); careers.choose(s, 2)
                    self.assertEqual(s['world']['money'], before + spec['pay'])
                    self.assertEqual(careers.get(s, key)['completed'], 0)
                    self.assertEqual(len(careers.get(s, key)['project']['days']), 1)
                    with self.assertRaises(ValueError): careers.begin(s, key)
                    location = s['world']['location']
                    town.loop.advance(s, 30)
                    self.assertEqual(s['world']['location'], location)
                    self.assertEqual(s['world']['cast'][who]['location'], location)
                    path = Path(folder) / (who + '.json')
                    core.save(s, path); loaded = core.load(path)
                    self.assertEqual(loaded['player'], who)
                    self.assertEqual(loaded['world']['money'], s['world']['money'])
                    self.assertEqual(loaded['careers'], s['careers'])
                    self.assertEqual(loaded['relationships'], s['relationships'])
                    town.travel(loaded, 'home'); town.finish_drive(loaded)
                    self.assertEqual(loaded['world']['location'], town.HOMES[who])

    def test_family_partner_and_private_access(self):
        for who, sibling in (('yuriko', 'rei'), ('valentina', 'ivan')):
            s = core.fresh(who)
            self.assertFalse(town.romanceable(s, sibling))
            self.assertEqual(town.character_stats(s, sibling)['status'], 'close siblings')
        for who, partner in (('neo', 'alyssa'), ('alyssa', 'neo')):
            s = core.fresh(who)
            self.assertEqual(s['relationships'][partner]['status'], 'official')
            self.assertTrue(town.romanceable(s, partner))
            self.assertFalse(town.romanceable(s, 'sophie'))
        for who in cast.STARTS:
            s = core.fresh(who)
            self.assertEqual(core.hidden.hq_access(s, who), who in core.hidden.SYNDICATE_MEMBERS)
        s = core.fresh('sylvanis')
        self.assertFalse(any(town.romanceable(s, target) for target in core.CONTACTS))
        self.assertEqual(town.character_stats(s, 'ivan')['status'], 'hostile coworkers')

    def test_advanced_projects_and_cross_character_isolation(self):
        for who in cast.STARTS:
            s = core.fresh(who); key, = careers.available(s)
            d = careers.get(s, key); d.update(completed=1, reputation=80)
            careers.start_project(s, key)
            self.assertTrue(d['project']['title'].startswith('Advanced '))
            with self.assertRaises(ValueError): careers.begin(s, 'restaurant')
        self.assertEqual(careers.available(core.fresh('garrett')), ['restaurant', 'dragons'])

    def test_dialogue_uses_selected_identity_and_canonical_partner(self):
        import hidden_cast
        import json
        from unittest.mock import patch
        for who in cast.STARTS:
            with self.subTest(player=who):
                s = core.fresh(who)
                other = s['canonical_partner'] if 'canonical_partner' in s else ('rei' if who != 'yuriko' else 'emily')
                hidden_cast.mark_met(s, other)
                s['active'] = other
                prompt = core.build_messages(s, 'Hello.')[0]['content']
                self.assertIn('selected protagonist is ' + who, prompt)
                if who in ('neo', 'alyssa'): self.assertIn('established committed partners', prompt)
                replies = dict(choices_speaker=core.PLAYERS[who], choices=['How was today?', 'Tell me more.', 'Let’s take our time.', 'I’m listening.'])
                replies['personal_choices'] = core.personal_choices(s, {})
                with patch.object(core, 'request', return_value={'message': {'content': json.dumps(replies)}}) as request:
                    scene = dict(dialogue='Hello.', narration='A notification.', memory='', choices=[],
                                 speaker=core.CONTACTS[other][0], addressee=core.PLAYERS[who])
                    core.generate_player_choices(s, 'Hello.', scene)
                    voice = request.call_args.args[1]['messages'][0]['content']
                    self.assertNotIn('a male protagonist', voice)
                    self.assertIn('selected protagonist is ' + who, voice)

    def test_project_cycle_and_rewards(self):
        for who in ('amy', 'camila', 'sylvanis'):
            with self.subTest(player=who):
                s = core.fresh(who); key, = careers.available(s)
                spec = careers.TRACKS[key]
                town.travel(s, spec['venue']); town.finish_drive(s)
                careers.start_project(s, key)
                funds = s['world']['money']
                for day in range(3):
                    s['world']['minute'] = day*1440 + 10*60
                    s['autonomy']['people'][who]['sleep_until'] = None
                    careers.begin(s, key); careers.choose(s, 0); careers.choose(s, 0)
                self.assertEqual(s['world']['money'], funds + 3*spec['pay'])
                finale = careers.book(s, key, town.loop.dates.story_date(3*1440).isoformat(), '10:00', kind='finale')
                s['world']['minute'] = finale['start']
                careers.begin(s, key, booking_id=finale['id'])
                self.assertEqual(careers.get(s, key)['completed'], 1)
                self.assertIsNone(careers.get(s, key)['project'])
                self.assertEqual(finale['status'], 'completed')


if __name__ == '__main__': unittest.main()
