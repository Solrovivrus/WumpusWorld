from os import stat
import numpy as np
from contextlib import suppress

class simpleExplorer:

    # --------------------------------------------------------------------------------------------
    # The caveSelection method iterates through all 10 caves generated and sends them to be solved 
    # within the simpleExplorer class
    @staticmethod
    def caveSelection(caves):
        simple = simpleExplorer
        for cave in caves:
            currentCave = simple.placeExplorer


    @staticmethod
    def placeExplorer(cave):
        simple = simpleExplorer
        # initializing starting cell count
        numCells = 0

        # placing the explorer in its starting location. Initializing current location tracker
        cave[0,0] = 'E'
        currentLocation = [0,0]
        print(cave)
        #assigning arrows based on number of wumpi in cave
        wumpusCount = 0
        for i in range(len(cave)):
            for j in range(len(cave[0])):
                if cave[i,j] == 'W':
                    wumpusCount += 1
        arrows = wumpusCount

        #initializing tracking cave
        tracker = np.full_like(cave, 0, dtype=object)

        simple.checkNeighbors(cave, tracker, currentLocation)



    # --------------------------------------------------------------------------------------------
    # The checkCells method checks through neighboring cells for possibile moves. Assigns a list to
    # the tracker matrix which holds stench/breeze values
    @staticmethod
    def checkNeighbors(cave, tracker, currentLocation):

        #getting dimensions
        caveDim = np.shape(cave)

        #iterating through neighboring cells to see what's possible
        x = currentLocation[0]
        y = currentLocation[1]
        print(x, y)
        print(tracker)
        #setting a list to hold 
        obstacleList = []
        tracker[x,y] = obstacleList
        print(tracker)
        #check left - if y = 0... nothing will be to the left of it
        #if a wumpus, assign stench in tracker. if pit, assign breeze
        if y>0:
            if cave[x-1,y] == 'W':
                tracker[x,y].append("Stench")
                print("A stench to the left!")
                print(tracker)
            elif cave[x-1,y] == 'P':
                tracker[x,y].append("Breeze")
                print("A breeze to the left!")
                print(tracker)
            else:
                print("Whew.. nothing new to the left")

        #check right
        with suppress(IndexError):
            if y < caveDim[1]-1:
                if cave[x+1, y] == 'W':
                    tracker[x,y].append("Stench")
                    print("A stench to the right!")
                    print(tracker)
                elif cave[x+1, y] == 'P':
                    tracker[x,y].append("Breeze")
                    print("A breeze to the right!")
                    print(tracker)
                else:
                    print("Whew.. nothing new to the left")

        #check top
        with suppress(IndexError):
            if x > 0:
                if cave[x, y+1] == 'W':
                    tracker[x,y].append("Stench")
                    print("A stench above!")
                    print(tracker)
                elif cave[x, y+1] == 'P':
                    tracker[x,y].append("Breeze")
                    print("A breeze above!")
                    print(tracker)
                else:
                    print("Whew.. nothing new above")

        #check bottom
        if x < caveDim[0] - :
            if cave[x,y-1] == 'W':
                tracker[x,y].append("Stench")
                print("A stench below")
                print(tracker)
            elif cave[x,y-1] == 'P':
                tracker[x,y].append("Breeze")
                print("A breeze below")
                print(tracker)
            else:
                print("Whew.. nothing new below")






        