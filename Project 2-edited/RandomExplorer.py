import numpy as np
import random as random

''' Contributors: Max Kuttner
----------------------------------------------------------------------------------------------
Random Explorer is a stochastic method of traversing the cave. It will be compared
    against the Reasoned Explorer to make inferences about their efficiencies. This version
    chooses paths randomly and will only backtrack to an explored path if there are no new adjacent
    ones, or the only new path is blocked.
----------------------------------------------------------------------------------------------
'''


class RandomExplorer:

    row = 0
    col = 0
    arrows = 0

    @staticmethod
    def place_explorer(cave):
        global row, col, arrows
        cave_dim = np.shape(cave)
        arrows = (np.char.count(cave, 'W'))
        arrows = np.count_nonzero(arrows == 1)
        count = 0
        while count == 0:
            row_choice = random.randint(1, cave_dim[0] - 1)
            col_choice = random.randint(1, cave_dim[1] - 1)
            row = row_choice
            col = col_choice
            if cave[row_choice, col_choice] == '':
                cave[row_choice, col_choice] = 'E'
                count += 1
            else:
                continue
        for n in cave:
            for i in range(0, len(n)):
                if n[i] == '':
                    n[i] = ' '
        print(cave)
        for n in cave:
            for i in range(0, len(n)):
                if n[i] == ' ':
                    n[i] = ''
        return cave

    @staticmethod
    def explore(cave):
        adjacent = []
        possible = []
        end_states = ['G', 'P', 'W']

        # --------------------------------------------------------------------------------------------------------------
        #   Checks explorers current position against 'end' states.
        def current_state():
            if cave[row, col] == 'G':
                print("Explorer has found the gold!")
            if cave[row, col] == 'W':
                print('Explorer has been killed by a wumpus!')
            if cave[row, col] == 'P':
                print('Explorer has fallen into a pit!')
            if cave[row, col] not in end_states:
                cave[row, col] = 'E'

        # --------------------------------------------------------------------------------------------------------------
        #   Updates list of adjacent cells. If statements ensure that no index error occurs.
        def update_adjacent():
            adjacent.clear()
            for n in range(0, 4):  adjacent.insert(n, ('', ''))
            if row != len(cave[:, 0]) - 1:
                adjacent[0] = (row + 1, col)
            if col != 0:
                adjacent[1] = (row, col - 1)
            if row != 0:
                adjacent[2] = (row - 1, col)
            if col != len(cave[0]) - 1:
                adjacent[3] = (row, col + 1)

        # --------------------------------------------------------------------------------------------------------------
        #   Updates adjacent list with possible(moves) list. This acts as a 'Dictionary' of sorts, since indexes are ==
        def info():
            possible.clear()
            for n in range(0, 4):  possible.insert(n, ' ')
            n = 0
            for i in adjacent:
                if adjacent[n] == ('', ''):
                    n += 1
                else:
                    possible[n] = cave[i]
                    n += 1

        # --------------------------------------------------------------------------------------------------------------
        #   Carries out movement for explorer. randomly choosing a cell to go to.
        def move(i):
            global row, col
            if possible[i] == 'B':
                print('Explorer ran into a wall...')
                return
            cave[row, col] = 'X'
            if possible[i] == 'X':                  # if the desired move state is 'X' that means there are no new paths
                changed = True                      # so randomly choose one of the cells with 'X' in it.
                while changed:
                    n = random.randint(0, 3)
                    if possible[n] == 'X':
                        row, col = adjacent[n]
                        cave[row, col] = 'E'
                        return
            row, col = adjacent[i]

        # --------------------------------------------------------------------------------------------------------------
        #   Decides what the explorer will do. Features the logic behind explorers actions.
        def action():
            global arrows

            # Function for randomly chooses an adjacent square to move to.
            def choose_random():
                bad_states = ['X', ' ']
                count = 0
                for k in possible:
                    if k in bad_states:
                        count += 1
                b = possible.count('B')
                if count == 4 or b + count == 4:
                    changed = True
                    while changed:
                        j = random.randint(0, 3)
                        if possible[j] == 'X':
                            move(j)
                            return
                else:
                    changed = True
                    while changed:
                        j = random.randint(0, 3)
                        if possible[j] not in bad_states:
                            move(j)
                            return

            if 'W' in possible and arrows != 0:
                shot = random.randint(0, len(adjacent)-1)
                if possible[shot] == 'W':
                    cave[adjacent[shot]] = ''
                    possible[shot] = ''
                    print('A loud scream rings out through the cave...')
                    arrows -= 1
                    move(shot)
                else:
                    print('The arrow misses its mark...')
                    arrows -= 1
                    choose_random()
            else:
                choose_random()

        # --------------------------------------------------------------------------------------------------------------
        #   Loop that runs until explorer reaches an "end" state. ('G', 'W', or 'P')
        while cave[row, col] not in end_states:
            update_adjacent()
            info()
            action()
            current_state()
        cave[row, col] = 'E'

        for n in cave:
            for i in range(0, len(n)):
                if n[i] == '':
                    n[i] = ' '

        print(cave)
