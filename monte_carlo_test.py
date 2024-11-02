import unittest
import numpy as np
import pandas as pd
from classes import Die 
from classes import Game
from classes import Analyzer

class MonteCarloTestSuite(unittest.TestCase):

    def test_die_constructor(self):

        self.assertRaises(TypeError, Die, ['one','two'])
        self.assertRaises(TypeError, Die, np.array([True,True,False]))
        self.assertRaises(ValueError, Die, np.array(['one','one','two']))
        
        die1 = Die(np.array([1,2,3,4,5,6]))

        self.assertEqual(die1.face_weights.shape,(6,1))
        self.assertIsInstance(die1.face_weights, pd.DataFrame)

    def test_change_face_weight(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        
        self.assertRaises(IndexError, die1.change_face_weight, 10,4.1)
        self.assertRaises(TypeError, die1.change_face_weight, 2, 'two')
        self.assertRaises(ValueError, die1.change_face_weight, 2,-1)

        die1.change_face_weight(1,10.0)

        self.assertEqual(die1.face_weights.iloc[0,0], 10.0)

    def test_roll_die(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        
        results = die1.roll_die(5)

        self.assertTrue(len(results) == 5)
        self.assertIn(results[4],[1,2,3,4,5,6])

    def test_show_face_weights(self):
        die1 = Die(np.array([1,2,3,4,5,6]))

        self.assertEqual(die1.show_face_weights().shape,(6,1))
        self.assertIsInstance(die1.show_face_weights(), pd.DataFrame)
    
    def test_game_constructor(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        die2 = Die(np.array(['red','blue','yellow']))

        self.assertRaises(ValueError, Game, 'not a list')
        self.assertRaises(ValueError, Game, ['something',die1])

        newgame = Game([die1,die2])

        self.assertIsInstance(newgame, Game)

    def test_play(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        die2 = Die(np.array(['red','blue','yellow']))
        newgame = Game([die1,die2])
        newgame.play(5)

        self.assertEqual(newgame.game.shape, (5,2))
        self.assertIsInstance(newgame.game, pd.DataFrame)
        self.assertIn(newgame.game.iloc[0,1], ['red','blue','yellow'])

    def test_show_results(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        die2 = Die(np.array(['red','blue','yellow']))
        newgame = Game([die1,die2])
        newgame.play(5)

        self.assertRaises(ValueError, newgame.show_result, 'either')

        wide = newgame.show_result()
        narrow = newgame.show_result('narrow')

        self.assertIsInstance(wide, pd.DataFrame)
        self.assertEqual(wide.shape, (5,2))
        self.assertEqual(narrow.shape, (10,))

    def test_analyzer_constructor(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        die2 = Die(np.array(['red','blue','yellow']))
        newgame = Game([die1,die2])
        newgame.play(5)

        self.assertRaises(ValueError, Analyzer, die1)

        a1 = Analyzer(newgame)

        self.assertIsInstance(a1, Analyzer)

    def test_jackpot(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        die2 = Die(np.array([1,2,3,4,5,6]))
        newgame = Game([die1,die2])
        newgame.play(5)
        a1 = Analyzer(newgame)

        self.assertIsInstance(a1.jackpot(), np.number)
        self.assertLessEqual(a1.jackpot(), 5)

        die3 = Die(np.array([1]))
        newgame2 = Game([die3,die3])
        newgame2.play(10)
        a2 = Analyzer(newgame2)

        self.assertEqual(a2.jackpot(), 10)

        die4 = Die(np.array([2,3]))
        newgame3 = Game([die3, die4])
        newgame3.play(4)
        a3 = Analyzer(newgame3)

        self.assertEqual(a3.jackpot(), 0)

    def test_face_counts(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        newgame = Game([die1,die1])
        newgame.play(100)

        a1 = Analyzer(newgame)

        self.assertIsInstance(a1.face_counts(), pd.DataFrame)
        self.assertEqual(a1.face_counts().shape, (100,6))

    def test_combination_count(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        newgame = Game([die1,die1])
        newgame.play(1000)

        a1 = Analyzer(newgame)
        combos = a1.combination_count()

        self.assertIsInstance(combos, pd.DataFrame)
        self.assertLessEqual(len(combos), 21)

    def test_permutation_count(self):
        die1 = Die(np.array([1,2,3,4,5,6]))
        newgame = Game([die1,die1])
        newgame.play(1000)

        a1 = Analyzer(newgame)
        permos = a1.permutation_count()

        self.assertIsInstance(permos, pd.DataFrame)
        self.assertLessEqual(len(permos), 36)

if __name__ == '__main__':
    unittest.main(verbosity=3)