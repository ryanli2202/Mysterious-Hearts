import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import dating
import game_core as core
import town
from date_fixtures import GOALS


def response(data):
    return {'message': {'content': json.dumps(data)}}


def invitation(yes=True):
    return dict(answer='yes', reply='just us? yes, please', goals=GOALS.copy()) if yes else dict(answer='no', reply='I’d like a little more time.')


def scene(**fields):
    return dict(dict(speaker='Emily Fields', addressee='Rei Takamura', choices_speaker='Rei Takamura',
                     narration='Emily looks up.', dialogue='I remember wanting to be a pilot.', memory='They talked about flying.',
                     choices=['Go on.', 'That makes sense.', 'Window seat?', 'I’d fly with you.']), **fields)


class DateTests(unittest.TestCase):
    def test_limits_vary_and_each_stat_matters(self):
        self.assertEqual(set(dating.LIMITS), set((*town.GIRLS, 'yuriko', *town.MALE_ROUTES, *town.LOCAL_MEN)))
        for who, player, stats, answer in [
            ('emily', 'rei', (0, 0, 0), 'yes'), ('emily', 'garrett', (40, 50, 40), 'no'),
            ('april', 'garrett', (30, 45, 22), 'yes'), ('april', 'rei', (30, 45, 22), 'no'),
            ('samantha', 'rei', (15, 35, 20), 'yes')]:
            s = core.fresh(player)
            s['relationships'][who].update(zip(dating.STATS, stats))
            self.assertEqual(dating.decision(s, who, 'date')[0], answer)
            self.assertEqual(dating.decision(s, who, 'official')[0], 'no')
        for kind in dating.ASK:
            s = core.fresh('rei')
            bond = s['relationships']['samantha']
            bond['status'] = 'dating'
            minimums = dating.minimums(s, 'samantha', kind)
            for stat in dating.STATS:
                bond.update(zip(dating.STATS, minimums))
                self.assertEqual(dating.decision(s, 'samantha', kind)[0], 'yes')
                bond[stat] -= 1
                self.assertEqual(dating.decision(s, 'samantha', kind)[0], 'no')
        self.assertTrue(all(a < b for a, b in zip(*dating.LIMITS['samantha'])))

    def test_decline_is_a_private_text_and_official_uses_its_own_thresholds(self):
        s = core.fresh('rei')
        who = 'samantha'
        bond = s['relationships'][who]
        bond.update(status='dating', closeness=50, trust=70, attraction=45)
        money = s['world']['money']
        no = dict(invitation(False), emotions={'rei':'hopeful',who:'guarded'})
        yes = dict(answer='yes', reply='Yeah. I want this with you.', emotions={'rei':'happy',who:'happy'})
        with patch.object(core, 'request', side_effect=[response(no), response(yes)]) as backend:
            actual = town.relationship(s, who, 'official')
            self.assertEqual(actual, no['reply'])
            self.assertEqual(bond['status'], 'dating')
            self.assertEqual(s['emotions'][who], 'guarded')
            bond.update(zip(dating.STATS, dating.minimums(s, who, 'official')))
            town.relationship(s, who, 'official')
        self.assertEqual(backend.call_args_list[0].args[1]['format']['properties']['answer']['enum'], ['no'])
        self.assertEqual(bond['status'], 'official')
        self.assertIn('official', bond['firsts'])
        self.assertEqual(s['world']['money'], money)
        history = s['routes'][who]['history']
        self.assertEqual(history[0]['content'], dating.ASK['official'])
        self.assertEqual(json.loads(history[1]['content'])['dialogue'], no['reply'])
        self.assertTrue(all(line.get('channel') == 'text' for line in history if line['role'] != 'status'))

    def test_remote_date_reloads_and_completes_only_after_actual_kiss(self):
        s = core.fresh('rei')
        money = s['world']['money']
        data = dict(invitation(), emotions={'rei':'hopeful', 'emily':'flustered'})
        with patch.object(core, 'request', return_value=response(data)) as backend:
            town.relationship(s, 'emily', 'date')
            self.assertIn('goals', backend.call_args.args[1]['format']['required'])
        self.assertEqual(s['world']['money'], money)
        self.assertFalse(s['date_session']['started'])
        with self.assertRaises(ValueError):
            dating.commit_invitation(s, 'emily', 'date', data)
        with self.assertRaises(ValueError):
            core.commit(s, 'Can we count that?', scene(date_progress=['activity']))
        core.commit(s, 'sending a kiss', scene(romance_event='kiss'))
        self.assertEqual(s['date_session']['done'], [])
        town.summon(s, 'emily')
        town.meet(s, 'emily')
        self.assertEqual(s['world']['money'], money - dating.PRICE)
        choices = dict(choices_speaker='Rei Takamura', choices=scene()['choices'],
                       personal_choices=['How was work?', 'When did you start?', 'Painting helps me think.', 'Can we talk about yesterday?'],
                       action_choices=['I wave.', 'I nod.', 'I bow.', 'I wink.'])
        generated = scene(emotions={'rei':'curious', 'emily':'happy'}, input_tone='Connection',
                          bond_moments={'emily':'personal_detail'}, date_progress=['conversation'])
        with patch.object(core, 'request', side_effect=[response(generated), response(choices)]) as backend:
            line = 'What did you want to be?'
            core.commit(s, line, core.generate(s, line))
            self.assertIn('date_progress', backend.call_args_list[0].args[1]['format']['required'])
        self.assertEqual(s['date_session']['done'], ['conversation'])
        route = s['routes']['emily']
        self.assertEqual(route['choices'],[])
        import suggestions
        with patch.object(core, 'request', return_value=response(dict(choices_speaker='Rei Takamura',choices=choices['personal_choices']))) as backend:
            target=('route','emily'); stamp=suggestions.stamp(s,target)
            lines=suggestions.generate(s,target,'personal')
            self.assertTrue(suggestions.apply(s,target,'personal',stamp,lines))
            self.assertEqual(backend.call_count,1)
        self.assertEqual(core.personal_choices(s, route), choices['personal_choices'])
        for tone, line in zip(core.PERSONAL_TONES, choices['personal_choices']):
            self.assertEqual(core.selected_tone(s, line), tone)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'saved.json'
            core.save(s, path)
            s = core.load(path)
        with self.assertRaises(ValueError):
            core.commit(s, core.SCENE_DIRECTIONS[1], scene(date_progress=['activity']))
        before = copy.deepcopy(s)
        with self.assertRaises(ValueError):
            core.commit(s, 'Again?', scene(date_progress=['conversation']))
        self.assertEqual(s, before)
        core.commit(s, 'Teach me that step.', scene(date_progress=['activity']))
        self.assertNotIn('date', s['relationships']['emily'].get('firsts', {}))
        core.commit(s, 'May I kiss you?', scene(romance_event='none'))
        self.assertEqual(s['date_session']['done'], ['conversation', 'activity'])
        core.commit(s, 'I meet her halfway.', scene(romance_event='kiss'))
        bond = s['relationships']['emily']
        self.assertNotIn('date_session', s)
        self.assertEqual(bond['status'], 'dating')
        self.assertEqual(set(bond['firsts']), {'kiss', 'date'})
        self.assertEqual(bond['last_date']['goals'], GOALS)
        dating.commit_invitation(s, 'emily', 'date', invitation())
        self.assertEqual(s['date_session']['done'], ['kiss'])

    def test_bad_generation_retries_before_state_changes(self):
        s = core.fresh('rei')
        before = copy.deepcopy(s)
        bad = dict(invitation(), goals=dict(GOALS, activity=GOALS['conversation']))
        with patch.object(core, 'request', return_value=response(bad)) as backend, self.assertRaises(ValueError):
            town.relationship(s, 'emily', 'date')
        self.assertEqual(backend.call_count, 2)
        self.assertEqual(s, before)
        with patch.object(core, 'request') as backend, self.assertRaises(ValueError):
            town.relationship(s, 'yuriko', 'date')
        backend.assert_not_called()

    def test_funding_cancellation_and_private_date_context(self):
        s = core.fresh('rei')
        s['world']['money'] = 0
        town.summon(s, 'emily')
        dating.commit_invitation(s, 'emily', 'date', invitation())
        self.assertFalse(dating.in_hangout(s, 'emily'))
        self.assertIn(GOALS['activity'], town.context(s, 'emily'))
        self.assertNotIn(GOALS['activity'], town.context(s, 'sophie'))
        self.assertNotIn('date', s['relationships']['emily'].get('firsts', {}))
        s['world']['money'] = dating.PRICE
        town.meet(s, 'emily')
        self.assertTrue(dating.in_hangout(s, 'emily'))
        self.assertEqual(s['world']['money'], 0)
        dating.cancel(s, 'emily')
        self.assertNotIn('date_session', s)
        self.assertNotEqual(s['relationships']['emily']['status'], 'dating')
        self.assertEqual(dating.decision(s, 'emily', 'date')[0], 'yes')

    def test_personal_panel_repairs_missing_generated_choices(self):
        s = core.fresh('rei')
        personal = ['What made your day?', 'Tell me about your greenhouse.', 'I paint to unwind.', 'Want to talk about it?']
        choices = dict(choices=scene()['choices'], choices_speaker='Rei Takamura')
        with patch.object(core, 'request', side_effect=[response(choices), response(dict(choices,personal_choices=personal))]) as backend:
            result = core.generate_player_choices(s, 'Hello.', scene())
        self.assertEqual(backend.call_count, 2)
        self.assertEqual(result['personal_choices'], personal)

    def test_local_resident_cannot_unlock_a_date(self):
        s = core.fresh('ivan')
        s['world']['npcs'] = ['Theo']
        for _ in range(3):
            town.social_event(s, 'Theo', 'returned_flirt')
        self.assertNotIn('Theo', s['relationships'])
        self.assertFalse(town.romanceable(s, 'Theo'))
        self.assertFalse(dating.begin(s, 'Theo'))
        with self.assertRaises(ValueError):
            dating.commit_invitation(s, 'Theo', 'date', invitation())
        self.assertNotIn('date_session', s)
