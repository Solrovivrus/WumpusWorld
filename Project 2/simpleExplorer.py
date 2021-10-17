from os import curdir, stat
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


        for i in range(100000000):
            cave[currentLocation[0], currentLocation[1]] = 'E'
            print(cave)
            #Process is: Update tracker of what is encountered. Then make move.
            tracker = simple.checkNeighbors(cave, tracker, currentLocation)

            next = simple.nextMove(tracker, currentLocation)

            #hopefully killing a wumpus...
            for x in tracker[currentLocation[0], currentLocation[1]]:
                if "Stench" in x:
                    tracker, arrows, cave = simple.shootWumpus(cave, currentLocation, tracker, arrows)

            #will needs ability to end loop when implemented if return is string
            if isinstance(next, str) == True:
                print(next)
                return
            elif cave[next[0], next[1]] == 'DW':
                print("The cell is blocked by a dead Wumpus!")
                continue
            # removes explorers location in cave and updates currentlocation with what was chosen
            else:
                cave[currentLocation[0], currentLocation[1]] = ''
                currentLocation[0] = next[0]
                currentLocation[1] = next[1]

            print("Our explorer moves to: " + str(currentLocation) + " and...")
            if cave[currentLocation[0], currentLocation[1]] == 'P':
                print("Falls into a Pit!")
                return
            elif cave[currentLocation[0], currentLocation[1]] == 'W':
                print("Is eaten by a Wumpus!!")
                return
            elif cave[currentLocation[0], currentLocation[1]] == 'G':
                print("The explorer has found the gold!")
                return
            else:
                print("The explorer safely moves to the next cell :) ")


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
        #setting a list to hold 
        obstacleList = []
        tracker[x,y] = obstacleList

        #check left - if y = 0... nothing will be to the left of it
        #if a wumpus, assign stench in tracker. if pit, assign breeze
        if y>0:
            if cave[x,y-1] == 'W':
                tracker[x,y].append("Stench")
                print("A stench to the left!")
            elif cave[x,y-1] == 'P':
                tracker[x,y].append("Breeze")
                print("A breeze to the left!")
            else:
                print("Whew.. nothing new to the left")

        #check right
        with suppress(IndexError):
            if y < caveDim[1]-1:
                if cave[x, y+1] == 'W':
                    tracker[x,y].append("Stench")
                    print("A stench to the right!")
                elif cave[x, y+1] == 'P':
                    tracker[x,y].append("Breeze")
                    print("A breeze to the right!")
                else:
                    print("Whew.. nothing new to the right")

        #check top
        with suppress(IndexError):
            if x > 0:
                if cave[x-1, y] == 'W':
                    tracker[x,y].append("Stench")
                    print("A stench above!")
                elif cave[x-1, y] == 'P':
                    tracker[x,y].append("Breeze")
                    print("A breeze above!")
                else:
                    print("Whew.. nothing new above")

        #check bottom
        if x < caveDim[0]-1:
            if cave[x+1,y] == 'W':
                tracker[x,y].append("Stench")
                print("A stench below")
            elif cave[x+1,y] == 'P':
                tracker[x,y].append("Breeze")
                print("A breeze below")
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
        print(moves)
        print(len(moves))
     
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
                randomChoice = random.randint(0, len(moves)+1)
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
                print("Move choice =" + str(randomChoice))
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
        
    @staticmethod
    def shootWumpus(cave, currentLocation, tracker, arrowCount):
        simple = simpleExplorer
        caveDim= np.shape(cave)
        directionList = simple.legalMove(tracker, currentLocation)
        arrowDirection = []

        for lst in directionList:
            randomDirection = random.randint(0, len(directionList)-1)
            arrowDirection.append(directionList[randomDirection][0])
            arrowDirection.append(directionList[randomDirection][1])
            break

        while arrowCount > 0:
            if cave[arrowDirection[0], arrowDirection[1]] == 'W':
                print("The arrow hit a wumpus ")
                cave[arrowDirection[0], arrowDirection[1]] = 'DW'
                print("The explorer hears a terrible scream! A wumpus is dead!")
                for x in tracker[currentLocation[0], currentLocation[1]]:
                    if "Stench" in x:
                        tracker[currentLocation[0], currentLocation[1]].remove(x)
                        arrowCount -= 1
                        return tracker, arrowCount, cave
            
            elif cave[arrowDirection[0], arrowDirection[1]] == 'DW':
                print("The explorer hears a mushy thud... I hit a dead Wumpus!")
                arrowCount -= 1
                return tracker, arrowCount, cave

            # indicate that arrow traveling up and continues
            elif currentLocation[0] > arrowDirection[0] and arrowDirection[0] > 0:
                arrowDirection[0] -= 1
                print("The arrow travles upwards and is in cell " + str(arrowDirection)) 
            # indicates that arrow traveling down and continues
            elif currentLocation[0] < arrowDirection[0] and arrowDirection[0] < caveDim[0]-1:
                arrowDirection[0] += 1 
                print("The arrow travles downwards and is in cell " + str(arrowDirection))
            # indicates that arrow traveling left and continues
            elif currentLocation[1] > arrowDirection[1] and arrowDirection[1] > 0:
                arrowDirection[1] -= 1 
                print("The arrow travels to the left and is in cell " + str(arrowDirection))
            # indicates that arrow traveling right and continues
            elif currentLocation[1] < arrowDirection[1] and arrowDirection[1] < caveDim[1]-1:
                arrowDirection[1] += 1
                print("The arrow travels to the right and is in cell " + str(arrowDirection))
            else:
                print("The explorer hears a thud as the arrow collides with a wall. Better aim next time!")
                return tracker, arrowCount, cave

            







        
        
        



            



        
