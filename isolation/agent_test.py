"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_minimax(self):
        self.player1 = game_agent.MinimaxPlayer(1, left_and_uppermost,0)
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
        self.player1.get_move(self.game,always_time_left)


def always_time_left():
    return 100

def left_and_uppermost(game,player):
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")
    y, x = game.get_player_location(player)
    return float(y**2 + x**2)



if __name__ == '__main__':
    unittest.main()
