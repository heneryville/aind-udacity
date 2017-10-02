import unittest

import isolation
import game_agent
from reachability import *

from importlib import reload

class ReachabilityTest(unittest.TestCase):

    def test_it_finds_reachability_on_open_board(self):
        player1 = "Player 1"
        player2 = "Player 2"
        game = isolation.Board(player1, player2, 4,4)
        """
        3|X|3|2
        --------
        2|3|2|1
        --------
        1|2|1|4
        --------
        2|3|2|3
        """
        reachables = reachability(game,(0,1))
        self.assertEqual([p[0] for p in reachables.pairs()],[3,2,1,2,0,3,2,3,3,2,1,2,2,1,4,3])

    def test_it_finds_reachability_on_open_board_another_position(self):
        player1 = "Player 1"
        player2 = "Player 2"
        game = isolation.Board(player1, player2, 4,4)
        game.set((0,1),'A')
        """
        5|A|3|2
        --------
        2|1|4|3
        --------
        3|4|1|2
        --------
        B|3|2|5
        """
        reachables = reachability(game,(3,0))
        self.assertEqual([p[0] for p in reachables.pairs()],[5,2,3,0,float("inf"),1,4,3,3,4,1,2,2,3,2,5])

    def test_it_gives_inf_on_unreachables(self):
        player1 = "Player 1"
        player2 = "Player 2"
        game = isolation.Board(player1, player2, 4,4)
        game.set((1,1),'/')
        game.set((2,2),'/')
        """
        3|X|3|∞
        --------
        4|/|2|1
        --------
        1|2|/|4
        --------
        ∞|3|2|3
        """
        reachables = reachability(game,(0,1))
        self.assertEqual([p[0] for p in reachables.pairs()],[3,4,1,float("inf"),0,float("inf"),2,3,3,2,float("inf"),2,float("inf"),1,4,3])

    def test_it_finds_oppossible_reachability(self):
        player1 = "Player 1"
        player2 = "Player 2"
        game = isolation.Board(player1, player2, 4,4)
        """
        Reach for A
        3|A|3|2
        --------
        2|3|2|1
        --------
        1|2|1|4
        --------
        B|3|2|3

        Reach for B
        5|A|3|2
        --------
        2|1|4|3
        --------
        3|4|1|2
        --------
        B|3|2|5

        Combined
        3|A | 3|2
        ----------
        2|-1| 2|1
        ----------
        1| 2| 1|-2
        ----------
        B| 3|-1|3
        """
        reachables = opposed_reachability(game,(0,1),(3,0))
        self.assertEqual([p[0] for p in reachables.pairs()],[3,2,1,0,0,-1,2,3,3,2,1,2,2,1,-2,3])

    def vest_it_runs_in_realistic_time(self):
        player1 = "Player 1"
        player2 = "Player 2"
        size_x = 1000
        size_y = 100
        game = isolation.Board(player1, player2, size_x,size_y)
        reachables = reachability(game,(0,1))

if __name__ == '__main__':
    unittest.main()
