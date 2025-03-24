import math
import random

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

df = pd.read_csv("Data.csv")



# A figure with axes
fig, ax = plt.subplots()
# the axes limits xmin, x max, y min, y max
ax.axis([0,100,0,10000])
# create a point in the axes, we are plotting the data from CSV file "Data.csv" . 
# Assume that, there are 100 possible sates Si where i = (1...100) 
# Each state (except state 1 and 100) have exactly 2 neighbours. Si has neighbors Si-1 and Si+1
# Data.csv directly provides the reward/utility of every state (1 to 100). Column named "State" corresponds to state number and its respective row " Reward" corresponds to utility of the state.
ax.plot(df['State'],df['Reward'])
# An animated point used to show the current state on the plot.
point, = ax.plot(0,1, marker="o")


# we will randomly use a state as the initial state. Indexing starts from 0, therefore, we are ommiting that first and last row
start_state=random.randint(1,98)
#Initially current state = start state.
cur_state=start_state

#Temperature = 4000, use this for Section 2, Q2
T = 4000

#A simple hillclimbing method, without sideway moves,  is implemented as an example
def HillClimbNoSideways(time):
    global cur_state #access the curstate as global variable
    #checks neighbors and move only if utility is strictly greater than current state.
    #The point is returned to the animating function which displays it on the plot.
    #Use this code an as example to complete the other two functions.
    if(df["Reward"][cur_state+1] >df["Reward"][cur_state]):
        cur_state=min(cur_state+1,98)
        point.set_data([cur_state], [df['Reward'][cur_state]])
        return point
    elif ( df["Reward"][cur_state - 1]>df["Reward"][cur_state] ):
        cur_state = max(cur_state - 1,1)
        point.set_data([cur_state], [df['Reward'][cur_state]])
        return point
    return point

""" DO NOT MAKE MODIFICATIONS ABOVE THIS LINE"""

#______________________________________________


def HillClimbWithSideways(time):
    global cur_state, limitvar
    probability=random.random()
    #print(probability) #for testing
    #initially added and limitvar > 0: to stop the looping condition at some points in the grap. but the problem was that even tho the plot updation stopped, the animation continued. then I found about event_source.stop.
    if df["Reward"][cur_state+1] > df["Reward"][cur_state]: #
        cur_state = min(cur_state+1, 98)
    elif df["Reward"][cur_state+1] == df["Reward"][cur_state] and probability < 0.5: #if the reward of the neighbour state is same, that means a plateau
        cur_state = min(cur_state+1, 98)

    elif df["Reward"][cur_state-1] > df["Reward"][cur_state] :
        cur_state = max(cur_state-1, 1)
    elif df["Reward"][cur_state-1] == df["Reward"][cur_state] and probability < 0.5: #if the reward of the neighbour state is same, that means a plateau
        cur_state = max(cur_state-1, 1)

    # final part to update the graph
    point.set_data([cur_state], [df['Reward'][cur_state]])
    return point


#'''
GlobalMaxima = cur_state #globalmaxima to store highest discovered reward.
def SimulatedAnnealing(time):
    global cur_state, T, GlobalMaxima
    if T == 0:
        cur_state = cur_state
    elif T>0:
        nextState = random.choice([min(cur_state+1, 98),max(cur_state-1, 1)]) #The Algorithm must randomly select a neighbor with probability 0.5
        delta = df["Reward"][nextState] - df["Reward"][cur_state] #delta stands for the difference in state utility.
        probability = math.exp(delta/T) #probability  p = e^(delta/T)
        if delta > 0: # which allows all upward moves
            cur_state = nextState
        else:
            if random.random() < probability: #which allows downward  moves with  probability  p = e^(delta/T)
                cur_state = nextState
        '''if delta > 0 or random.random() < probability: # which allows all upward moves, if not- allow downward  moves with  probability  p = e^(delta/T)
            cur_state = nextState'''
    T -= 1  #Use a linearly decreasing T , that is, T=T-1 every iteration.
    if T <= 0:  #stopping animation when Animation gets 0
        ani.event_source.stop()

# I have noticed that depending on where the current state is when T hits 0, It is not reaching a global Maxima.
# So I added the code below so that it will atleast display what the highest reward (global maxima) is.
    if df["Reward"][cur_state] > df["Reward"][GlobalMaxima]:
        GlobalMaxima = cur_state
    print("Temperature",T)
    print("max Reward found till now is at state", GlobalMaxima, "with reward",df["Reward"][GlobalMaxima])
    print("----------------------------------------------------------------------------")

 #final part to update the graph
    point.set_data([cur_state], [df['Reward'][cur_state]])
    return point


""" DO NOT MAKE MODIFICATIONS BELOW THIS LINE, Except for the second parameter in FuncAnimation call"""
#______________________________________________

# This  animation with 50ms interval, which is repeated,
# The second parameter, the function name, is the function that is called
# repeatedly for "frames" (sixth parameter) number of times.

ani = FuncAnimation(fig,SimulatedAnnealing, interval=50, blit=False, repeat=False, frames=5000)
#ani = FuncAnimation(fig,HillClimbWithSideways, interval=50, blit=False, repeat=False, frames=5000)
#ani = FuncAnimation(fig,HillClimbNoSideways, interval=50, blit=False, repeat=False, frames=5000)

plt.show()

