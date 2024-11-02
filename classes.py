import numpy as np
import pandas as pd

class Die:
    '''
    A class to create a die with customizable faces and weights. This die can be rolled, and each face has a weight 
    that affects the likelihood of it appearing in a roll. Faces can be strings or numbers, and weights can be positive 
    numbers, including zero. Weights default to 1 if not specified.
    '''
    def __init__(self, faces):
        '''
        PURPOSE: Create a die object with any number of faces.
        INPUTS: 
        faces: numpy array containing strings or numpy array containing numbers

        OUTPUTS:
        face_weights: dataframe containing the weight for each face on the die.

        RETURNS:
        none
        '''
        if not isinstance(faces, np.ndarray):
            raise TypeError("Expected a numpy array for 'faces', but received something else.")
        if not (np.issubdtype(faces.dtype, np.str_) or np.issubdtype(faces.dtype, np.number)):
            raise TypeError("The faces array must contain all strings or all integers. Your array is of type "+str(faces.dtype))
        if len(faces) != len(np.unique(faces)):
            raise ValueError("All faces must be unique.")
        
        self.face_weights = pd.DataFrame({'faces': faces, 'weights': 1.0})
        self.face_weights.set_index('faces', inplace=True)

    def change_face_weight(self, face, weight):
        '''
        PURPOSE: Customize the weights of the faces on an existing die object.

        INPUTS: 
        face: string or int. Will raise IndexError if the face provided is not present in the die's index of faces.
        weight: float or int. Must be positive.

        OUTPUTS:
        Changes the face_weights attribute to reflect the inputted weight.

        RETURNS:
        none
        
        '''
        if face not in self.face_weights.index:
            raise IndexError("The face whose weight you wish to change is not on the die. Valid faces are: "+ str(self.face_weights.index.to_list()))
        if not isinstance(weight, (int, float)):
            raise TypeError("Only integers or floats can be used as face weights.")
        if weight < 0:
            raise ValueError("Face weights must be positive.")
        self.face_weights.loc[face,'weights'] = weight

    def roll_die(self, num_rolls = 1):
        '''
        PURPOSE: Roll the die the specified number of times and return the results of the rolls. For example, if a standard six-sided die was rolled 3 times, the output could look like this: [2,4,3].

        INPUTS: 
        num_rolls: int

        RETURNS:
        rolls: list of strings or integers
        '''
        rolls = []
        for i in range(num_rolls):
            rolls.append(self.face_weights.sample(n = 1, weights = 'weights').index[0])
        return rolls
    
    def show_face_weights(self):
        '''
        PURPOSE: Show the weights for each face on the die.

        INPUTS:
        none

        RETURNS:
        face_weights: Dataframe with 'faces' as the index and 'weights' as a column of floats
        '''
        return self.face_weights

# mydie = Die(np.array(['red','blue','green']))
# mydie.change_face_weight('red',10)
# print(mydie.roll_die(10))

class Game:
    '''Represents a game played with multiple dice. Each die is rolled simultaneously for a specified
    number of rolls. The results are stored and can be presented in either a wide or narrow format.'''

    game = pd.DataFrame()

    def __init__(self, dice):
        '''
        PURPOSE: Create a game object with a list of dice.

        INPUTS: 
        dice: list of dice objects

        RETURNS: 
        none
        '''
        if not isinstance(dice, list):
            raise ValueError("Please create a game using a list of Die objects.")
        if not isinstance(dice[0], Die):
            raise ValueError("Your list must contain Die objects only.")

        self.dice = dice

    def play(self, num_rolls = 1):
        '''
        PURPOSE: Simulate a game by rolling all dice simultaneously for a specified number of times.

        INPUTS:
        num_rolls: int specifying number of times to roll the dice

        OUTPUTS:
        game: attribute containing a dataframe of the last played game. The dataframe has roll number as the named index, columns for each die number, and the face rolled in that instance in each cell.

        RETURNS:
        none
        '''
        self.current_game = {}
        for index, die in enumerate(self.dice):
            self.current_game[index] = die.roll_die(num_rolls = num_rolls)
        roll_num = range(1, num_rolls + 1)
        self.game = pd.DataFrame(self.current_game, index = roll_num)

    def show_result(self, form = 'wide'):
        '''
        PURPOSE: show the result of the last game played in either a 'wide' (default) or 'narrow' format as specified by the user.

        INPUT:
        form: string. Defaults to 'wide', accepts either 'narrow' or 'wide'.

        RETURNS:
        game: dataframe of the last game played in wide (default) or narrow format.
        '''
        if form == 'wide':
            return self.game
        elif form == 'narrow':
            return self.game.stack()
        else:
            raise ValueError('Please specify how to return results using either "narrow" or "wide".')
    
class Analyzer:
    '''
    Used to analyze the results of a Game. It provides methods to calculate the number of jackpots,
    count occurrences of each face, and count combinations and permutations of the game results.
    '''

    def __init__(self, game):
        '''
        PUPROSE: create an analyzer object from a game.

        INPUTS: game object

        RETURNS:
        none        
        '''
        if not isinstance(game, Game):
            raise ValueError("Please include a 'Game' object in your constructor.")

        self.game = game

    def jackpot(self):
        '''
        PURPOSE: Calculate the number of 'jackpots' that occurred in the last game. A jackpot is a result in which all faces are the same, e.g. all ones for a six-sided die.
        
        INPUTS: none

        RETURNS:
        total number of jackpots as an integer
        '''
        jackpots = self.game.show_result().nunique(axis = 1)
        return (jackpots == 1).sum()
    
    def face_counts(self):
        '''
        PURPOSE: Compute how many times a given face is rolled for each event. For example, if a roll of five dice has all sixes, then the counts for this roll would be 5 for the face value '6' and 0 for the other faces.

        INPUTS: none

        RETURNS:
        counts: dataframe with roll number as the index, face values as columns, and count values in the cells
        '''
        counts = self.game.show_result().stack().groupby(level=0).value_counts().unstack(fill_value=0)
        return counts
    
    def combination_count(self):
        '''
        PURPOSE: Compute the distinct combination of faces rolled along with their counts. Combinations are order-independent.

        INPUTS: none

        RETURNS:
        dataframe with multiindex of distinct combinations and a column totaling each combinations' counts.
        '''
        combo_df = pd.DataFrame(np.sort(self.game.show_result().values, axis = 1), columns = self.game.show_result().columns)
        return combo_df.value_counts().to_frame()

    def permutation_count(self):
        '''
        PURPOSE: Compute the distinct permutations of faces rolled along with their counts. Permutations are order-dependent.

        INPUTS: none

        RETURNS:
        dataframe with multiindex of distinct permutations and a colum totaling each permutations' counts.
        '''
        return self.game.show_result().value_counts().to_frame()


# die1 = Die(np.array([1,2,3,4,5,6]))
# die2 = Die(np.array([1,2,3,4,5,6]))
# newgame = Game([die1,die2])
# newgame.play(5)
# a1 = Analyzer(newgame)

# print(a1.face_counts())
# print(a1.face_counts().shape)

die1 = Die(np.array([1,2,3,4,5,6]))
newgame = Game([die1,die1])
newgame.play(1000)

a1 = Analyzer(newgame)
combos = a1.combination_count()

print(type(combos))
