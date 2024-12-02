# ds5100_final_project

# Metadata

Author: Jack Burke
Project: Monte Carlo Simulator

# Synopsis

The Monte Carlo Simulator consists of three classes: **Die**, **Game**, and **Analyzer**, which allow the user to implement a simple [monte carlo simulator](https://en.wikipedia.org/wiki/Monte_Carlo_method). Game objects are initialized with a Die object, and Analyzer objects are initialized with a Game object. A Die can be any discrete random variable associated with a stochastic process, such as using a deck of cards, flipping a coin, rolling an actual die, or speaking a language.

## Installing Monte Carlo Simulator

Download files from the project [github repository](https://github.com/jackburke12/ds5100_final_project.git).
Navigate to the project directory and run the following in a terminal:
```
pip install .
```
Once the package is installed, you can import the die, game and analyzer classes like so:
```
from monte_carlo.monte_carlo_simulator import Die, Game, Analyzer
```
Use help() to view class descriptions and methods:
```
help(Die)
```

## Creating Dice

A die object can be created by passing a numpy array of strings or numbers. Note that all faces must be unique. Face weights are initialized to 1.0, and can be modified using the change_face_weight() method. 

```
#Standard 6-sided die
6_sided_die = Die(np.array([1,2,3,4,5,6))

#Standard coin
coin = Die(np.array(["Heads","Tails"])

#Loaded die - make 6s five times more likely to be rolled
loaded_die = Die(np.array([1,2,3,4,5,6]))
loaded_die.change_face_weight(6, 5.0)
```
Show the face weights:
```
loaded_die.show_face_weights()
```
Once your dice are created, you can roll them a specified number of times and return a list of the results:
```
print(coin.roll_die(10))
```

## Playing a Game

A Game can be played by passing a list of Die objects to Game:
```
mygame = Game([6_sided_die, 6_sided_die])
```
Using the Play method will roll the dice for a specified number of times. If no number of rolls is specified, the dice will be rolled once. show_result()
will show the results of the last game played in wide format. Pass the argument 'narrow' to show_result() to return the results in narrow format.
```
mygame.play(5)
mygame.show_result()
```

## Analyzing games

Create an analyzer to review the results of the last game in detail:
```
a1 = Analyzer(mygame)
```
Use analyzer methods to count jackpots, number of times each face was rolled, unique combinations rolled, and unique permutations rolled:
```
print(a1.jackpot())
print(a1.face_counts())
print(a1.combination_count())
print(a1.permutation_count())
```

# API Description

```
class Die
    A class to create a die with customizable faces and weights. This die can be rolled, and each face has a weight 
    that affects the likelihood of it appearing in a roll. Faces can be strings or numbers, and weights can be positive 
    numbers, including zero. Weights default to 1 if not specified.

    __init__(faces)
        PURPOSE: Create a die object with any number of faces.
        INPUTS: 
        faces: numpy array containing strings or numpy array containing numbers

        OUTPUTS:
        face_weights: dataframe containing the weight for each face on the die.

        RETURNS:
        none
        
    change_face_weight(face, weight)
        PURPOSE: Customize the weights of the faces on an existing die object.

        INPUTS: 
        face: string or int. Will raise IndexError if the face provided is not present in the die's index of faces.
        weight: float or int. Must be positive.

        OUTPUTS:
        Changes the face_weights attribute to reflect the inputted weight.

        RETURNS:
        none
        
    roll_die(num_rolls = 1)
        PURPOSE: Roll the die the specified number of times and return the results of the rolls. For example, if a standard six-sided die was rolled 3 times, the output could look like this: [2,4,3].

        INPUTS: 
        num_rolls: int

        RETURNS:
        rolls: list of strings or integers
        
    show_face_weights()
        
        PURPOSE: Show the weights for each face on the die.

        INPUTS:
        none

        RETURNS:
        face_weights: Dataframe with 'faces' as the index and 'weights' as a column of floats
        
class Game
    Represents a game played with multiple dice. Each die is rolled simultaneously for a specified
    number of rolls. The results are stored and can be presented in either a wide or narrow format.

    __init__(dice)
           
        PURPOSE: Create a game object with a list of dice.

        INPUTS: 
        dice: list of dice objects

        RETURNS: 
        none
     
    play(num_rolls = 1)
         
        PURPOSE: Simulate a game by rolling all dice simultaneously for a specified number of times.

        INPUTS:
        num_rolls: int specifying number of times to roll the dice

        OUTPUTS:
        game: attribute containing a dataframe of the last played game. The dataframe has roll number as the named index, columns for each die number, and the face rolled in that instance in each cell.

        RETURNS:
        none
         
    show_result(form = 'wide')
             
        PURPOSE: show the result of the last game played in either a 'wide' (default) or 'narrow' format as specified by the user.

        INPUT:
        form: string. Defaults to 'wide', accepts either 'narrow' or 'wide'.

        RETURNS:
        game: dataframe of the last game played in wide (default) or narrow format.
         

class Analyzer
    Used to analyze the results of a Game. It provides methods to calculate the number of jackpots,
    count occurrences of each face, and count combinations and permutations of the game results.
     
    
    __init__(game)
             
        PUPROSE: create an analyzer object from a game.

        INPUTS: game object

        RETURNS:
        none        
         
    jackpot()
             
        PURPOSE: Calculate the number of 'jackpots' that occurred in the last game. A jackpot is a result in which all faces are the same, e.g. all ones for a six-sided die.
        
        INPUTS: none

        RETURNS:
        total number of jackpots as an integer
         
    face_counts()
             
        PURPOSE: Compute how many times a given face is rolled for each event. For example, if a roll of five dice has all sixes, then the counts for this roll would be 5 for the face value '6' and 0 for the other faces.

        INPUTS: none

        RETURNS:
        counts: dataframe with roll number as the index, face values as columns, and count values in the cells
         
    combination_count()
             
        PURPOSE: Compute the distinct combination of faces rolled along with their counts. Combinations are order-independent.

        INPUTS: none

        RETURNS:
        dataframe with multiindex of distinct combinations and a column totaling each combinations' counts.
         
    permutation_count()
             
        PURPOSE: Compute the distinct permutations of faces rolled along with their counts. Permutations are order-dependent.

        INPUTS: none

        RETURNS:
        dataframe with multiindex of distinct permutations and a colum totaling each permutations' counts.
         
