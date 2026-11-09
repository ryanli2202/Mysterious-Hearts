import tempfile
import unittest
from pathlib import Path
import game_core as core
import town

class MinsuTests(unittest.TestCase):
    def test_playable_routes_and_home(self):
        state = core.fresh('minsu')
        for who in core.CONTACTS:
            if who == 'minsu': continue
            state['active'] = who
            core.hidden.mark_met(state, who)
            if who in core.hidden.CAST: core.hidden.add_contact(state, who)
            messages = core.build_messages(state, core.INCOMING_TEXT)
            self.assertIn('Minsu Park', str(messages))
        self.assertGreater(state['relationships']['amy']['closeness'], 70)
        self.assertGreater(state['relationships']['sophie']['closeness'], 70)
        for who in ('emily', 'samantha', 'april'):
            self.assertEqual(state['relationships'][who]['closeness'], 0)
            self.assertEqual(state['relationships'][who]['status'], 'strangers')
        for who in ('garrett', 'rei'):
            self.assertEqual(state['friendships'][who]['closeness'], 0)
        town.travel(state, 'home'); town.finish_drive(state)
        town.home_action(state, town.HOME_ACTIONS['minsu'][0])
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'story.json'
            core.save(state, path)
            self.assertEqual(core.load(path), state)

    def test_old_save_adds_contact_without_reset(self):
        state = core.fresh('rei')
        state['routes'].pop('minsu')
        state['world']['cast'].pop('minsu')
        state['friendships'].pop('minsu')
        state['relationships']['amy']['closeness'] = 63
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'story.json'
            core.save(state, path)
            loaded = core.load(path)
        self.assertIn('minsu', loaded['routes'])
        self.assertIn('minsu', loaded['world']['cast'])
        self.assertIn('minsu', loaded['friendships'])
        self.assertEqual(loaded['relationships']['amy']['closeness'], 63)
