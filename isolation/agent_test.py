"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class MinimaxTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)

    def test_minimax_starts_ul(self):
        self.player1 = game_agent.MinimaxPlayer(1, left_and_uppermost,0)
        self.player2 = "Player 2"
        self.game = isolation.Board(self.player1, self.player2, 3,3)
        move = self.player1.get_move(self.game,always_time_left)
        self.assertEqual(move,(0,0))

    def test_minimax_can_forecast_single_move(self):
        """This scenario gives the game agent only one place to start where he'll have a future move."""
        self.player1 = "Player 1"
        self.player2 = game_agent.MinimaxPlayer(3, most_moves,0)
        self.game = isolation.Board(self.player1, self.player2, 3,2)
        self.game._board_state[5] = 'X'
        self.game.apply_move((1,1))
        move = self.player2.get_move(self.game,always_time_left)
        self.assertEqual(move,(1,0))

def always_time_left():
    return 100

def left_and_uppermost(game,player):
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    y, x = game.get_player_location(player)
    return -float(y**2 + x**2)

def most_moves(game,player):
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    return len(game.get_legal_moves(player))

if __name__ == '__main__':
    unittest.main()
