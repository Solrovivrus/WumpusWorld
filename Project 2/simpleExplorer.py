from os import stat
import numpy as np
from contextlib import suppress
import random

class simpleExplorer:

    # --------------------------------------------------------------------------------------------
    # The caveSelection method iterates through all 10 caves generated and sends them to be solved 
    # within the simpleExplorer class
    @staticmethod
    def caveSelection(caves):
        simple = simpleExplorer
        for cave in caves:
            currentCave = simple.placeExplorer(cave)


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

        #Process is: Update tracker of what is encountered. Then make move.
        tracker = simple.checkNeighbors(cave, tracker, currentLocation)

        next = simple.nextMove(tracker, currentLocation)

        #will needs ability to end loop when implemented if return is string
        if isinstance(next, str) == True:
            print(next)
        else:
            currentLocation[0] = next[0]
            currentLocation[1] = next[1]
        print(currentLocation)




        

    # --------------------------------------------------------------------------------------------
    # The checkCells method checks through neighboring cells for possibile moves. Assigns a list to
    # the tracker matrix which holds stench/breeze values
    @staticmethod
    def checkNeighbors(cave, tracker, currentLocation):
        simple = simpleExplorer
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
            if cave[x,y-1] == 'W':
                tracker[x,y].append("Stench")
                print("A stench to the left!")
                print(tracker)
            elif cave[x,y-1] == 'P':
                tracker[x,y].append("Breeze")
                print("A breeze to the left!")
                print(tracker)
            else:
                print("Whew.. nothing new to the left")

        #check right
        with suppress(IndexError):
            if y < caveDim[1]-1:
                if cave[x, y+1] == 'W':
                    tracker[x,y].append("Stench")
                    print("A stench to the right!")
                    print(tracker)
                elif cave[x, y+1] == 'P':
                    tracker[x,y].append("Breeze")
                    print("A breeze to the right!")
                    print(tracker)
                else:
                    print("Whew.. nothing new to the right")

        #check top
        with suppress(IndexError):
            if x > 0:
                if cave[x-1, y] == 'W':
                    tracker[x,y].append("Stench")
                    print("A stench above!")
                    print(tracker)
                elif cave[x-1, y] == 'P':
                    tracker[x,y].append("Breeze")
                    print("A breeze above!")
                    print(tracker)
                else:
                    print("Whew.. nothing new above")

        #check bottom
        if x < caveDim[0]-1:
            if cave[x+1,y] == 'W':
                tracker[x,y].append("Stench")
                print("A stench below")
                print(tracker)
            elif cave[x+1,y] == 'P':
                tracker[x,y].append("Breeze")
                print("A breeze below")
                print(tracker)
            else:
                print("Whew.. nothing new below")
        
        return tracker


    @staticmethod
    def nextMove(tracker, currentLocation):
        simple = simpleExplorer
        #getting current coordinates
        x = currentLocation[0]
        y = currentLocation[1]
        #initializing list to store next move
        next = []
        #setting up possibilities
        left = [x,y-1]
        right = [x,y+1]
        up = [x-1, y]
        down = [x+1,y]

        # sends tracker and current location to find what moves are available
        moves = simple.legalMove(tracker, currentLocation)

        # if the returned moves list is empty, not moves left so quit, this should only happen
        # if player is initially palced in a cage
        if len(moves) == 0:
            return "Game Over"

        # check first to see if one of the cells are unexplored.. if so , make that move
        if len(moves) == 4:
            if tracker[left[0],left[1]] == 0:
                next.append(left[0])
                next.append(left[1])
            
            elif tracker[right[0],right[1]] == 0:
                next.append(right[0])
                next.append(right[1])
            
            elif tracker[up[0],up[1]] == 0:
                next.append(up[0])
                next.append(up[1])
            
            elif tracker[down[0],down[1]] == 0:
                next.append(down[0])
                next.append(down[1])
            
            else:
                randomChoice = random.randint(0, len(moves)-1)
                next.append(moves[randomChoice][0])
                next.append(moves[randomChoice][1])
            
            return next

        # if list isn't full, pick one that's not been explored first
        for lst in moves:
            if tracker[lst[0], lst[1]] == 0:
                next.append(lst[0])
                next.append(lst[1])
                return next
            else: 
                randomChoice = random.randint(0, len(moves)-1)
                next.append(moves[randomChoice][0])
                next.append(moves[randomChoice][1])
                return next

        
        


            
    # the legalMove function checks through the neighbors to see what exists and adds to 
    # legalList with what directions would work
    @staticmethod
    def legalMove(tracker, currentLocation):
        simple = simpleExplorer
        legalList = []
        x = currentLocation[0]
        y = currentLocation[1]
        caveDim = np.shape(tracker)
        #adding list of possible coordinates
        if y > 0:
            legalList.append([x,y-1])
        if y < caveDim[1]-1:
            legalList.append([x,y+1])
        if x > 0:
            legalList.append([x-1,y])
        if x < caveDim[0]-1:
            legalList.append([x+1, y])
        
        return legalList
        
        



            



        
