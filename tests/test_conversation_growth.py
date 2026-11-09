from date_fixtures import next_morning
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import game_core as core
import groups
import town


def exchange(line='Ha! That was yours?', moment='none', event='none'):
    return dict(narration='Emily sets the photo down.', dialogue=line, memory='They looked at a photo.',
                speaker='Emily Fields', addressee='Garrett Han', choices_speaker='Garrett Han',
                choices=['Yep.', 'It was a gift.', 'Look closer.', 'Keep it.'],
                bond_moments={'emily': moment}, social_event=event,
                emotions={'garrett':'content', 'emily':'amused'}, input_tone='Other')


class ConversationGrowthTests(unittest.TestCase):
    def test_phone_laughter_and_spoken_delivery_on_first_meeting(self):
        state = core.fresh()
        for line in ('lol, tbh that tracks', 'wyd after practice?', 'LMAO', 'WE WON!!!'):
            core.validate_response(exchange(line), state)
        town.travel(state, 'flowers')
        town.finish_drive(state)
        # This is still the phone route until the generated scene establishes the meeting.
        for line in ('LMAOOOO', 'tbh you had me', 'wyd?', 'WE WON!!!', 'I opened it and… OH MY GOD!'):
            with self.subTest(line=line), self.assertRaisesRegex(ValueError, 'spoken words'):
                core.validate_response(dict(exchange(line), conversation_channel='in_person'), state)
        core.validate_response(dict(exchange('Ha! Was the LEGO set yours?'), conversation_channel='in_person'), state)
        town.meet(state, 'emily')
        before = copy.deepcopy(state)
        with self.assertRaises(ValueError):
            core.commit(state, 'Hello', dict(exchange(), choices=['LOL', 'Sure.', 'Wait.', 'Okay.']))
        self.assertEqual(state, before)

    def test_in_person_generation_retries_a_textism_in_the_players_suggestions(self):
        state = core.fresh()
        town.summon(state, 'emily')
        scene = exchange(moment='shared_laugh')
        choices = dict(choices_speaker='Garrett Han', choices=scene['choices'],
                       personal_choices=core.personal_choices(state, {}),
                       action_choices=['I nod.', 'I grin.', 'I bow.', 'I wink.'])
        outputs = [scene, dict(choices, choices=['LMAO', *choices['choices'][1:]]), choices]
        with patch.object(core, 'request', side_effect=[
                {'message': {'content': json.dumps(out)}} for out in outputs]) as model:
            result = core.generate(state, 'You really kept that photo?')
            self.assertEqual(model.call_count,1)
            self.assertEqual(result['choices'],[])
            core.commit(state,'You really kept that photo?',result)
            import suggestions
            suggested=suggestions.generate(state,('route','emily'))
        self.assertEqual(model.call_count, 3)
        self.assertIn(core.SPOKEN_DELIVERY, model.call_args.args[1]['messages'][0]['content'])
        self.assertEqual(suggested, scene['choices'])

    def test_daily_familiarity_and_personal_exchanges_survive_reload(self):
        state = core.fresh()
        r = state['relationships']['emily']
        trust, closeness, attraction = r['trust'], r['closeness'], r['attraction']
        core.commit(state, core.INCOMING_TEXT, exchange(moment='personal_detail'))
        self.assertEqual((r['trust'], r['closeness']), (trust, closeness))
        for moment in ('personal_detail', 'support', 'shared_laugh', 'personal_detail'):
            core.commit(state, 'Tell me more.', exchange(moment=moment))
        self.assertEqual((r['trust'], r['closeness'], r['attraction']), (trust + 5, closeness + 6, attraction))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'story.json'
            core.save(state, path)
            state = core.load(path)
        r = state['relationships']['emily']
        core.commit(state, 'How about you?', exchange(moment='personal_detail'))
        self.assertEqual(r['bond_bonus_count'], 3)
        self.assertEqual(r['trust'], trust + 5)
        next_morning(state)
        core.commit(state, 'I remember that one.', exchange(moment='chemistry'))
        self.assertEqual((r['trust'], r['closeness'], r['attraction']), (trust + 8, closeness + 10, attraction + 1))

    def test_attraction_grows_on_welcome_and_reciprocation(self):
        state = core.fresh()
        r = state['relationships']['emily']
        start = r['attraction']
        closeness = r['closeness']
        for event in ('flirt', 'welcomed_flirt', 'returned_flirt'):
            core.commit(state, 'I like your smile.', exchange(moment='none', event=event))
        self.assertEqual(r['attraction'], start + 5)
        self.assertEqual(r['closeness'], closeness + 4)
        before = dict(r)
        core.commit(state, 'Another compliment.', exchange(moment='setback', event='welcomed_flirt'))
        self.assertEqual(r, before)
        r['status'] = 'strained'
        core.commit(state, 'Still flirting.', exchange(moment='chemistry', event='returned_flirt'))
        self.assertEqual(r['attraction'], start + 5)

    def test_siblings_and_platonic_friends_only_build_trust_and_closeness(self):
        for player, who in [('rei', 'yuriko'), ('ivan', 'valentina'), ('garrett', 'rosa')]:
            with self.subTest(player=player, who=who):
                state = core.fresh(player)
                r = town.character_stats(state, who)
                before = r.copy()
                town.social_event(state, who, 'returned_flirt')
                town.conversation_progress(state, who, 'chemistry')
                self.assertGreater(r['trust'], before['trust'])
                self.assertGreater(r['closeness'], before['closeness'])
                self.assertEqual(r['attraction'], 0)
                self.assertNotIn(who, state['relationships'])

    def test_group_bonus_and_attraction_go_to_the_people_involved(self):
        state = core.fresh()
        gid = groups.create_text(state, 'Weekend', ['emily', 'sophie'])
        data = dict(narration='Two texts arrive.', choices=exchange()['choices'],
                    lines=[dict(speaker='Emily Fields', text='oh haha, i remember that'),
                           dict(speaker='Sophie Parker', text='LMAO')],
                    social_target='emily', social_event='welcomed_flirt',
                    bond_moments={'emily':'personal_detail', 'sophie':'shared_laugh'})
        before = copy.deepcopy(state['relationships'])
        groups.commit(state, gid, 'Remember my costume?', data)
        for who, gains in [('emily', (3, 4, 2)), ('sophie', (1, 3, 0)), ('amy', (0, 0, 0))]:
            self.assertEqual(tuple(state['relationships'][who][k] - before[who][k]
                                   for k in ('trust', 'closeness', 'attraction')), gains)
        saved = copy.deepcopy(state)
        with self.assertRaises(ValueError):
            groups.commit(state, gid, 'Hello', dict(data, bond_moments={'amy':'support'}))
        self.assertEqual(state, saved)
