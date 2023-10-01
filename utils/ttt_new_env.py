import turtle as t
from random import choice
import numpy as np
import time

# Define an action_space helper class
class action_space:
    def __init__(self, n):
        self.n = n
    def sample(self):
        num = np.random.choice(range(self.n))
        # covert to 1 to 9
        action = 1+num
        return action
    
# Define an obervation_space helper class    
class observation_space:
    def __init__(self, n):
        self.shape = (n,)

class ttt():
    def __init__(self): 
        # use the helper action_space class
        self.action_space=action_space(9)
        # use the helper observation_space class
        self.observation_space=observation_space(9)
        self.info=""         
        # Create a dictionary to map cell number to coordinates
        self.cellcenter = {1:(-200,-200), 2:(0,-200), 3:(200,-200),
                    4:(-200,0), 5:(0,0), 6:(200,0),
                    7:(-200,200), 8:(0,200), 9:(200,200)} 


    def reset(self):  
        # The X player moves first
        self.turn = "X"
        # Count how many rounds played
        self.rounds = 1
        # Create a list of valid moves
        self.validinputs = list(self.cellcenter.keys())
        # Create a dictionary of moves made by each player
        self.occupied = {"X":[],"O":[]}
        # Tracking the state
        self.state=np.array([0,0,0,0,0,0,0,0,0])
        self.done=False
        self.reward=0     
        return self.state        
        
    # step() function: place piece on board and update state
    def step(self, inp):
        # Add the move to the occupied list 
        self.occupied[self.turn].append(inp)
        # update the state: X is 1 and O is -1
        self.state[int(inp)-1]=2*(self.turn=="X")-1
        # Disallow the move in future rounds
        self.validinputs.remove(inp) 
        # check if the player has won the game
        if self.win_game() == True:
            self.done=True
            # reward is 1 if X won; -1 if O won
            self.reward=2*(self.turn=="X")-1
            self.validinputs=[]
        # If all cellls are occupied and no winner, it's a tie
        elif self.rounds == 9:
            self.done=True
            self.reward=0
            self.validinputs=[]
        # Counting rounds
        self.rounds += 1
        # Give the turn to the other player
        if self.turn == "X":
            self.turn = "O"
        else:
            self.turn = "X"             
        return self.state, self.reward, self.done, self.info
                    
    # Determine if a player has won the game
    def win_game(self):
        lst = self.occupied[self.turn]
        if 1 in lst and 2 in lst and 3 in lst:
            return True
        elif 4 in lst and 5 in lst and 6 in lst:
            return True        
        elif 7 in lst and 8 in lst and 9 in lst:
            return True        
        elif 1 in lst and 4 in lst and 7 in lst:
            return True
        elif 2 in lst and 5 in lst and 8 in lst:
            return True
        elif 3 in lst and 6 in lst and 9 in lst:
            return True
        elif 1 in lst and 5 in lst and 9 in lst:
            return True
        elif 3 in lst and 5 in lst and 7 in lst:
            return True
        else:
            return False


