import copy
import json
import unittest
from unittest.mock import patch
import game_core as core
import town
import groups
import phone_apps
import encounter_context as encounters


class EncounterContextTests(unittest.TestCase):
    def setUp(self):
        self.s = core.fresh('rei')
        self.s['world']['cast']['emily'].update(location=self.s['world']['location'], journey=None)

    def meeting(self):
        return self.s['groups'][self.s['active_group']]['meeting_context']['emily']

    def test_spontaneous_and_invited_meetings(self):
        town.meet(self.s, 'emily')
        self.assertEqual(self.meeting()['kind'], 'spontaneous')
        groups.close_active(self.s, 'Done')
        self.s['world']['cast']['emily']['waiting_for_hangout'] = True
        town.meet(self.s, 'emily')
        self.assertEqual(self.meeting()['kind'], 'planned')

    def test_future_plan_remembered_then_used_at_meeting(self):
        data = {'meeting_plans': [{'who': 'emily', 'status': 'agreed', 'details': 'Meet at the café tomorrow for tea.'}]}
        location = self.s['world']['location']
        encounters.record(self.s, data, ['emily'])
        self.assertEqual(self.s['world']['location'], location)
        self.assertIsNone(self.s.get('active_group'))
        saved = json.loads(json.dumps(self.s))
        self.assertIn('tomorrow', encounters.for_participants(saved, ['emily'])['agreed_future_plans']['emily']['details'])
        town.meet(self.s, 'emily')
        self.assertEqual(self.meeting()['kind'], 'planned')
        self.assertEqual(self.meeting()['arrangement']['details'], data['meeting_plans'][0]['details'])
        self.assertNotIn('emily', self.s['meeting_plans'])

    def test_summoned_character_is_a_visitor_and_journal_preserves_it(self):
        town.summon(self.s, 'emily')
        self.assertEqual(self.meeting()['kind'], 'visitor')
        self.assertEqual(self.meeting()['host'], 'rei')
        groups.close_active(self.s, 'Finished visit')
        self.assertEqual(self.s['hangout_journal'][-1]['meeting_context']['emily']['kind'], 'visitor')

    def test_public_post_and_private_delivery_context(self):
        phone_apps.post(self.s, 'I finally finished the painting!')
        key = next(iter(phone_apps.MENUS["Mario's Pizza"]))
        phone_apps.order(self.s, 'Doober Eats', key, 'emily', "Mario's Pizza")
        phone_apps.order(self.s, 'Doober Eats', key, 'garrett', "Mario's Pizza")
        context = phone_apps.conversation_context(self.s, ['emily'])
        self.assertEqual(context['latest_player_post']['text'], 'I finally finished the painting!')
        self.assertEqual(len(context['deliveries_received_by_speakers']), 1)
        self.assertEqual(context['deliveries_received_by_speakers'][0]['recipient'], 'emily')
        self.assertIn("Garrett's Noodles", context['menus'])
        self.assertIsNone(phone_apps.conversation_context(core.fresh('rei'), ['emily'])['latest_player_post'])

    def test_all_dialogue_paths_receive_apps_and_meeting_context(self):
        phone_apps.post(self.s, 'A painting of the river.')
        cases = [lambda: core.generate(self.s, 'Have you seen my latest Grove post?')]
        gid = groups.create_text(self.s, 'Friends', ['emily', 'garrett'])
        cases.append(lambda: groups.generate(self.s, gid, 'Want to order Doober Eats?'))
        self.s['world']['npcs'] = ['Maya']
        cases.append(lambda: town.generate_npc(self.s, 'Maya', 'Have you heard of Supafast?'))
        for call in cases:
            before = copy.deepcopy(self.s)
            with patch.object(core, 'request', side_effect=RuntimeError('capture only')) as request:
                with self.assertRaises(RuntimeError): call()
                payload = request.call_args.args[1]
                prompt = json.dumps(payload['messages'])
                self.assertIn('A painting of the river.', prompt)
                self.assertIn('Doober Eats', prompt)
                self.assertIn('meeting_context', prompt)
                self.assertIn('meeting_plans', payload['format']['properties'])
            self.assertEqual(self.s['world']['money'], before['world']['money'])

    def test_cancellation_and_invalid_participant(self):
        encounters.record(self.s, {'meeting_plans': [{'who': 'emily', 'status': 'agreed', 'details': 'Tea tomorrow'}]}, ['emily'])
        encounters.record(self.s, {'meeting_plans': [{'who': 'emily', 'status': 'cancelled', 'details': 'Cancelled tea'}]}, ['emily'])
        self.assertNotIn('emily', self.s['meeting_plans'])
        with self.assertRaises(ValueError):
            encounters.record(self.s, {'meeting_plans': [{'who': 'garrett', 'status': 'agreed', 'details': 'Not in conversation'}]}, ['emily'])
