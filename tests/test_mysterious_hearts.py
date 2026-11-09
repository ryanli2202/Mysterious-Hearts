import copy
import json
import unittest
from unittest.mock import patch

import game_core as core
import mysterious_hearts as h
import contact_profiles as p
import memory_store
import dating


class HeartsTests(unittest.TestCase):
    def setUp(self):
        self.s = core.fresh('rei')
        self.ident = h.send(self.s, 'emily', 'rei', 'You mean a great deal to me.', 'confession')

    def test_private_identity_and_reply(self):
        self.assertIsNone(h.view(self.s, self.ident, 'rei')['sender'])
        self.assertEqual(h.view(self.s, self.ident, 'emily')['sender'], 'emily')
        self.assertEqual(h.inbox(self.s, 'sophie'), [])
        with self.assertRaises(ValueError): h.reply(self.s, self.ident, 'sophie', 'Hi')
        h.reply(self.s, self.ident, 'rei', 'Who are you?')
        self.assertEqual(h.view(self.s, self.ident, 'emily')['messages'][-1]['role'], 'recipient')

    def test_shared_copy_not_live_feed_or_identity(self):
        h.action(self.s, self.ident, 'rei', 'share', 'sophie')
        h.reply(self.s, self.ident, 'emily', 'Another private message')
        h.action(self.s, self.ident, 'emily', 'reveal')
        view = h.view(self.s, self.ident, 'sophie')
        self.assertEqual(len(view['messages']), 1)
        self.assertIsNone(view['sender'])
        self.assertEqual(h.view(self.s, self.ident, 'rei')['sender'], 'emily')

    def test_guesses_do_not_confirm_and_are_individual(self):
        h.clue(self.s, self.ident, 'rei', 'amy', 'Sounds like Amy', 95)
        h.action(self.s, self.ident, 'rei', 'suspect', 'amy')
        self.assertFalse(h.view(self.s, self.ident, 'rei')['confirmed'])
        self.assertIsNone(h.view(self.s, self.ident, 'emily')['case']['selected'])
        h.clue(self.s, self.ident, 'rei', 'amy', 'Could also be someone else', -25)
        self.assertEqual(h.case(self.s, self.ident, 'rei')['suspects']['amy'], 70)

    def test_accusation_directional_once(self):
        before = self.s['relationships']['amy']['trust']
        h.action(self.s, self.ident, 'rei', 'accuse', 'amy')
        h.action(self.s, self.ident, 'rei', 'accuse', 'amy')
        self.assertEqual(self.s['relationships']['amy']['trust'], before-4)
        self.assertIsNone(h.view(self.s, self.ident, 'rei')['sender'])

    def test_block_cannot_be_bypassed_with_new_thread(self):
        h.action(self.s, self.ident, 'rei', 'block')
        with self.assertRaises(ValueError): h.reply(self.s, self.ident, 'emily', 'Hello')
        with self.assertRaises(ValueError): h.send(self.s, 'emily', 'rei', 'New thread')

    def test_affinity_not_transferred_on_reveal(self):
        before = self.s['relationships']['emily']['attraction']
        h.action(self.s, self.ident, 'rei', 'welcome')
        h.action(self.s, self.ident, 'emily', 'reveal')
        self.assertEqual(self.s['relationships']['emily']['attraction'], before)
        self.assertEqual(h.view(self.s, self.ident, 'rei')['affinity'], 10)

    def test_canon_and_simulation_change(self):
        self.assertEqual(h.feeling(self.s, 'emily', 'rei'), 80)
        self.assertEqual(h.feeling(self.s, 'emily', 'garrett'), 0)
        self.s['relationships']['emily'].update(attraction=0, unresolved_harm=True)
        for hour in range(1, 49):
            self.s['world']['minute'] = hour*60
            h.tick(self.s)
        self.assertLess(h.feeling(self.s, 'emily', 'rei'), 30)
        self.assertEqual(h.view(self.s, self.ident, 'rei')['messages'][0]['text'], 'You mean a great deal to me.')

    def test_no_replay_and_no_player_autonomous_messages(self):
        self.s['world']['minute'] = 18*60
        h.tick(self.s)
        saved = copy.deepcopy(h.ensure(self.s))
        h.tick(self.s)
        self.assertEqual(h.ensure(self.s), saved)
        self.assertFalse(any(t['sender'] == 'rei' for t in saved['threads']))

    def test_hourly_feelings_survive_reload_and_ignore_global_randomness(self):
        restored = json.loads(json.dumps(self.s))
        initial = copy.deepcopy(h.ensure(self.s)['feelings'])
        # Simulate unrelated workers/minigames leaving opposite random streams.
        # Compare the full subsystem, including sustained feelings and queued notes.
        for state, roll in ((self.s, 0.0), (restored, .999999)):
            with patch('romantic_types.random.random', return_value=roll):
                for hour in range(9, 33):
                    state['world']['minute'] = hour*60
                    h.tick(state)
        self.assertEqual(h.ensure(self.s), h.ensure(restored))
        self.assertNotEqual(h.ensure(self.s)['feelings'], initial)

    def test_npc_to_npc_even_without_player(self):
        s = core.fresh('garrett'); s['world']['minute'] = 18*60
        h.tick(s)
        pending = next(p for p in h.ensure(s)['pending'] if p['actor'] == 'emily')
        h.commit_note(s, pending, 'A generated note.')
        notes = [t for t in h.ensure(s)['threads'] if t['sender'] == 'emily']
        self.assertEqual(notes[0]['recipient'], 'rei')
        self.assertNotIn(notes[0]['id'], [row['id'] for row in h.inbox(s, 'garrett')])

    def test_generated_reply_uses_provider_and_discards_stale_result(self):
        h.queue_note(self.s, 'emily', 'rei', 'reply', self.ident)
        p = h.ensure(self.s)['pending'][0]
        with patch.object(core, 'request', return_value={'message': {'content': '{"text":"Your reply made my evening."}'}}) as request:
            text = h.generate(self.s, p)
        self.assertEqual(request.call_args.args[0], '/api/chat')
        h.reply(self.s, self.ident, 'rei', 'Another question')
        self.assertFalse(h.commit_note(self.s, p, text))
        self.assertEqual(len(h._thread(self.s, self.ident)['messages']), 2)

    def test_recipient_prompt_does_not_include_hidden_identity(self):
        ident = h.send(self.s, 'amy', 'emily', 'Hello there')
        h.queue_note(self.s, 'emily', 'amy', 'reply', ident)
        p = h.ensure(self.s)['pending'][0]
        with patch.object(core, 'request', return_value={'message': {'content': '{"text":"That is kind of you."}'}}) as request:
            h.generate(self.s, p)
        payload = json.loads(request.call_args.args[1]['messages'][1]['content'])
        self.assertNotIn('recipient', payload)
        self.assertNotIn('relationship', payload)
        self.assertNotIn('memories', payload)

    def test_blocked_pending_note_is_not_delivered(self):
        h.queue_note(self.s, 'emily', 'rei', 'reply', self.ident)
        p = h.ensure(self.s)['pending'][0]
        h.action(self.s, self.ident, 'rei', 'block')
        self.assertFalse(h.commit_note(self.s, p, 'This must not appear.'))

    def test_invalid_and_identifying_generation_rejected(self):
        h.queue_note(self.s, 'emily', 'rei', 'reply', self.ident)
        for text in ('', 'It is Emily here.'):
            with patch.object(core, 'request', return_value={'message': {'content': json.dumps({'text': text})}}):
                with self.assertRaises(ValueError): h.generate(self.s, h.ensure(self.s)['pending'][0])

    def test_pump_failure_and_save_switch(self):
        from types import SimpleNamespace
        from hearts_ai import NotePump
        from unittest.mock import Mock
        h.queue_note(self.s, 'emily', 'rei', 'reply', self.ident)
        p = h.ensure(self.s)['pending'][0]
        game = SimpleNamespace(state_data=self.s, in_game=True, busy=True, persist=Mock())
        pump = NotePump(game)
        pump.results.put((self.s, p['id'], None, True))
        pump.tick()
        self.assertTrue(p['error'])
        self.assertEqual(len(h._thread(self.s, self.ident)['messages']), 1)
        game.state_data = core.fresh('rei')
        pump.results.put((self.s, p['id'], 'Late reply', False))
        pump.tick()
        self.assertEqual(h.ensure(game.state_data)['threads'], [])

    def test_serialization_and_additive_upgrade(self):
        before = copy.deepcopy(self.s['routes'])
        restored = json.loads(json.dumps(self.s))
        core.town.ensure(restored)
        self.assertEqual(restored['routes'], before)
        self.assertEqual(h.view(restored, self.ident, 'rei'), h.view(self.s, self.ident, 'rei'))
        del restored['mysterious_hearts']; del restored['contact_profiles']
        core.town.ensure(restored)
        self.assertEqual(h.feeling(restored, 'emily', 'rei'), 80)

    def test_private_selected_and_public_fields(self):
        p.edit(self.s, 'rei', 'Food', 'Noodles', 'selected', ['emily'])
        p.edit(self.s, 'rei', 'Movies', 'Secret film', 'private')
        self.assertEqual(p.public(self.s, 'rei', 'emily')['Food'], 'Noodles')
        self.assertNotIn('Food', p.public(self.s, 'rei', 'amy'))
        self.assertNotIn('Movies', p.public(self.s, 'rei', 'amy'))
        self.assertEqual(p.public(self.s, 'rei', 'rei')['Movies'], 'Secret film')

    def test_notebook_discovery_and_pin(self):
        memory_store.add(self.s, source='test', text='My favorite food is ramen.', owners=['emily', 'rei'], subjects=['emily'], kind='fact')
        p.add(self.s, 'rei', 'emily', 'Question', 'Was that note yours?')
        p.toggle(self.s, 'rei', 'emily', 1, 'pinned')
        view = p.view(self.s, 'emily', 'rei')
        self.assertEqual(view['favourites']['Food']['value'], 'ramen')
        self.assertTrue(view['notebook'][0]['pinned'])
        self.assertEqual(p.view(self.s, 'emily', 'amy')['discoveries'], [])
        self.assertEqual(p.view(self.s, 'emily', 'amy')['notebook'], [])

    def test_lost_crush_removes_automatic_date_acceptance(self):
        h.ensure(self.s)['feelings']['emily']['rei'] = 10
        self.s['relationships']['emily'].update(attraction=5, trust=40, closeness=20)
        self.assertEqual(dating.decision(self.s, 'emily', 'date')[0], 'no')

    def test_canon_persists_without_relationship_change(self):
        for hour in range(1, 49):
            self.s['world']['minute'] = hour*60
            h.tick(self.s)
        self.assertGreaterEqual(h.feeling(self.s, 'emily', 'rei'), 80)

    def test_bystander_context_has_no_private_thread(self):
        self.assertEqual(h.context(self.s, 'amy')['anonymous_threads'], [])
        self.assertNotIn('emily', json.dumps(h.context(self.s, 'rei')))

    def test_memory_clue_requires_own_evidence(self):
        text = 'Rei and Emily watched the rain from the flower shop doorway.'
        memory_store.add(self.s, source='rain', text=text, owners=['emily', 'rei'])
        ident = h.send(self.s, 'emily', 'rei', 'I keep thinking about this: '+text)
        self.assertTrue(h.inspect(self.s, ident, 'rei'))
        self.assertEqual(h.case(self.s, ident, 'rei')['suspects']['emily'], 35)
        h.action(self.s, ident, 'rei', 'share', 'amy')
        self.assertFalse(h.inspect(self.s, ident, 'amy'))
        self.assertFalse(h.view(self.s, ident, 'rei')['confirmed'])


if __name__ == '__main__': unittest.main()
