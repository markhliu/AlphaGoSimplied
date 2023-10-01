import turtle as t
import numpy as np
import time
import random

# Define an action_space helper class
class action_space:
    def __init__(self, n):
        self.n = n
   
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
        self.showboard=False          
        # Create a dictionary to map cell number to coordinates
        self.cellcenter = {1:(-200,-200), 2:(0,-200), 3:(200,-200),
                    4:(-200,0), 5:(0,0), 6:(200,0),
                    7:(-200,200), 8:(0,200), 9:(200,200)} 
        # set the game to the initial state
        self.reset()
        
    # sample() function: returns a random move
    def sample(self):
        return random.choice(self.validinputs)   

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
        else:
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


    def display_board(self):
        # Set up the screen
        try:
            t.setup(630,630,10,70) 
        except t.Terminator:
            t.setup(630,630,10,70)   
        t.tracer(False)
        t.hideturtle()
        t.bgcolor("azure")
        t.title("Tic-Tac-Toe in Turtle Graphics")
        # Draw horizontal lines and vertical lines
        t.pensize(5)
        t.color('blue')
        for i in (-300,-100,100,300):  
            t.up()
            t.goto(i,-300)
            t.down()
            t.goto(i,300)
            t.up()
            t.goto(-300,i)
            t.down()
            t.goto(300,i)
            t.up()
        # Write down the cell number
        t.color('red')
        for cell, center in list(self.cellcenter.items()):
            t.goto(center[0]-80,center[1]-80)
            t.write(cell,font = ('Arial',20,'normal'))

    def render(self):
        if self.showboard==False:
            self.display_board()
            self.showboard=True   
        # Place X or O in occupied cells
        t.color('light gray')
        if len(self.occupied["X"])>0:
            for x in self.occupied["X"]:
                xy=self.cellcenter[x]
                t.up()
                t.goto(xy[0]-60,xy[1]-60)
                t.down()               
                t.goto(xy[0]+60,xy[1]+60)
                t.up()
                t.goto(xy[0]-60,xy[1]+60)
                t.down()               
                t.goto(xy[0]+60,xy[1]-60)
                t.up()    
                t.update()
        if len(self.occupied["O"])>0:                
            for o in self.occupied["O"]:
                t.up()
                t.goto(self.cellcenter[o])
                t.dot(160,"light gray") 
                t.update()

    def close(self):
        time.sleep(1)
        try:
            t.bye()
        except t.Terminator:
            print('exit turtle')
            
            
            
            
            
            
            