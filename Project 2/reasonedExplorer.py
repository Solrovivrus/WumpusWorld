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
        pickDirection = random.randint(1, 4)
        gold = False
        alive = True

        while count == 0:
            row = random.randint(1, caveDim[0] - 1)
            col = random.randint(1, caveDim[1] - 1)
            if caves[row, col] == '':
                caves[row, col] = 'E'
                currentLocation = [row, col]
                count += 1
            else:
                continue


        # initializing tracking cave
        tracker = np.full_like(caves, 0, dtype=object)

        rea.track(caves, tracker, currentLocation, pickDirection, gold, alive)

    @staticmethod
    def track(cave, tracker, currentLocation, pickDirection, gold, alive):
        rea = reasonedExplorer
        # getting dimensions
        caveDim = np.shape(cave)
        direction = []

        # iterating through neighboring cells to see what's possible
        x = currentLocation[0]
        y = currentLocation[1]

        # setting a list to hold
        obstacleList = ["Safe"]
        tracker[x, y] = obstacleList

        # check left - if y = 0... nothing will be to the left of it
        # if a wumpus, assign stench in tracker. if pit, assign breeze
        while not gold:
            print(cave)
            if not alive:
                return print("Your journey ends here")
            else:
                if y > 0:
                    if pickDirection == 1:
                        direction = [x, y - 1]
                    if cave[x, y - 1] == 'W':
                        tracker[x, y].append("Stench")
                        print("A stench to the left!")

                    elif cave[x, y - 1] == 'P':
                        tracker[x, y].append("Breeze")
                        print("A breeze to the left!")

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

                        elif cave[x, y + 1] == 'P':
                            tracker[x, y].append("Breeze")
                            print("A breeze to the right!")

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

                        elif cave[x - 1, y] == 'P':
                            tracker[x, y].append("Breeze")
                            print("A breeze above!")

                        else:
                            print("Whew.. nothing new above")

                # check bottom
                if x < caveDim[0] - 1:
                    if pickDirection == 4:
                        direction = [x + 1, y]
                    if cave[x + 1, y] == 'W':
                        tracker[x, y].append("Stench")
                        print("A stench below")

                    elif cave[x + 1, y] == 'P':
                        tracker[x, y].append("Breeze")
                        print("A breeze below")

                    else:
                        print("Whew.. nothing new below")

                print(tracker)
                if "Stench" in tracker[x, y]:
                    rea.shootWumpus(cave, currentLocation, direction)

                return print(rea.tryToEnter(cave, currentLocation, direction, tracker))

        return print("You found the gold at \n", cave)


    @staticmethod
    def tryToEnter(cave, currentLocation, direction, tracker):
        pickDirection = random.randint(1, 4)
        rea = reasonedExplorer
        x = currentLocation[0]
        y = currentLocation[1]
        obstacleList = []


        # print(direction)
        # if y > 0 or y < caveDim[1] - 1 or x > 0 or x < caveDim[0] - 1:
        if cave[direction[0], direction[1]] == 'W':
            # if explorer dies put F for Fatality
            tracker[direction[0], direction[1]] = obstacleList
            cave[x, y] = 'S'
            tracker[x, y].append("Safe")
            gold = False
            alive = False
            cave[direction[0], direction[1]] = 'F'
            print("You died from Wumpus")
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive)
        elif cave[direction[0], direction[1]] == 'P':
            tracker[direction[0], direction[1]] = obstacleList
            # if explorer dies put F for Fatality
            cave[x, y] = 'S'
            gold = False
            alive = False
            tracker[x, y].append("Safe")
            cave[direction[0], direction[1]] = 'F'
            print("You died from a pit")
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive)
        elif cave[direction[0], direction[1]] == 'B':
            tracker[direction[0], direction[1]] = obstacleList
            tracker[direction[0], direction[1]].append("Blocked")
            gold = False
            alive = True
            print("You cannot go that way")
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive)
        elif cave[direction[0], direction[1]] == 'G':
            tracker[direction[0], direction[1]] = obstacleList
            gold = True
            alive = True
            print("You found the gold!")
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive)
        elif cave[direction[0], direction[1]] == 'D':
            tracker[direction[0], direction[1]] = obstacleList
            tracker[direction[0], direction[1]].append("Dead")
            gold = False
            alive = True
            print("There's a dead Wumpus here!")
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive)
        else:
            tracker[direction[0], direction[1]] = obstacleList
            cave[x, y] = 'S'
            if "Safe" not in tracker[x, y]:
                tracker[x, y].append("Safe")
            tracker[direction[0], direction[1]].append("Safe")
            cave[direction[0], direction[1]] = 'E'
            gold = False
            alive = True
            x = direction[0]
            y = direction[1]
            currentLocation = [x, y]
            print(pickDirection)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive)



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
        arrows = wumpusCount

        if arrows == 0:
            print("You're out of arrows!")
        else:
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

                else:
                    print(cave)
                    print("You hear your arrow hit a wall")
                    arrows -= 1
