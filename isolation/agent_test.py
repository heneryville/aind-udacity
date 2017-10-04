"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
import timeit

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

    def test_minimax_no_moves(self):
        self.player1 = game_agent.MinimaxPlayer(1, left_and_uppermost,0)
        self.player2 = "Player 2"
        self.game = isolation.Board(self.player1, self.player2, 1,1)
        self.game._board_state[0] = 'X'
        move = self.player1.get_move(self.game,always_time_left)
        self.assertEqual(move,(-1,-1))

    def test_minimax_can_forecast_single_move(self):
        """This scenario gives the game agent only one place to start where he'll have a future move."""
        self.player1 = "Player 1"
        self.player2 = game_agent.MinimaxPlayer(3, most_moves,0)
        self.game = isolation.Board(self.player1, self.player2, 3,2)
        self.game._board_state[5] = 'X'
        self.game.apply_move((1,1))
        move = self.player2.get_move(self.game,always_time_left)
        self.assertEqual(move,(1,0))

class AlphaBetaTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)

    def test_alpha_beta_can_forecast_single_move(self):
        self.player1 = "Player 1"
        self.player2 = game_agent.AlphaBetaPlayer(3, most_moves,1)
        self.player2.debug = True
        self.game = isolation.Board(self.player1, self.player2, 7,7)
        self.game.apply_move((0,0))
        start = timeit.default_timer()
        move = self.player2.get_move(self.game,timer(10))
        end = timeit.default_timer()
        print(end-start)
        self.assertTrue( (end-start) < 10)
        self.assertEqual(move,(2,2))

    """
    def test_alpha_beta_can_prune(self):
        self.player1 = game_agent.ImprovedAlphaBetaPlayer(3, most_moves,4)
        self.player2 = game_agent.AlphaBetaPlayer(1, most_moves,4)
        self.game = isolation.Board(self.player1, self.player2, 7,7)
        self.game.apply_move((0,0))
        self.game.apply_move((6,6))
        self.player1.get_move(self.game,timer(200))
    """

    def test_alpha_beta_can_play_full_if_stupid_game_where_player_2_thinks_harder(self):
        self.player1 = game_agent.AlphaBetaPlayer(3, most_moves,4)
        self.player2 = game_agent.AlphaBetaPlayer(1, most_moves,4)
        self.game = isolation.Board(self.player1, self.player2, 7,7)
        winner, moves,reason = self.game.play(120)
        if reason == 'forfeit':
            print('Game ended in forfeit for', 'Player 1' if self.game.active_player else 'Player 2')
            print('Legal moves',self.game.get_legal_moves())
            print(self.game.to_string())
            self.fail('Game ended in illegal move')
        print(self.game.to_string())
        print(winner == self.player1, moves,reason)
        self.assertTrue(len(moves)>0)
        self.assertEqual(reason,'illegal move')

def timer(time_limit):
    time_millis = lambda: 1000 * timeit.default_timer()
    move_start = time_millis()
    def time_left():
        return time_limit - (time_millis() - move_start)
    return time_left

def always_time_left():
    return 1000
      

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
    #unittest.main()
    test = AlphaBetaTest()
    #test.test_alpha_beta_can_prune()
    test.test_alpha_beta_can_forecast_single_move()
