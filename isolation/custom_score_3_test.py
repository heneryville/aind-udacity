import unittest

import isolation
import game_agent
import timeit

from importlib import reload

class CustomScore3Test(unittest.TestCase):
    def test_it_finds_weights(self):
        player1 = "Player 1"
        player2 = "Player 2"
        game = isolation.Board(player1, player2, 4,4)
        game.apply_move((1,0))
        game.apply_move((3,0))
        """
         |1| |
        --------
         |O| |X
        --------
        X| |B|
        --------
        2| | |
        """
        # 2 + 2 + 2 = 6 moves from moves for one
        # 3 + 2 = 5 moves from moves for two
        score_for_one = game_agent.custom_score_3(game,player1)
        self.assertEqual(score_for_one,6/6)

if __name__ == '__main__':
    unittest.main()
