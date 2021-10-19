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
    def placeExplorer(cave):
        rea = reasonedExplorer
        caveDim = np.shape(cave)
        currentLocation = []
        count = 0
        gold = False
        alive = True

        while count == 0:
            row = random.randint(1, caveDim[0] - 1)
            col = random.randint(1, caveDim[1] - 1)
            if cave[row, col] == '':
                cave[row, col] = 'E'
                currentLocation = [row, col]
                count += 1
            else:
                continue

        # set the amount of arrows
        wumpusCount = 0
        for i in range(len(cave)):
            for j in range(len(cave[0])):
                if cave[i, j] == 'W':
                    wumpusCount += 1
        arrows = wumpusCount

        # initializing tracking cave
        tracker = np.full_like(cave, 0, dtype=object)
        obstacleList = ["Safe"]
        tracker[currentLocation[0], currentLocation[1]] = obstacleList

        pickDirection = rea.decideNextMove(cave, currentLocation, tracker, arrows)
        rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows)

    @staticmethod
    def track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows):
        rea = reasonedExplorer
        # getting dimensions
        caveDim = np.shape(cave)
        direction = []

        # iterating through neighboring cells to see what's possible
        x = currentLocation[0]
        y = currentLocation[1]
        left = [x, y - 1]
        right = [x, y + 1]
        up = [x - 1, y]
        down = [x + 1, y]

        # setting a list to hold
        obstacleList = ["Safe"]
        tracker[x, y] = obstacleList

        # check left - if y = 0... nothing will be to the left of it
        # if a wumpus, assign stench in tracker. if pit, assign breeze
        while not gold:
            print(cave)
            if not alive:
                return "Your journey ends here"
            else:
                if y > 0:
                    if pickDirection == "left":
                        direction = left
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
                        if pickDirection == "right":
                            direction = right
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
                        if pickDirection == "up":
                            direction = up
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
                    if pickDirection == "down":
                        direction = down
                    if cave[x + 1, y] == 'W':
                        tracker[x, y].append("Stench")
                        print("A stench below")

                    elif cave[x + 1, y] == 'P':
                        tracker[x, y].append("Breeze")
                        print("A breeze below")

                    else:
                        print("Whew.. nothing new below")

                print(tracker)

                print(pickDirection)
                return rea.tryToEnter(cave, currentLocation, direction, tracker, arrows)

    @staticmethod
    def tryToEnter(cave, currentLocation, direction, tracker, arrows):
        rea = reasonedExplorer
        x = currentLocation[0]
        y = currentLocation[1]
        obstacleList = []
        print(direction)
        tracker[direction[0], direction[1]] = obstacleList
        print(tracker[x, y])

        # print(direction)
        # if y > 0 or y < caveDim[1] - 1 or x > 0 or x < caveDim[0] - 1:
        if cave[direction[0], direction[1]] == 'W':
            pickDirection = 0
            # if explorer dies put F for Fatality
            cave[x, y] = 'S'
            tracker[x, y].append("Safe")
            gold = False
            alive = False
            cave[direction[0], direction[1]] = 'F'
            print("You died from Wumpus")
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows)
        elif cave[direction[0], direction[1]] == 'P':
            pickDirection = 0
            # if explorer dies put F for Fatality
            cave[x, y] = 'S'
            gold = False
            alive = False
            tracker[x, y].append("Safe")
            cave[direction[0], direction[1]] = 'F'
            print("You died from a pit")
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows)
        elif cave[direction[0], direction[1]] == 'B':
            tracker[direction[0], direction[1]].append("Blocked")
            gold = False
            alive = True
            print("You cannot go that way")
            pickDirection = rea.decideNextMove(cave, currentLocation, tracker, arrows)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows)
        elif cave[direction[0], direction[1]] == 'G':
            pickDirection = 0
            gold = True
            alive = True
            print("You found the gold at \n", [direction[0], direction[1]])
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows)
        elif cave[direction[0], direction[1]] == 'D':
            tracker[direction[0], direction[1]].append("Dead")
            gold = False
            alive = True
            print("There's a dead Wumpus here!")
            pickDirection = rea.decideNextMove(cave, currentLocation, tracker, arrows)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows)
        else:
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
            print(tracker, "LOOK")
            pickDirection = rea.decideNextMove(cave, currentLocation, tracker, arrows)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows)

    @staticmethod
    def decideNextMove(cave, currentLocation, tracker, arrows):
        rea = reasonedExplorer
        legalList = []
        legalDirections = []
        x = currentLocation[0]
        y = currentLocation[1]
        '''obstacleList = []
        tracker[x, y] = obstacleList'''
        caveDim = np.shape(tracker)
        left = [x, y - 1]
        right = [x, y + 1]
        up = [x - 1, y]
        down = [x + 1, y]
        # adding list of possible coordinates
        if y > 0:
            legalList.append("left")
        if y < caveDim[1] - 1:
            legalList.append("right")
        if x > 0:
            legalList.append("up")
        if x < caveDim[0] - 1:
            legalList.append("down")

        nextMove = random.choice(legalList)
        if nextMove == "left":
            legalDirections = left
        elif nextMove == "right":
            legalDirections = right
        elif nextMove == "up":
            legalDirections = up
        elif nextMove == "down":
            legalDirections = down
        print(tracker, "HERE")
        # print(legalDirections)
        print(currentLocation)

        if "Blocked" in tracker[legalDirections] or "Dead" in tracker[legalDirections]:
            legalList.remove(nextMove)
            nextMove = random.choice(legalList)
            # return nextMove
        if "Stench" in tracker[x, y]:  # and "Breeze" not in tracker[currentLocation]
            print("this is happening just not working")
            cave, arrows = rea.shootWumpus(cave, currentLocation, legalDirections, arrows)
            return nextMove
        else:
            return nextMove

    @staticmethod
    def shootWumpus(cave, currentLocation, direction, arrows):
        caveDim = np.shape(cave)
        x = currentLocation[0]
        y = currentLocation[1]
        # assigning arrows based on number of wumpi in cave
        print("You have ", arrows, " arrows")

        if arrows == 0:
            print("You're out of arrows!")
        else:
            # direction[1] > 0 and direction[1] < caveDim[1] - 1 and direction[0] > 0 and direction[0] < caveDim[0] - 1:
            while 0 < direction[1] < caveDim[1] - 1 and 0 < direction[0] < caveDim[0] - 1:
                if cave[direction[0], direction[1]] == 'W':
                    # change the wumpus into a dead wumpus
                    cave[direction[0], direction[1]] = 'D'
                    print("You heard a scream")
                    arrows -= 1
                    break
                elif cave[direction[0], direction[1]] == 'B':
                    print("You hear your arrow break")
                    arrows -= 1
                    break
# elif cave[direction[0], direction[1]] == '' or cave[direction[0], direction[1]] == 'P' or cave[direction[0], direction[1]] == 'G':
                else:
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

                if 0 > direction[1] > caveDim[1] - 1 and 0 > direction[0] > caveDim[0] - 1:
                    print("You hear your arrow hit a wall")
                    arrows -= 1

            return arrows, cave
