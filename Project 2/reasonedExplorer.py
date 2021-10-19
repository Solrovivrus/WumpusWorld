import random
from contextlib import suppress

import numpy as np


class reasonedExplorer:
    """
    This method will take the cave array and use random uniform distribution to
    pick a random place to start the explorer, and also count the wumpi
    to give the explorer the right amount of arrows
    """

    goldFound = 0
    killedByWumpus = 0
    killedByPit = 0
    unsolved = 0
    numberCells = 0
    wumpusKilled = 0

    # --------------------------------------------------------------------------------------------
    # The caveSelection method iterates through all 10 caves generated and sends them to be solved
    # within the simpleExplorer class
    @staticmethod
    def caveSelection(caves):
        rea = reasonedExplorer
        for cave in caves:
            currentCave = rea.placeExplorer(cave)

        print("The explorer found the gold " + str(rea.goldFound) + " times.")
        print("The explorer fell into a pit " + str(rea.killedByPit) + " times")
        print("The explorer was killed by a wumpus " + str(rea.killedByWumpus) + " times")

        return rea.goldFound, rea.killedByPit, rea.killedByWumpus, rea.unsolved, rea.numberCells, rea.wumpusKilled

    @staticmethod
    def placeExplorer(cave):
        rea = reasonedExplorer
        caveDim = np.shape(cave)
        currentLocation = []
        count = 0
        gold = False
        alive = True
        count = 0

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

        pickDirection = rea.decideNextMove(currentLocation, tracker)
        rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows, count)

    @staticmethod
    def track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows, count):
        rea = reasonedExplorer

        # iterating through neighboring cells to see what's possible
        x = currentLocation[0]
        y = currentLocation[1]
        left = [x, y - 1]
        right = [x, y + 1]
        up = [x - 1, y]
        down = [x + 1, y]

        # getting dimensions
        caveDim = np.shape(tracker)
        direction = []
        legalList = []
        legalDirections = []
        if count == 100:
            rea.unsolved += 1
        else:
            count += 1
            for i in range(5000):
                if y > 0:
                    legalList.append("left")
                if y < caveDim[1] - 1:
                    legalList.append("right")
                if x > 0:
                    legalList.append("up")
                if x < caveDim[0] - 1:
                    legalList.append("down")

                nextMove = random.choice(legalList)

                # setting a list to hold
                obstacleList = ["Safe"]
                tracker[x, y] = obstacleList

                # check left - if y = 0... nothing will be to the left of it
                # if a wumpus, assign stench in tracker. if pit, assign breeze
                while not gold:
                    # print(cave)
                    if not alive:
                        return "Your journey ends here"
                    else:
                        if y > 0:
                            if pickDirection == left:
                                direction = left
                            if cave[x, y - 1] == 'W':
                                tracker[x, y].append("Stench")
                                # print("You smell a foul order")

                            elif cave[x, y - 1] == 'P':
                                tracker[x, y].append("Breeze")
                                # print("You feel a breeze")

                        # check right
                        with suppress(IndexError):

                            if y < caveDim[1] - 1:
                                if pickDirection == right:
                                    direction = right
                                if cave[x, y + 1] == 'W':
                                    tracker[x, y].append("Stench")
                                    # print("You smell a foul order")

                                elif cave[x, y + 1] == 'P':
                                    tracker[x, y].append("Breeze")
                                    # print("You feel a breeze")

                        # check top
                        with suppress(IndexError):
                            if x > 0:
                                if pickDirection == up:
                                    direction = up
                                if cave[x - 1, y] == 'W':
                                    tracker[x, y].append("Stench")
                                    # print("You smell a foul order")

                                elif cave[x - 1, y] == 'P':
                                    tracker[x, y].append("Breeze")
                                    # print("You feel a breeze")

                        # check bottom
                        if x < caveDim[0] - 1:
                            if pickDirection == down:
                                direction = down
                            if cave[x + 1, y] == 'W':
                                tracker[x, y].append("Stench")
                                # print("You smell a foul order")

                            elif cave[x + 1, y] == 'P':
                                tracker[x, y].append("Breeze")
                                # print("You feel a breeze")

                        # print(tracker)
                        if "Stench" in tracker[x, y]:
                            cave, arrows = rea.shootWumpus(cave, currentLocation, direction, arrows)

                        if "Blocked" in tracker[legalDirections] or "Dead" in tracker[legalDirections]:
                            legalList.remove(nextMove)
                            nextMove = random.choice(legalList)
                            if nextMove == "left":
                                direction = left
                            elif nextMove == "right":
                                direction = right
                            elif nextMove == "up":
                                direction = up
                            elif nextMove == "down":
                                direction = down

                        if "Breeze" in tracker[x, y]:
                            if tracker[left[0], left[1]-1] != 0 and "Safe" in tracker[left[0], left[1]-1] and y > 0:
                                direction = left
                            elif tracker[right[0], right[1]-1] != 0 and "Safe" in tracker[right[0], right[1]-1] and y < caveDim[1] - 1:
                                direction = right
                            elif tracker[up[0], up[1]-1] != 0 and "Safe" in tracker[up[0], up[1]-1] and x > 0:
                                direction = up
                            elif tracker[down[0], down[1]-1] != 0 and "Safe" in tracker[down[0], down[1]-1] and x < caveDim[0] - 1:
                                direction = down

                        return rea.tryToEnter(cave, currentLocation, direction, tracker, arrows, count)

    @staticmethod
    def tryToEnter(cave, currentLocation, direction, tracker, arrows, count):
        rea = reasonedExplorer
        x = currentLocation[0]
        y = currentLocation[1]
        obstacleList = []
        tracker[direction[0], direction[1]] = obstacleList
        rea.numberCells += 1

        if cave[direction[0], direction[1]] == 'W':
            pickDirection = 0
            # if explorer dies put F for Fatality
            cave[x, y] = 'S'
            tracker[x, y].append("Safe")
            gold = False
            alive = False
            cave[direction[0], direction[1]] = 'F'
            # print("You died from Wumpus")
            rea.killedByWumpus += 1
            # print(cave)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows, count)
        elif cave[direction[0], direction[1]] == 'P':
            pickDirection = 0
            # if explorer dies put F for Fatality
            cave[x, y] = 'S'
            gold = False
            alive = False
            tracker[x, y].append("Safe")
            cave[direction[0], direction[1]] = 'F'
            # print("You died from a pit")
            rea.killedByPit += 1
            # print(cave)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows, count)
        elif cave[direction[0], direction[1]] == 'B':
            tracker[direction[0], direction[1]].append("Blocked")
            gold = False
            alive = True
            # print("You cannot go that way")
            pickDirection = rea.decideNextMove(currentLocation, tracker)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows, count)
        elif cave[direction[0], direction[1]] == 'G':
            pickDirection = 0
            gold = True
            alive = True
            rea.goldFound += 1
            # print("You found the gold at \n", [direction[0], direction[1]])
            # print(cave)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows, count)
        elif cave[direction[0], direction[1]] == 'D':
            tracker[direction[0], direction[1]].append("Dead")
            gold = False
            alive = True
            # print("There's a dead Wumpus here!")
            pickDirection = rea.decideNextMove(currentLocation, tracker)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows, count)
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
            pickDirection = rea.decideNextMove(currentLocation, tracker)
            return rea.track(cave, tracker, currentLocation, pickDirection, gold, alive, arrows, count)

    @staticmethod
    def decideNextMove(currentLocation, tracker):
        legalList = []
        legalDirections = []
        x = currentLocation[0]
        y = currentLocation[1]
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

        return legalDirections

    @staticmethod
    def shootWumpus(cave, currentLocation, direction, arrows):
        rea = reasonedExplorer
        caveDim = np.shape(cave)
        x = currentLocation[0]
        y = currentLocation[1]
        # assigning arrows based on number of wumpi in cave
        # print("You have ", arrows, " arrows")

        if arrows == 0:
            print("You're out of arrows!")
        else:
            while 0 < direction[1] < caveDim[1] - 1 or 0 < direction[0] < caveDim[0] - 1:
                if cave[direction[0], direction[1]] == 'W':
                    # change the wumpus into a dead wumpus
                    cave[direction[0], direction[1]] = 'D'
                    # print("You heard a scream")
                    rea.wumpusKilled += 1
                    arrows -= 1
                    break
                elif cave[direction[0], direction[1]] == 'B':
                    # print("You hear your arrow break")
                    arrows -= 1
                    break
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
                    break

            return cave, arrows
