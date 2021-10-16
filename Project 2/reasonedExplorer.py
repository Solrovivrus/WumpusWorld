import random
from contextlib import suppress

import numpy as np


class reasonedExplorer:
    """
    This method will take the cave array and use random uniform distribution to
    pick a random place to start the explorer, and also count the wumpi
    to give the explorer the right amount of arrows
    """

    @staticmethod
    def placeExplorer(caves):
        rea = reasonedExplorer
        caveDim = np.shape(caves)
        currentLocation = []
        count = 0

        while count == 0:
            row = random.randint(1, caveDim[0] - 1)
            col = random.randint(1, caveDim[1] - 1)
            if caves[row, col] == '':
                caves[row, col] = 'E'
                currentLocation = [row, col]
                count += 1
            else:
                continue

        print(caves)
        # initializing tracking cave
        tracker = np.full_like(caves, 0, dtype=object)

        rea.track(caves, tracker, currentLocation)

    """
    So the place explorer needs to place the explorer in a random blank space on the board
    my code up above does that but it doesnt fit with the track method yet and needs to be tweaked
    the code commented out is my attempt on that but it doesnt work
    it also replaces everything with 0 for some reason?
    
    @staticmethod
    def placeExplorer(caves):
        rea = reasonedExplorer
        caveDim = np.shape(caves)
        currentLocation = caves
        count = 0

        while count == 0:
            row = random.randint(1, caveDim[0] - 1)
            col = random.randint(1, caveDim[1] - 1)
            if caves[row, col] == ' ':
                currentLocation[row, col] = 'E'
                count += 1
            else:
                continue
        # initializing tracking cave
        tracker = np.full_like(caves, 0, dtype=object)

        rea.track(caves, tracker, currentLocation)
    """

    @staticmethod
    def track(cave, tracker, currentLocation):
        rea = reasonedExplorer
        # getting dimensions
        caveDim = np.shape(cave)
        direction = []
        pickDirection = random.randint(1, 4)

        # iterating through neighboring cells to see what's possible
        x = currentLocation[0]
        y = currentLocation[1]
        # print(x, y)
        # print(tracker)
        # setting a list to hold
        obstacleList = []
        tracker[x, y] = obstacleList
        # print(tracker)

        # check left - if y = 0... nothing will be to the left of it
        # if a wumpus, assign stench in tracker. if pit, assign breeze
        if y > 0:
            if pickDirection == 1:
                direction = [x, y - 1]
            if cave[x, y - 1] == 'W':
                tracker[x, y].append("Stench")
                print("A stench to the left!")
                # print(tracker)
            elif cave[x, y - 1] == 'P':
                tracker[x, y].append("Breeze")
                print("A breeze to the left!")
                # print(tracker)
            else:
                print("Whew.. nothing new to the left")

        # check right
        with suppress(IndexError):

            if y < caveDim[1] - 1:
                if pickDirection == 2:
                    direction = [x, y + 1]
                if cave[x, y + 1] == 'W':
                    tracker[x, y].append("Stench")
                    print("A stench to the right!")
                    # print(tracker)
                elif cave[x, y + 1] == 'P':
                    tracker[x, y].append("Breeze")
                    print("A breeze to the right!")
                    # print(tracker)
                else:
                    print("Whew.. nothing new to the right")

        # check top
        with suppress(IndexError):
            if x > 0:
                if pickDirection == 3:
                    direction = [x - 1, y]
                if cave[x - 1, y] == 'W':
                    tracker[x, y].append("Stench")
                    print("A stench above!")
                    # print(tracker)
                elif cave[x - 1, y] == 'P':
                    tracker[x, y].append("Breeze")
                    print("A breeze above!")
                    # print(tracker)
                else:
                    print("Whew.. nothing new above")

        # check bottom
        if x < caveDim[0] - 1:
            if pickDirection == 4:
                direction = [x + 1, y]
            if cave[x + 1, y] == 'W':
                tracker[x, y].append("Stench")
                print("A stench below")
                # print(tracker)
            elif cave[x + 1, y] == 'P':
                tracker[x, y].append("Breeze")
                print("A breeze below")
                # print(tracker)
            else:
                print("Whew.. nothing new below")

        # if "stench" in tracker[x, y]:
        rea.shootWumpus(cave, currentLocation, direction)
        rea.tryToEnter(cave, currentLocation, direction)

    @staticmethod
    def tryToEnter(cave, currentLocation, direction):
        x = currentLocation[0]
        y = currentLocation[1]

        print(direction)
        # if y > 0 or y < caveDim[1] - 1 or x > 0 or x < caveDim[0] - 1:
        if cave[direction[0], direction[1]] == 'W':
            # if explorer dies put F for Fatality
            cave[direction[0], direction[1]] = 'F'
            print("You died from Wumpus")
        elif cave[direction[0], direction[1]] == 'P':
            # if explorer dies put F for Fatality
            cave[direction[0], direction[1]] = 'F'
            print("You died from a pit")
        elif cave[direction[0], direction[1]] == 'B':
            print("You cannot go that way")
        elif cave[direction[0], direction[1]] == 'G':
            print("You found the gold!")
        elif cave[direction[0], direction[1]] == 'D':
            print("There's a dead Wumpus here! Pat yourself of the back for killing it :)")
        else:
            cave[x, y] = 'S'
            cave[direction[0], direction[1]] = 'E'

        print(cave)



    @staticmethod
    def shootWumpus(cave, currentLocation, direction):
        caveDim = np.shape(cave)
        x = currentLocation[0]
        y = currentLocation[1]

        # assigning arrows based on number of wumpi in cave
        wumpusCount = 0
        for i in range(len(cave)):
            for j in range(len(cave[0])):
                if cave[i, j] == 'W':
                    wumpusCount += 1
        arrows = 1# wumpusCount

        if arrows == 0:
            print("You're out of arrows!")
        # direction[1] > 0 and direction[1] < caveDim[1] - 1 and direction[0] > 0 and direction[0] < caveDim[0] - 1:
        while 0 < direction[1] < caveDim[1] - 1 and 0 < direction[0] < caveDim[0] - 1:
            if cave[direction[0], direction[1]] == 'W':
                # change the wumpus into a dead wumpus
                cave[direction[0], direction[1]] = 'D'
                print("You heard a scream")
                print(cave)
                arrows -= 1
                break
            elif cave[direction[0], direction[1]] != '':
                print("You hear your arrow break")
                arrows -= 1
                break
            elif cave[direction[0], direction[1]] == '':
                if x != direction[0]:
                    if direction[0] < x:
                        direction = [direction[0] - 1, direction[1]]
                    else:
                        direction = [direction[0] + 1, direction[1]]
                elif y != direction[1]:
                    if direction[0] < x:
                        direction = [direction[0], direction[1] - 1]
                    else:
                        direction = [direction[0], direction[1] - 1]
        # cave[direction[0], direction[1]] = 'A'
            else:
                print(cave)
                print("You hear your arrow hit a wall")
                arrows -= 1



'''
        # check right
        with suppress(IndexError):
            if y < caveDim[1]-1:
                if cave[x, y+1] == 'W':
                    print("You died from Wumpus")
                elif cave[x, y+1] == 'P':
                    print("You died from a pit")
                elif cave[x, y+1] == 'B':
                    print("You cannot go that way")
                elif cave[x, y+1] == 'G':
                    print("You found the gold!")
                else:
                    cave[x, y+1] = 'E'

        # check top
        with suppress(IndexError):
            if x > 0:
                if cave[x-1, y] == 'W':
                    print("You died from Wumpus")
                elif cave[x-1, y] == 'P':
                    print("You died from a pit")
                elif cave[x-1, y] == 'B':
                    print("You cannot go that way")
                elif cave[x-1, y] == 'G':
                    print("You found the gold!")
                else:
                    cave[x-1, y] = 'E'

        # check bottom
        if x < caveDim[0]-1:
            if cave[x+1, y] == 'W':
                print("You died from Wumpus")
            elif cave[x+1, y] == 'P':
                print("You died from a pit")
            elif cave[x+1, y] == 'B':
                print("You cannot go that way")
            elif cave[x+1, y] == 'G':
                print("You found the gold!")
            else:
                cave[x+1, y] = 'E'

        print(cave)
'''
'''
        my old code to check neighboring cells, it checks left and right well enough
        but I couldn't figure out how to check up and down
        but once we do that we can just make a copy of a blank array 
        and use that to track areas that are next to danger/blocked.
        Just gonna keep this here in case it comes handy
        
        # gotGold = False
        rea = reasonedExplorer
        f = rea.placeExplorer(caves)
        print(f)
        
        for array in f:
            for i in range(0, len(array)):
                if array[i] == 'E':
                    if array[i-1] or array[i+1] == 'P':
                        print("you feel a breeze.")
                    if array[i-1] or array[i+1] == 'W':
                        print("you smell something awful")
                    else:
                        print("nothing to see here")
        



            for i in range(0, len(array)):
                if array[i] == 'E':
                    if array[i-len(array)] or array[i+len(array)] == 'P':
                        print(array[i-len(array)])
                        #print(array[i+len(array)])
                        print("you feel a breeze.")
                    if array[i-len(array)] or array[i+len(array)] == 'W':
                        print("you smell something awful")
                    else:
                        print("nothing to see here")
'''
