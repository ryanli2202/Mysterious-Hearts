import random
import unittest
from unittest.mock import Mock, patch
from copy import deepcopy
import tkinter as tk
import arcade_games as g
from mini_games_ui import Arcade
from sound import SoundSystem


class PuzzleRules(unittest.TestCase):
    def test_memory_pairs_and_mismatch_lock(self):
        m = g.MemoryMatch()
        m.cards = list(range(8)) * 2
        self.assertTrue(m.flip(0))
        self.assertFalse(m.flip(0))
        m.flip(1)
        self.assertFalse(m.flip(2))
        m.hide()
        for i in range(8):
            m.flip(i)
            m.flip(i + 8)
        self.assertTrue(m.over)
        self.assertEqual(m.moves, 9)

    def test_mines_first_reveal_flags_win_and_loss(self):
        for difficulty in ('Easy', 'Medium', 'Hard'):
            m = g.Minesweeper(difficulty)
            m.flag((0, 0))
            m.reveal((0, 0))
            self.assertFalse(m.started)
            m.flag((0, 0))
            m.reveal((0, 0))
            self.assertEqual(len(m.mines), m.mine_count)
            self.assertFalse(m.mines & (m.neighbors((0, 0)) | {(0, 0)}))
            for y in range(m.size):
                for x in range(m.size):
                    if (x, y) not in m.mines: m.reveal((x, y))
            self.assertTrue(m.won)
        m = g.Minesweeper()
        m.reveal((0, 0))
        m.reveal(next(iter(m.mines)))
        self.assertTrue(m.over)
        self.assertFalse(m.won)

    def test_breakout_brick_paddle_lives_and_win(self):
        m = g.Breakout()
        m.launch()
        m.x, m.y, m.vx, m.vy = 30, 29, 0, 5
        m.step()
        self.assertEqual(len(m.bricks), 39)
        self.assertEqual(m.score, 10)
        self.assertEqual(m.event, 'brick')
        m.x, m.y, m.vy = m.paddle, 342, 4
        m.step()
        self.assertLess(m.vy, 0)
        for _ in range(3):
            m.launch()
            m.y = 411
            m.vy = 4
            m.step()
        self.assertTrue(m.over)
        self.assertEqual(m.lives, 0)
        m = g.Breakout()
        m.bricks = {(0, 0)}
        m.x, m.y, m.vx, m.vy = 30, 29, 0, 5
        m.launch()
        m.step()
        self.assertTrue(m.won)

    def test_match3_stable_board_swaps_cascades_and_end(self):
        for _ in range(10):
            m = g.Match3()
            self.assertFalse(m.find_matches())
            legal = m.legal_moves()
            self.assertTrue(legal)
            before = deepcopy(m.board)
            self.assertFalse(m.swap((0, 0), (6, 6)))
            self.assertEqual(m.board, before)
            m.moves = 1
            self.assertTrue(m.swap(*legal[0]))
            for _ in range(100):
                if not m.matches: break
                m.settle()
            self.assertFalse(m.matches)
            self.assertTrue(m.over)
            self.assertGreaterEqual(m.score, 30)
            self.assertEqual(sum(map(len, m.board)), 49)
            self.assertTrue(all(0 <= value < 5 for row in m.board for value in row))

    def test_wordsearch_words_exist_and_reverse_selection_wins(self):
        for _ in range(30):
            m = g.WordSearch()
            for word in m.words:
                path = m.paths[word]
                self.assertEqual(''.join(m.board[y][x] for x, y in path), word)
                self.assertTrue(m.select(path[-1], path[0]))
            self.assertTrue(m.over)
        self.assertEqual(g.WordSearch.line((0, 0), (2, 1)), [])

    def test_simon_round_and_failure(self):
        m = g.Simon()
        for round in range(1, 5):
            for color in list(m.sequence): outcome = m.press(color)
            self.assertEqual(outcome, 'round')
            self.assertEqual(m.score, round)
            self.assertEqual(len(m.sequence), round + 1)
        self.assertEqual(m.press((m.sequence[0] + 1) % 4), 'lose')
        self.assertTrue(m.over)

    def test_solitaire_deal_recycle_and_moves(self):
        m = g.Solitaire()
        all_cards = m.stock + [c for pile in m.tableau for c in pile]
        self.assertEqual(len(set(all_cards)), 52)
        self.assertEqual(list(map(len, m.tableau)), list(range(1, 8)))
        stock = m.stock[:]
        for _ in range(24): m.draw()
        m.draw()
        self.assertEqual(m.stock, stock)
        m.tableau = [[(9, 0), (8, 2)], [(10, 3)], [], [], [], [], []]
        m.hidden = [0] * 7
        self.assertTrue(m.move(('tableau', 0, 0), ('tableau', 1)))
        self.assertEqual(m.tableau[1], [(10, 3), (9, 0), (8, 2)])
        self.assertFalse(m.move(('tableau', 1, 1), ('tableau', 2)))
        m.waste = [(1, 0)]
        self.assertTrue(m.auto(('waste', 0, 0)))
        m.waste = [(3, 0)]
        self.assertFalse(m.auto(('waste', 0, 0)))
        m.tableau[0] = [(7, 2), (13, 0)]
        m.hidden[0] = 1
        self.assertFalse(m.move(('tableau', 0, 0), ('tableau', 2)))
        self.assertTrue(m.move(('tableau', 0, 1), ('tableau', 2)))
        self.assertEqual(m.hidden[0], 0)


class ExpandedViewTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.errors = []
        self.root.report_callback_exception = lambda *args: self.errors.append(args)
        self.sounds = Mock()
        self.a = Arcade(self.root, {}, self.sounds)

    def tearDown(self):
        self.root.destroy()
        self.assertFalse(self.errors)

    def finish(self):
        a = self.a
        if a.animation:
            start, duration = a.animation['start'], a.animation['duration']
            for fraction in (.2, .5, .8, 1.1):
                a.after_cancel(a.animation_timer)
                with patch('mini_games_ui.monotonic', return_value=start + duration * fraction): a.animation_frame()

    def test_new_game_interactions_and_cancel(self):
        a = self.a
        a.open('Memory Match')
        a.model.cards = list(range(8)) * 2
        a.extra_click(50, 50)
        self.finish()
        a.extra_click(150, 50)
        self.finish()
        self.assertTrue(a.jobs)
        a.memory_hide()
        self.finish()
        a.open('Minesweeper')
        a.extra_click(50, 50)
        self.finish()
        self.assertTrue(a.model.started)
        a.open('Match-3')
        first, second = a.model.legal_moves()[0]
        for x, y in (first, second): a.extra_click((x + .5) * 400 / 7, (y + .5) * 400 / 7)
        self.finish()
        a.cancel_jobs()
        for _ in range(100):
            if not a.model.matches: break
            a.match_flash()
            self.finish()
            a.cancel_jobs()
            a.match_settle()
            self.finish()
            a.cancel_jobs()
        a.match_continue()
        self.assertFalse(a.busy)
        a.open('Word Search')
        path = a.model.paths[a.model.words[0]]
        for x, y in (path[0], path[-1]): a.extra_click(x * 40 + 20, y * 32 + 16)
        self.finish()
        self.assertEqual(len(a.model.found), 1)
        a.open('Solitaire')
        a.extra_click(25, 25)
        self.finish()
        self.assertEqual(len(a.model.waste), 1)
        a.open('Breakout')
        a.paused = False
        a.action('space')
        self.finish()
        a.tick()
        self.finish()
        a.open('Simon Says')
        a.cancel_jobs()
        a.busy = False
        a.simon_press(a.model.sequence[0])
        self.assertEqual(a.model.score, 1)
        self.assertTrue(a.jobs)
        a.menu()
        self.assertFalse(a.jobs)
        self.assertIsNone(a.timer)
        self.assertIsNone(a.animation_timer)
        a.open('Simon Says')
        a.destroy()
        self.root.update()

    def test_existing_games_cues_and_mute(self):
        a = self.a
        for name, action, cue in [('Connect 4', '4', 'drop'), ('2048', 'left', 'merge'),
                                   ('Blackjack', 'hit', 'card'), ('Tetris', 'up', 'rotate')]:
            a.open(name)
            if name == '2048': a.model.board = [[2, 2, 0, 0]] + [[0] * 4 for _ in range(3)]
            if name == 'Blackjack':
                a.model.result = ''
                a.model.player = [(2, 'S'), (3, 'H')]
                a.model.deck = [(4, 'S')]
            if name == 'Tetris':
                a.paused = False
                a.model.kind = 2
                a.model.piece = [(1, 0), (0, 1), (1, 1), (2, 1)]
            self.sounds.play.reset_mock()
            a.action(action)
            self.sounds.play.assert_called_with('arcade_' + cue)
        a.open('Snake')
        a.model.food = (10, 10)
        a.paused = False
        a.tick()
        self.sounds.play.assert_called_with('arcade_eat')
        a.open('Pong')
        a.paused = False
        a.model.x, a.model.y, a.model.vx = 30, 200, -4
        a.tick()
        self.sounds.play.assert_called_with('arcade_bounce')
        a.toggle_sound()
        self.sounds.play.reset_mock()
        a.effect('win')
        self.sounds.play.assert_not_called()

    def test_reduced_motion_keeps_rules_and_simon_timing(self):
        with patch('phone_personalization.preferences', return_value={'reduced_motion': True}):
            self.a.open('Memory Match')
            self.a.extra_click(50, 50)
            self.assertEqual(len(self.a.model.face_up), 1)
            self.assertIsNone(self.a.animation_timer)
            self.a.open('Simon Says')
            self.assertTrue(self.a.jobs)


class ArcadeAudioTests(unittest.TestCase):
    def test_waveaudio_fallback_scales_volume_and_reloads(self):
        with patch('sound.sys.platform', 'test'): sounds = SoundSystem()
        sounds._mci = Mock(side_effect=lambda command, *args: 277 if 'type mpegvideo' in command else 0)
        with patch('phone_personalization.preferences', return_value={'notification_volume': 30}):
            sounds.play('arcade_note0')
            self.assertEqual(sounds._arcade_wave['arcade_note0'], 30)
        with patch('phone_personalization.preferences', return_value={'notification_volume': 0}):
            sounds.play('arcade_note0')
            self.assertEqual(sounds._arcade_wave['arcade_note0'], 0)
            import wave
            from pathlib import Path
            with wave.open(str(Path(sounds._arcade_cache.name) / 'note0.wav'), 'rb') as audio:
                self.assertFalse(any(audio.readframes(audio.getnframes())))
        sounds.close()
        self.assertIsNone(sounds._arcade_cache)

    def test_lazy_loading_master_mute_and_cleanup(self):
        with patch('sound.sys.platform', 'test'): sounds = SoundSystem()
        sounds._mci = Mock(return_value=0)
        sounds.play('arcade_merge')
        self.assertIn('arcade_merge', sounds._aliases)
        alias = sounds._aliases['arcade_merge']
        sounds._mci.assert_called_with(f'play {alias} from 0', None, 0, None)
        sounds.stop_arcade()
        sounds._mci.assert_called_with(f'stop {alias}', None, 0, None)
        sounds.toggle()
        sounds._mci.reset_mock()
        sounds.play('arcade_win')
        sounds._mci.assert_not_called()
        sounds.close()


if __name__ == '__main__': unittest.main()
