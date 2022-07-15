import numpy as np
import pandas as pd

class Die:
    '''
    A Die object has N sides, or “faces”, and W weights, and can be rolled to select a face. 

    W defaults to 1.0 for each face but can be changed after the object is created.
    
    Note that the weights are just numbers, not a normalized probability distribution.
    
    The die has one behavior, which is to be rolled one or more times.
    
    Note that what we are calling a “die” here can be any discrete random variable associated with a stochastic process, such as using
    a deck of cards or flipping a coin or speaking a language. Our probability model for such variable is, however, very simple – since
    our weights apply to only to single events, we are assuming that the events are independent. This makes sense for coin tosses but
    not for language use.
    '''
    
    def __init__(self, faces):
        '''
        PURPOSE: Initializes an instance of the Die object. Internally initializes the weights to 1.0 for each face. Saves both 
        faces and weights into a private dataframe that is to be shared by the other methods.
        
        INPUTS: Takes an ndarray of faces as an argument. The array's data type (dtype) may be strings or numbers
        
        OUTPUTS: None
        '''
        self.faces = faces
        self.weights = np.ones_like(self.faces, dtype = np.float64)
        self._opportunity_set = pd.DataFrame({'faces':self.faces, 'weights':self.weights})
        
    def change_weight(self, face, weight):
        '''
        PURPOSE: Changes the weight of a single side. Checks to see if the face passed is valid; is it in the array of weights?
        Checks to see if the weight is valid; is it a float? Can it be converted to one?
        
        INPUTS: Takes two arguments: the face value to be changed and the new weight. The new weight must be a float.
        
        OUTPUTS: None
        '''
        if face in self.faces:
            if type(weight) == float:
                self._opportunity_set.loc[self._opportunity_set['faces'] == face, 'weights'] = weight
                self.weights = self._opportunity_set.weights
            else:
                return "Please enter a number with a decimal for the weight."
        else:
            return "Please enter a face on this die."
        
    def die_roll(self, rolls = 1):
        '''
        PURPOSE: A method to roll the die one or more times.
        
        INPUTS: Takes a parameter of how many times the die is to be rolled; defaults to 1.
        
        OUTPUTS: Returns a list of outcomes. Does not internally store this list.
        '''
        results = []
        probabilities = [x / sum(self.weights) for x in self.weights]
        
        for i in range(rolls):
            instance = self._opportunity_set.faces.sample(weights = probabilities).values[0]
            results.append(instance)
            
        return results
    
    def get_die(self):
        '''
        PURPOSE: A method to show the user the die’s current set of faces and weights (since the latter can be changed).
        
        INPUTS: None
        
        OUTPUTS: Returns the dataframe created in the initializer.
        '''
        df = self._opportunity_set.copy()
        return df
    
class Game:
    '''
    A Game object consists of rolling of one or more dice of the same kind one or more times. 

    Each game is initialized with one or more of similarly defined dice (Die objects).
    
    By “same kind” and “similarly defined” we mean that each die in a given game has the same number of sides and 
    associated faces, but each die object may have its own weights.
    
    The class has a behavior to play a game, i.e. to rolls all of the dice a given number of times.
    
    The class keeps the results of its most recent play. 
    '''
    
    def __init__(self, dice):
        '''
        PURPOSE: Initializes a Game object.
        
        INPUTS: Takes a single parameter, a list of already instantiated similar Die objects.
        
        OUTPUTS: None
        '''
        self.dice = dice
        
    def play(self, num_times):
        '''
        PURPOSE: Plays a game by simulating rolls of its dice a given number of times. Saves the result of the play to a 
        private dataframe of shape N rolls by M dice.
        
        INPUTS: Takes an int that specifies how many times the dice should be rolled.
        
        OUTPUTS: None
        '''
        self._result = pd.DataFrame()
        self._result.index.name = 'roll'
        self._result.columns.name = 'die'
        for i in range(len(self.dice)):
            self._result[i] = self.dice[i].die_roll(num_times)
        
    def show(self, stack = 'wide'):
        '''
        PURPOSE: A method to show the user the results of the most recent play. This method  passes the private dataframe created
        in play() to the user.
        
        INPUTS: Takes a string parameter "narrow" or "wide" that determines the form that the dataframe is returned. An exception
        will be thrown if a different parameter is passed. Defaults to "wide"
        
        OUTPUTS: Returns a dataframe of the results of play(). The narrow form of the dataframe will have a two-column index 
        with the roll number and the die number, and a column for the face rolled. The wide form of the dataframe will a 
        single column index with the roll number, and each die number as a column.
        '''
        assert (stack == 'wide' or stack == 'narrow'), "Please enter narrow or wide"
        df = self._result.copy()
        
        if stack == 'wide':
            return df
        else:
            df = df.stack().to_frame('faces rolled')
            return df
        
class Analyzer:
    '''
    An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it. 
    These properties results are available as attributes of an Analyzer object. Attributes (and associated methods) include:

    A face counts per roll, i.e. the number of times a given face appeared in each roll. For example, if a roll of five dice 
    has all sixes, then the counts for this roll would be 6 for the face value '6' and 0 for the other faces.
    
    A jackpot count, i.e. how many times a roll resulted in all faces being the same, e.g. all one for a six-sided die.
    
    A combo count, i.e. how many combination types of faces were rolled and their counts.
    '''
    
    def __init__(self, game):
        '''
        PURPOSE: Initializes an instance of an Analyzer object. At initialization time, it also infers the data type of the 
        die faces used.
        
        INPUTS: Takes a game object as its input parameter.
        
        OUTPUTS: None
        '''
        self.game = game
        self.face_type = game.dice[0].faces[0].dtype
        
    def jackpot(self):
        '''
        PURPOSE: A method to compute how many times the game resulted in all faces being identical. Stores the results as a 
        dataframe of jackpot results in a public attribute, jackpots. The dataframe has the roll number as a named index.
        
        INPUTS: None
        
        OUTPUTS: Returns an integer for the number times to the user.
        '''
        result = self.game.show('wide')
        jackpot_test = result.eq(result.iloc[:, 0], axis=0).all(1)
        
        jackpot_counter = 0
        jackpot_rolls = []
        self.jackpots = pd.DataFrame(columns = result.columns)
        self.jackpots.index.name = 'roll'
        
        for i in range(len(jackpot_test)):
            if jackpot_test.loc[i]:
                jackpot_counter += 1
                jackpot_rolls.append(i)
                self.jackpots.loc[len(self.jackpots)-1] = result.loc[i]
                
        self.jackpots.index = jackpot_rolls
        
        return jackpot_counter
            
    def combo(self):
        '''
        PURPOSE: A method to compute the distinct combinations of faces rolled, along with their counts. Combinations are sorted and 
        saved as a multi-columned index. Stores the results as a dataframe in a public attribute, combinations.
        
        INPUTS: None
        
        OUTPUTS: None
        '''
        self.combinations = self.game.show('wide')
        self.combinations = self.combinations.apply(lambda x: pd.Series(sorted(x)), 1).value_counts().to_frame('n')
        return
    
    def face_counts_per_roll(self):
        '''
        PURPOSE: A method to compute how many times a given face is rolled in each event. Stores the results as a dataframe in a public
        attribute. The dataframe has an index of the roll number and face values as columns (i.e. it is in wide format).
        
        INPUTS: None
        
        OUTPUTS: None
        '''
        self.face_counts = self.game.show('wide').apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)
