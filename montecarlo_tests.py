import unittest
import pandas as pd
import numpy as np
from montecarlo import Die, Game, Analyzer

class MontecarloTestSuite(unittest.TestCase):
    '''
    This is a suite of tests intended to ensure the functionality of the montecarlo module. Methods (tests) include:
        test_01_change_weight()
        test_02_die_roll()
        test_03_get_die()
        test_04_play()
        test_05_show()
        test_06_jackpot()
        test_07_combos()
        test_08_face_counts_per_roll()
    '''
    
    def test_01_change_weight(self):
        '''
        PURPOSE: This function tests the change_weight() function of the montecarlo.Die class by testing that both the
        weights and private opportunity set attributes are correctly changed by the function
        '''
        test_die = Die(np.array([1,2,3,4,5,6]))
        test_die.change_weight(2, 5.0)
        
        self.assertTrue(test_die.weights[1] == 5.0 and test_die._opportunity_set.loc[1][1] == 5.0)
    
    def test_02_die_roll(self):
        '''
        PURPOSE: This function tests the die_roll() function of the montecarlo.Die class by testing that the length of the list
        returned by the function is the same length as the number of rolls instructed
        '''
        test_die = Die(np.array([1,2,3,4,5,6]))
        test_result = test_die.die_roll(15)
        
        self.assertTrue(len(test_result) == 15)
        
    def test_03_get_die(self):
        '''
        PURPOSE: This function tests the get_die() function of the montecarlo.Die class by testing that select observations in
        the dataframe returned by the function are as expected
        '''        
        test_die = Die(np.array([1,2,3,4,5,6]))
        test_result = test_die.get_die()
        
        self.assertTrue(test_result.loc[3][0] == 4 and test_result.loc[3][1] == 1)
        
    def test_04_play(self):
        '''
        PURPOSE: This function tests the play() function of the montecarlo.Game class by testing that the size of the
        private dataframe is as expected given the number of die (3) and the number of rolls (20)
        '''
        die1 = Die(np.array([1,2,3,4,5]))
        die2 = Die(np.array([1,2,3,4,5]))
        die3 = Die(np.array([1,2,3,4,5]))
        dielist = [die1, die2, die3]
        
        test_game = Game(dielist)
        
        test_game.play(20)
        
        self.assertTrue(len(test_game._result) == 20 and len(test_game._result.columns) == 3)
        
    def test_05_show(self):
        '''
        PURPOSE: This function tests the show() function of the montecarlo.Game class by testing that the size of the dataframe
        returned with the narrow input parameter is stacked as expected
        '''
        die1 = Die(np.array([1,2,3,4,5]))
        die2 = Die(np.array([1,2,3,4,5]))
        die3 = Die(np.array([1,2,3,4,5]))
        dielist = [die1, die2, die3]
        
        test_game = Game(dielist)
        test_game.play(20)
        test_result = test_game.show('narrow')
        
        self.assertTrue(len(test_result) == (3*20) and len(test_result.columns) == 1)
        
    def test_06_jackpot(self):
        '''
        PURPOSE: This function tests the jackpot() function of the montecarlo.Analyzer class by testing that the integer returned
        is equal to the number of jackpots in a game
        '''
        die1 = Die(np.array([1,2,3,4,5]))
        die2 = Die(np.array([1,2,3,4,5]))
        die3 = Die(np.array([1,2,3,4,5]))
        dielist = [die1, die2, die3]
        
        test_game = Game(dielist)
        test_game.play(5)
        test_game._result.loc[0] = [5,5,5]
        test_game._result.loc[1] = [5,5,5]
        test_game._result.loc[2] = [1,5,5]
        test_game._result.loc[3] = [1,2,5]
        test_game._result.loc[4] = [4,3,5]
        
        test_analyzer = Analyzer(test_game)
        test_jackpots = test_analyzer.jackpot()
        
        self.assertTrue(test_jackpots == 2)
        
    def test_07_combos(self):
        '''
        PURPOSE: This function tests the combos() function of the montecarlo.Analyzer class by testing that the number of combinations
        found is equal to the true number of combinations in a game
        '''
        die1 = Die(np.array([1,2,3,4,5]))
        die2 = Die(np.array([1,2,3,4,5]))
        die3 = Die(np.array([1,2,3,4,5]))
        dielist = [die1, die2, die3]
        
        test_game = Game(dielist)
        test_game.play(5)
        test_game._result.loc[0] = [5,5,5]
        test_game._result.loc[1] = [5,5,5]
        test_game._result.loc[2] = [1,5,5]
        test_game._result.loc[3] = [1,2,5]
        test_game._result.loc[4] = [4,3,5]
        
        test_analyzer = Analyzer(test_game)
        test_combos = test_analyzer.combo()
        
        self.assertTrue(len(test_analyzer.combinations) == 4)
        
    def test_08_face_counts_per_roll(self):
        '''
        PURPOSE: This function tests the face_counts_per_roll() function of the montecarlo.Analyzer class by testing that select
        observations of the returned data frame are equal to the expected face count tallies
        '''
        die1 = Die(np.array([1,2,3,4,5]))
        die2 = Die(np.array([1,2,3,4,5]))
        die3 = Die(np.array([1,2,3,4,5]))
        dielist = [die1, die2, die3]
        
        test_game = Game(dielist)
        test_game.play(5)
        test_game._result.loc[0] = [5,5,5]
        test_game._result.loc[1] = [5,5,5]
        test_game._result.loc[2] = [1,5,5]
        test_game._result.loc[3] = [1,2,5]
        test_game._result.loc[4] = [4,3,5]
        
        test_analyzer = Analyzer(test_game)
        test_analyzer.face_counts_per_roll()
        test_fc = test_analyzer.face_counts
        
        self.assertTrue(test_fc.loc[0][5] == 3 and test_fc.loc[4][1] == 0)
        
if __name__ == '__main__':
    
    unittest.main(verbosity=3)