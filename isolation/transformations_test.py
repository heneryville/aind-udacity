import unittest

import isolation

from importlib import reload

class TransformationsTest(unittest.TestCase):

    def test_it_can_find_itself_in_dict(self):
        game1 = isolation.Board('p1','p2', 4,4)
        game1.apply_move((1,1))
        game1.apply_move((2,1))

        game2 = game1.copy()

        game3 = game1.copy()
        game3.apply_move((3,2))

        dictionary = {}
        dictionary[game1] = 123
        self.assertEqual(dictionary[game1],123)

    def test_it_can_find_identical_in_dict(self):
        game1 = isolation.Board('p1','p2', 4,4)
        game1.apply_move((1,1))
        game1.apply_move((2,1))

        game2 = game1.copy()

        game3 = game1.copy()
        game3.apply_move((3,2))

        dictionary = {}
        dictionary[game1] = 123
        self.assertEqual(dictionary[game2],123)

    def test_it_cannot_find_different_in_dict(self):
        game1 = isolation.Board('p1','p2', 4,4)
        game1.apply_move((1,1))
        game1.apply_move((2,1))

        game2 = game1.copy()

        game3 = game1.copy()
        game3.apply_move((3,2))

        dictionary = {}
        dictionary[game1] = 123
        self.assertFalse(game3 in dictionary)

    def test_index_to_loc(self):
        game = isolation.Board("player1", "player2", 4,4)
        self.assertEqual(game.indexToLoc(0),(0,0))
        self.assertEqual(game.indexToLoc(1),(1,0))
        self.assertEqual(game.indexToLoc(2),(2,0))
        self.assertEqual(game.indexToLoc(3),(3,0))
        self.assertEqual(game.indexToLoc(4),(1,1))
        self.assertEqual(game.indexToLoc(5),(1,2))
        

    def test_it_rotates(self):
        player1 = "Player 1"
        player2 = "Player 2"
        game = isolation.Board(player1, player2, 4,4)
        game.set((0,0),1)
        game.set((3,0),2)
        game.set((0,3),3)
        game.set((3,3),4)
        rotated = game.rotate90()
        self.assertEqual(rotated.get((0,0)),2)
        self.assertEqual(rotated.get((3,0)),4)
        self.assertEqual(rotated.get((0,3)),1)
        self.assertEqual(rotated.get((3,3)),3)
        
        """
        TODO: Transform where the players are too
        TODO: Can this be faster?
        """

if __name__ == '__main__':
    unittest.main()
