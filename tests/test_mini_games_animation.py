"""Animation paths and mounted-view lifecycle regression checks."""
import random
import tkinter as tk
import unittest
from unittest.mock import patch

from mini_games import Tiles2048
from mini_games_ui import Arcade, ENGINES, tile_paths


class TilePathTests(unittest.TestCase):
    def test_paths_match_engine_in_every_direction(self):
        rng = random.Random(42)
        for direction in ('left', 'right', 'up', 'down'):
            for _ in range(100):
                model = Tiles2048()
                model.board = [[rng.choice((0, 2, 4, 8)) for _ in range(4)] for _ in range(4)]
                paths, merges = tile_paths(model.board, direction)
                expected = [[0] * 4 for _ in range(4)]
                sources, targets = set(), {}
                for source, (x, y), value in paths:
                    self.assertNotIn(source, sources)
                    sources.add(source)
                    expected[y][x] += value
                    targets[(x, y)] = targets.get((x, y), 0) + 1
                self.assertEqual(merges, {cell for cell, count in targets.items() if count == 2})
                with patch.object(model, 'spawn'):
                    model.move(direction)
                self.assertEqual(expected, model.board)


class AnimationViewTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.errors = []
        self.root.report_callback_exception = lambda *args: self.errors.append(args)
        self.arcade = Arcade(self.root, {})

    def tearDown(self):
        self.root.destroy()
        self.assertFalse(self.errors)

    def finish_frames(self):
        arcade = self.arcade
        self.assertIsNotNone(arcade.animation_timer)
        start, duration = arcade.animation['start'], arcade.animation['duration']
        for fraction in (.2, .5, .8, 1.1):
            arcade.after_cancel(arcade.animation_timer)
            with patch('mini_games_ui.monotonic', return_value=start + duration * fraction):
                arcade.animation_frame()
        self.assertIsNone(arcade.animation)
        self.assertIsNone(arcade.animation_timer)

    def test_all_games_animate_and_clean_up(self):
        arcade = self.arcade
        for name in ('Connect 4', 'Tetris', 'Blackjack', 'Snake', 'Pong', '2048'):
            arcade.open(name)
            if name == '2048':
                arcade.model.board = [[2, 2, 2, 2]] + [[0] * 4 for _ in range(3)]
                arcade.action('left')
                board = [row[:] for row in arcade.model.board]
                arcade.action('down')
                self.assertEqual(board, arcade.model.board)
            elif name == 'Connect 4':
                arcade.action('4')
            elif name == 'Blackjack':
                arcade.model.result = ''
                arcade.model.player = [(10, 'S'), (7, 'S')]
                arcade.model.dealer = [(10, 'H'), (6, 'H')]
                arcade.model.deck = [(3, 'S')]
                arcade.action('stand')
            else:
                arcade.paused = False
                arcade.tick()
                arcade.cancel_timer()
            self.finish_frames()
            arcade.menu()
            self.assertIsNone(arcade.animation_timer)
        arcade.open('Connect 4')
        arcade.action('4')
        arcade.menu()
        self.assertIsNone(arcade.animation_timer)
        arcade.open('2048')
        arcade.model.board = [[0, 2, 0, 0]] + [[0] * 4 for _ in range(3)]
        arcade.action('left')
        arcade.open('2048', restart=True)
        self.assertIsNone(arcade.animation_timer)
        arcade.action('right')
        arcade.destroy()
        self.root.update()


if __name__ == '__main__':
    unittest.main()
