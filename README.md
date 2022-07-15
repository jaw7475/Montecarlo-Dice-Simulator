# Montecarlo-Dice-Simulator

## Metadata
Project: Monte Carlo Simulator \
Author: Jake Weinberg

## Synopsis

### Installing
1. `git clone` repo found at https://github.com/jaw7475/Montecarlo-Dice-Simulator/
2. Through the console: `pip install .`

### Importing
1. To import entire package: `import montecarlo.montecarlo`
2. To import specific classses: `from montecarlo.montecarlo import Die, Game, Analyzer`

### Creating a Die

To initialize:
``` python
example_die = Die(np.array([1,2,3,4,5,6]))
```
Dice are initialized by passing an ndarray of numbers or strings.

### Creating a Game

To initialize:
``` python
dielist = [die1, die2, die3]
example_game = Game(dielist)
```
Games are initialized by passing a list of already initialized Dice.

### Creating an Analyzer
To initialize:

``` python
example_analyzer = Analyzer(test_game)
```
Analyzers are initialized by passing an already initialized Game.

## API Description

### Class Die

Docstring:

    A Die object has N sides, or “faces”, and W weights, and can be rolled to select a face. 

    W defaults to 1.0 for each face but can be changed after the object is created.
    
    Note that the weights are just numbers, not a normalized probability distribution.
    
    The die has one behavior, which is to be rolled one or more times.
    
    Note that what we are calling a “die” here can be any discrete random variable associated with a stochastic process, 
    such as using a deck of cards or flipping a coin or speaking a language. Our probability model for such variable is, 
    however, very simple – since our weights apply to only to single events, we are assuming that the events are 
    independent. This makes sense for coin tosses but not for language use.
    
#### Methods:
``` python
__init__(self, faces):
```
    PURPOSE: Initializes an instance of the Die object. Internally initializes the weights to 1.0 for each face. 
    Saves both faces and weights into a private dataframe that is to be shared by the other methods.
        
    INPUTS: Takes an ndarray of faces as an argument. The array's data type (dtype) may be strings or numbers
        
    OUTPUTS: None

```python
change_weight(self, face, weight):
```
    PURPOSE: Changes the weight of a single side. Checks to see if the face passed is valid; is it in the array of weights?
    Checks to see if the weight is valid; is it a float? Can it be converted to one?
        
    INPUTS: Takes two arguments: the face value to be changed and the new weight. The new weight must be a float.
        
    OUTPUTS: None
    
```python
die_roll(self, rolls = 1):
```
    PURPOSE: A method to roll the die one or more times.
        
    INPUTS: Takes a parameter of how many times the die is to be rolled as an int; defaults to 1.
        
    OUTPUTS: Returns a list of outcomes. Does not internally store this list.
    
```python
get_die(self):
```
    PURPOSE: A method to show the user the die’s current set of faces and weights (since the latter can be changed).
        
    INPUTS: None
        
    OUTPUTS: Returns the dataframe created in the initializer.
    
#### Parameters:
`faces` ndarray of numbers or strings; required parameter for initialization; represents faces of dice\
`weights` ndarray of floats; probabilisitic weights that correspond to each face of the die; default = 1.0 for each\

### Game

Docstring:

    A Game object consists of rolling of one or more dice of the same kind one or more times. 

    Each game is initialized with one or more of similarly defined dice (Die objects).
    
    By “same kind” and “similarly defined” we mean that each die in a given game has the same number of sides and 
    associated faces, but each die object may have its own weights.
    
    The class has a behavior to play a game, i.e. to rolls all of the dice a given number of times.
    
    The class keeps the results of its most recent play. 
    
#### Methods

```python
__init__(self, dice):
```
    PURPOSE: Initializes a Game object.
        
    INPUTS: Takes a single parameter, a list of already instantiated similar Die objects.
        
    OUTPUTS: None
    
```python
play(self, num_times):
```
    PURPOSE: Plays a game by simulating rolls of its dice a given number of times. Saves the result of the play to a 
    private dataframe of shape N rolls by M dice.
        
    INPUTS: Takes an int that specifies how many times the dice should be rolled.
        
    OUTPUTS: None
    
```python
show(self, stack = 'wide')
```
    PURPOSE: A method to show the user the results of the most recent play. This method  passes the private dataframe 
    created in play() to the user.
        
    INPUTS: Takes a string parameter "narrow" or "wide" that determines the form that the dataframe is returned. An 
    exception will be thrown if a different parameter is passed. Defaults to "wide"
        
    OUTPUTS: Returns a dataframe of the results of play(). The narrow form of the dataframe will have a two-column index 
    with the roll number and the die number, and a column for the face rolled. The wide form of the dataframe will a 
    single column index with the roll number, and each die number as a column.

#### Parameters
`dice` list of dice objects in game; required for initialization

### Analyzer

Docstring:

    An Analyzer object takes the results of a single game and computes various descriptive statistical properties about it. 
    These propertiesresults are available as attributes of an Analyzer object. Attributes (and associated methods) include:

    A face counts per roll, i.e. the number of times a given face appeared in each roll. For example, if a roll of five 
    dice has all sixes, then the counts for this roll would be 6 for the face value '6' and 0 for the other faces.
    
    A jackpot count, i.e. how many times a roll resulted in all faces being the same, e.g. all one for a six-sided die.
    
    A combo count, i.e. how many combination types of faces were rolled and their counts.
    
#### Methods

```python
__init__(self, game):
```
    PURPOSE: Initializes an instance of an Analyzer object. At initialization time, it also infers the data type of the 
    die faces used.
        
    INPUTS: Takes a game object as its input parameter.
        
    OUTPUTS: None
    
```python
jackpot(self):
```
    PURPOSE: A method to compute how many times the game resulted in all faces being identical. Stores the results as 
    a dataframe of jackpot results in a public attribute, jackpots. The dataframe has the roll number as a named index.
        
    INPUTS: None
        
    OUTPUTS: Returns an integer for the number times to the user.
    
```python
combo(self)
```
    PURPOSE: A method to compute the distinct combinations of faces rolled, along with their counts. Combinations are 
    sorted and saved as a multi-columned index. Stores the results as a dataframe in a public attribute, combinations.
        
    INPUTS: None
        
    OUTPUTS: None

```python
face_counts_per_roll(self):
```
    PURPOSE: A method to compute how many times a given face is rolled in each event. Stores the results as a dataframe 
    in a public attribute. The dataframe has an index of the roll number and face values as columns (i.e. it is in 
    wide format).
        
    INPUTS: None
        
    OUTPUTS: None

#### Parameters
`game` game object; required as paramenter during initialization\
`face_type` variable type of dice faces used to play the game object passed to the analyzer\
`jackpots` dataframe of all rolls in game that were jackpot results (all faces were identical)\
`combinations` dataframe with multi-indexed columns that stores all of the diffrent roll combinations from the game\
`face_counts` dataframe that shows how many of each face were rolled for each roll event in the game\

## Manifest

- Montecarlo-Dice-Simulator/
  - docs/
  - LICENSE.txt
  - README.txt
  - montecarlo_demo.ipynb
  - montecarlo_test_results.txt
  - setup.py
  - montecarlo/
    - \__init__.py
    - montecarlo.py
    - montecarlo_tests.py
