from collections import defaultdict
from random import shuffle
from copy import deepcopy

file_in = open('zad_input.txt', 'r').read().splitlines()

walls = defaultdict(lambda: False)
goals = set()
starting_points = set()

row_len = len(file_in)
col_len = len(file_in[0])


for i in range(row_len):
    for j in range(col_len):
        temp = file_in[i][j]
        if temp == '#':
            walls[(i, j)] = True
        if temp == 'G':
            goals.add((i, j))
        if temp == 'S':
            starting_points.add((i, j))
        if temp == 'B':
            goals.add((i, j))
            starting_points.add((i, j))



def move(state, direction):
    res = set()

    x_mod = 0
    y_mod = 0

    if direction == 'U':
        x_mod = -1

    if direction == 'D':
        x_mod = 1

    if direction == 'L':
        y_mod = -1

    if direction == 'R':
        y_mod = 1

    for s in state:
        x = s[0]
        y = s[1]

        if not walls[(x + x_mod, y + y_mod)]:
            res.add((x + x_mod, y + y_mod))
        else:
            res.add((x, y))

    return res


work = True
result = []
while work:
    state1 = deepcopy(starting_points)
    counter = 0
    path = ''

    while counter <= 50:
        moves = []
        for m in ['U', 'L', 'D', 'R']:
            state2 = move(state1, m)
            moves.append((state2, len(state2), m))

        shuffle(moves)
        state2, _, m = min(moves, key=lambda t: t[1])
        path += m
        state1 = state2
        counter += 1
        if len(state2) <= 2:
            break

    states = [[state1, '']]
    already_done = set()

    while work and counter <= 150:
        min_size = len(min(states, key=lambda t: len(t[0]))[0])
        moves = []

        for s in states:
            if len(s[0]) == min_size:
                moves.append(s)

        if moves != states:
            states = moves
            continue

        for [state, history] in states:
            if (state.difference(goals)) == set():
                result = path + history
                work = False

        new_state = []
        for [state, history] in states:
            for m in ['U', 'D', 'L', 'R']:
                state2 = move(state, m)
                if tuple(state2) not in already_done:
                    new_state.append([state2, history + m])
                    already_done.add(tuple(state2))

        states = new_state
        counter += 1

open('zad_output.txt', 'w+').write(result)
