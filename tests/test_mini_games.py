import unittest
from unittest.mock import patch

import mini_games as g


class ArcadeRulesTests(unittest.TestCase):
    def test_connect_four_all_directions(self):
        for coords, final in (([(0, 5), (1, 5), (2, 5)], 3),
                              ([(0, 5), (0, 4), (0, 3)], 0),
                              ([(0, 5), (1, 4), (2, 3)], 3),
                              ([(0, 2), (1, 3), (2, 4)], 3)):
            game = g.Connect4()
            for x, y in coords: game.board[y][x] = 1
            if coords[1] == (1, 4):
                for y in (3, 4, 5): game.board[y][3] = 2
            game.drop(final, 1)
            self.assertEqual(game.result, 'You win!')
            self.assertFalse(game.drop(6, 2))

    def test_computer_blocks_and_wins(self):
        for player in (1, 2):
            game = g.Connect4()
            game.board[5][:3] = [player] * 3
            game.computer()
            self.assertEqual(game.board[5][3], 2)
            if player == 2: self.assertEqual(game.result, 'Computer wins!')

    def test_full_column_rejects_move(self):
        game = g.Connect4()
        for row in game.board: row[0] = 1
        self.assertFalse(game.drop(0, 1))

    def test_2048_merges_once_and_counts_score(self):
        self.assertEqual(g.merge_line([2, 2, 2, 2]), ([4, 4, 0, 0], 8))
        self.assertEqual(g.merge_line([4, 0, 4, 8]), ([8, 8, 0, 0], 8))
        for direction in ('left', 'right', 'up', 'down'):
            game = g.Tiles2048()
            game.board = [[2] * 4 for _ in range(4)]
            with patch.object(game, 'spawn') as spawn:
                self.assertTrue(game.move(direction))
                self.assertEqual(game.score, 32)
                spawn.assert_called_once()

    def test_2048_no_op_and_loss(self):
        game = g.Tiles2048()
        game.board = [[2, 4, 2, 4], [4, 2, 4, 2]] * 2
        with patch.object(game, 'spawn') as spawn:
            self.assertFalse(game.move('left'))
            spawn.assert_not_called()
        self.assertTrue(game.over)

    def test_snake_growth_reverse_and_wall(self):
        game = g.Snake()
        game.food = (10, 10)
        game.turn((-1, 0))
        game.step()
        self.assertEqual(game.score, 10)
        self.assertEqual(len(game.body), 4)
        self.assertNotIn(game.food, game.body)
        for _ in range(20): game.step()
        self.assertTrue(game.over)

    def test_snake_can_enter_departing_tail(self):
        game = g.Snake()
        game.body = [(1, 1), (1, 2), (0, 2), (0, 1)]
        game.direction = game.pending = (-1, 0)
        game.food = (5, 5)
        game.step()
        self.assertFalse(game.over)

    def test_tetris_clear_and_top_out(self):
        game = g.Tetris()
        game.board[-1] = [1] * 6 + [0] * 4
        game.piece = list(g.SHAPES[0])
        game.kind, game.x, game.y = 0, 6, 18
        game.step()
        self.assertEqual(game.lines, 1)
        self.assertEqual(game.score, 100)
        game.board = [[1] * 10 for _ in range(20)]
        game.spawn()
        self.assertTrue(game.over)

    def test_tetris_bag_and_rotation(self):
        game = g.Tetris()
        self.assertEqual(set([game.kind, game.next] + [game.take() for _ in range(5)]), set(range(7)))
        game.kind, game.piece, game.x, game.y = 2, list(g.SHAPES[2]), 3, 3
        original = set(game.piece)
        for _ in range(4): game.rotate()
        self.assertEqual(set(game.piece), original)

    def test_blackjack_aces_and_dealer_stands_soft_17(self):
        self.assertEqual(g.hand_value([(1, 'S'), (1, 'H'), (9, 'S')]), 21)
        game = g.Blackjack()
        game.result = ''
        game.player, game.dealer = [(10, 'S'), (8, 'S')], [(1, 'H'), (6, 'H')]
        game.stand()
        self.assertEqual(len(game.dealer), 2)
        self.assertEqual(game.result, 'You win!')

    def test_blackjack_bust_and_naturals(self):
        game = g.Blackjack()
        game.result = ''
        game.player = [(10, 'S'), (9, 'S')]
        game.deck = [(5, 'S')]
        game.hit()
        self.assertEqual(game.result, 'Bust! Dealer wins.')
        # Pop order: player ace/king, dealer ace/queen.
        def deck_order(deck): deck[:] = [(12, 'H'), (1, 'H'), (13, 'S'), (1, 'S')]
        with patch.object(g.random, 'shuffle', deck_order):
            self.assertEqual(g.Blackjack().result, 'Push — both have Blackjack.')

    def test_pong_bounce_score_and_finish(self):
        game = g.Pong()
        game.x, game.y, game.vx, game.vy = 30, 200, -4, 0
        game.step()
        self.assertGreater(game.vx, 0)
        game.scores = [6, 0]
        game.x, game.y, game.vx = 399, 20, 4
        game.step()
        self.assertEqual(game.scores, [7, 0])
        self.assertTrue(game.over)


if __name__ == '__main__':
    unittest.main()
