# Montecarlo-Dice-Simulator

## Metadata
Project: Monte Carlo Simulator \
Author: Jake Weinberg

## Synopsis

### Installing
1. `git clone` repo found at https://github.com/jaw7475/Montecarlo-Dice-Simulator/
2. Through the console: `pip install .`

### Importing
1. To import entire package: `import montecarlo`
2. To import specific classses: `from montecarlo import Die, Game, Analyzer`

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
