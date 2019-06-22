import copy
import math

base_board = []
goals = []
path = {}
gpath = {}
mirror = {}


def bfs(base_board1, boxes, sx, sy):
    moves = []
    if base_board1[sx][sy][0] != 1:
        bfs_start = [sx, sy]
        states1 = [bfs_start]
        s_index = 0

        for i in range(len(boxes)):
            moves.append([])
            for j in range(4):
                moves[i].append(False)

        entered = {}
        entered.clear()

        while s_index < len(states1):
            state = states1[s_index]
            board = copy.deepcopy(base_board1)
            px = state[0]
            py = state[1]

            for r in range(-1, 2, 2):  # os Y
                if board[px + r][py][1] == 2 and board[px+r*2][py][0] != 1 and board[px+r*2][py][1] != 2: #zapisz mozliwy ruch
                    bn = 0
                    for i in range(len(boxes)):
                        if boxes[i][0] == px + r and boxes[i][1] == py:
                              bn = i
                    moves[bn][r+1] = True

                if board[px + r][py][0] != 1:  # czy nie sciana
                    if board[px + r][py][1] == 0 and ((px + r), py) not in entered:  # wejdz na wolne pole
                        board[px][py][1] = 0
                        board[px + r][py][1] = 1
                        states1.append([px + r, py])
                        entered[((px + r), py)] = -1
                        board[px][py][1] = 1
                        board[px + r][py][1] = 0

            for r in range(-1, 2, 2):  # os X
                if board[px][py+r][1] == 2 and board[px][py+r*2][0] != 1 and board[px][py+r*2][1] != 2: #zapisz mozliwy ruch
                    bn = 0
                    for i in range(len(boxes)):
                        if boxes[i][0] == px and boxes[i][1] == py + r:
                              bn = i
                    moves[bn][r+2] = True

                if board[px][py + r][0] != 1:  # czy nie sciana
                    if board[px][py + r][1] == 0 and (px, (py + r)) not in entered:  # wejdz na wolne pole
                        board[px][py][1] = 0
                        board[px][py + r][1] = 1
                        states1.append([px, py + r])
                        entered[(px, (py + r))] = -1
                        board[px][py][1] = 1
                        board[px][py + r][1] = 0

            s_index = s_index + 1

    return moves


def check_mirror(px, py, xbox, ybox, boxes, moves):
    state_tuple = ()

    for box in boxes:
        if px == box[0] and py == box[1]:
            state_tuple = state_tuple + (xbox, ybox)
        else:
            state_tuple = state_tuple + tuple(box)

    for move in moves:
        state_tuple = state_tuple + tuple(move)

    if state_tuple not in mirror:
        mirror[state_tuple] = True
        return True
    else:
        return False


def deep(boxes, depth, taken):
    s = 1000000
    if depth < len(boxes):
        for i in range(len(goals)):
            if not taken[i]:
                taken[i] = True

                if (boxes[depth][0],boxes[depth][1],i) in gpath:
                    mn = gpath[(boxes[depth][0],boxes[depth][1],i)]
                    mn = mn + deep(boxes, depth+1, taken)
                    if mn < s:
                        s = mn

                taken[i] = False
    else:
        return 0
    return s


def copy_state(boxes, s_index, move, index, depth):
    mbox = move[0]
    direction = move[1]
    new_state = [0, [], s_index, move, index, depth, 0]
    px = boxes[mbox][0]
    py = boxes[mbox][1]
    new_state[0] = [px,py]
    new_state[1] = copy.deepcopy(boxes)

    if direction == 0:
        new_state[1][mbox][0] = new_state[1][mbox][0] - 1
    if direction == 1:
        new_state[1][mbox][1] = new_state[1][mbox][1] - 1
    if direction == 2:
        new_state[1][mbox][0] = new_state[1][mbox][0] + 1
    if direction == 3:
        new_state[1][mbox][1] = new_state[1][mbox][1] + 1

    taken = []
    for i in range(len(goals)):
        taken.append(False)

    new_state[6] = deep(new_state[1],0,taken)
    return new_state

start = [0, [], -1, 0, 0, 0, 0]
file_in = open('zad_input.txt', 'r').read().splitlines()

for i in range(len(file_in)):

    line = []
    cell = []

    for j in range(len(file_in[i])):
        if file_in[i][j] == 'W':
            cell = [1, 0]
        if file_in[i][j] == '.':
            cell = [0, 0]
        if file_in[i][j] == 'K':
            cell = [0, 0]
            start[0] = [i, j]
        if file_in[i][j] == 'B':
            cell = [0, 0]
            start[1].append([i, j])
        if file_in[i][j] == 'G':
            cell = [2, 0]
            goals.append([i, j])
        if file_in[i][j] == '*':
            cell = [2, 0]
            start[1].append([i, j])
            goals.append([i, j])
        if file_in[i][j] == '+':
            cell = [2, 0]
            start[0] = [i, j]
            goals.append([i, j])
        line.append(cell)

    base_board.append(line)

#liczymy sciezki z kazdego punktu na mapie do kazdego pola dla boksow

states = []

for i in range(len(base_board)):
    for j in range(len(base_board[i])):
        if base_board[i][j][0] != 1:
            bfs_start = [i,j,0]
            states.clear()
            states.append(bfs_start)
            s_index = 0
            t_found = []
            t_found.clear()
            entered = {}
            entered.clear()

            for w in range(0,99):
                for e in range(0, 99):
                    entered[(w,e)] = 0
                    path[(i,j,w,e)] = 100000

            for w in range(len(goals)):
                t_found.append(False)

            while s_index < len(states):
                state = states[s_index]
                board = copy.deepcopy(base_board)
                px = state[0]
                py = state[1]
                depth = state[2]
                path[(i,j,px,py)] = depth

                for g in range(len(goals)):
                    if px == goals[g][0] and py == goals[g][1]:
                        if not t_found[g]:
                            gpath[(i,j,g)] = depth
                            t_found[g] = True

                for r in range(-1, 2, 2):  # os Y
                    if board[px + r][py][0] != 1:  # czy nie sciana
                        if board[px + r][py][1] == 0 and board[px - r][py][0] != 1 and board[px - r][py][1] == 0 and entered[((px + r),py)] != -1:  # wejdz na wolne pole
                            board[px][py][1] = 0
                            board[px + r][py][1] = 1
                            states.append([px + r, py, depth + 1])
                            entered[((px+r),py)] = -1
                            board[px][py][1] = 1
                            board[px + r][py][1] = 0

                for r in range(-1, 2, 2):  # os X
                    if board[px][py + r][0] != 1:  # czy nie sciana
                        if board[px][py + r][1] == 0 and board[px][py-r][0] != 1 and board[px][py-r][1] == 0 and entered[(px,(py + r))] != -1:  # wejdz na wolne pole
                            board[px][py][1] = 0
                            board[px][py + r][1] = 1
                            states.append([px, py + r, depth + 1])
                            entered[(px,(py+r))] = -1
                            board[px][py][1] = 1
                            board[px][py + r][1] = 0

                s_index = s_index + 1

# states = [state] -> zapisane dane dla bfs
# state = [pozycja_gracza, pozycje_skrzynek, indeks_poprzedniego_stanu, ostatni_ruch, obecny_indeks, depth, koszt] -> stan gry
# pozycja_gracza = [x,y]
# pozycja_skrzynek = [[x0,y0],[x1,y1],...,[xn,yn]]
# lista_ruchow = [[x,a],[x,b],[y,a]...] | [x,a] -> skrzynka[x] ruch w strone a.
n_index = 1

states = []
states.append(start)

g_index = 0
work = True

while work:

    states.sort(key=lambda x: x[6])
    #print()
    #print(states)
    #print()

    board = copy.deepcopy(base_board)
    state = states[0]
    state[6] = 1000000

    px = state[0][0]
    py = state[0][1]
    board[px][py][1] = 1
    index = state[4]
    depth = state[5]

    boxes = state[1]
    for box in boxes:
        board[box[0]][box[1]][1] = 2

    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == [2, 1] or board[i][j] == [2, 0]:
                count = count + 1

    if count == 0:
        work = False
        g_index = index

    moves = bfs(board, boxes, px, py)

    #print(index)
    #for line in board:
    #    print(line)
    #print()

    for i in range(len(moves)):
        for j in range(len(moves[i])):
            if moves[i][j]:
                if j == 0 and check_mirror(boxes[i][0], boxes[i][1], boxes[i][0] - 1, boxes[i][1], boxes, moves):
                    states.append(copy_state(boxes, index, [i, j], n_index, depth + 1))
                    n_index = n_index + 1

                if j == 1 and check_mirror(boxes[i][0], boxes[i][1], boxes[i][0], boxes[i][1] - 1, boxes, moves):
                    states.append(copy_state(boxes, index, [i, j], n_index, depth + 1))
                    n_index = n_index + 1

                if j == 2 and check_mirror(boxes[i][0], boxes[i][1], boxes[i][0] + 1, boxes[i][1], boxes, moves):
                    states.append(copy_state(boxes, index, [i, j], n_index, depth + 1))
                    n_index = n_index + 1

                if j == 3 and check_mirror(boxes[i][0], boxes[i][1], boxes[i][0], boxes[i][1] + 1, boxes, moves):
                    states.append(copy_state(boxes, index, [i, j], n_index, depth + 1))
                    n_index = n_index + 1

states = sorted(states, key = lambda x: x[4])
result = []

while g_index > 0:
    pxd = state[0][0]
    pyd = state[0][1]
    if state[3][1] == 0:
        result.append('U')
        pxd = pxd + 1
    if state[3][1] == 1:
        result.append('L')
        pyd = pyd + 1
    if state[3][1] == 2:
        result.append('D')
        pxd = pxd - 1
    if state[3][1] == 3:
        result.append('R')
        pyd = pyd - 1
    g_index = state[2]
    state = states[g_index]

    boxes = state[1]
    board = copy.deepcopy(base_board)
    for box in boxes:
        board[box[0]][box[1]][1] = 2

    bfs_start = [state[0][0], state[0][1], 0]
    states1 = [bfs_start]
    s_index = 0

    entered = {}
    entered.clear()

    for w in range(0, 99):
        for e in range(0, 99):
            entered[(w, e)] = -1

    entered[(state[0][0], state[0][1])] = 0

    work = True
    #print(state[0][0], state[0][1], pxd, pyd)
    while work:
        #print(px, py, states1)
        state1 = states1[s_index]
        px = state1[0]
        py = state1[1]
        depth = state1[2]

        if px == pxd and py == pyd:
            work = False

        for r in range(-1, 2, 2):  # os Y
            if board[px + r][py][0] != 1:  # czy nie sciana
                if board[px + r][py][1] == 0 and entered[((px + r), py)] < 0:  # wejdz na wolne pole
                    board[px][py][1] = 0
                    board[px + r][py][1] = 1
                    states1.append([px + r, py, depth + 1])
                    entered[((px + r), py)] = depth+1
                    board[px][py][1] = 1
                    board[px + r][py][1] = 0

        for r in range(-1, 2, 2):  # os X
            if board[px][py + r][0] != 1:  # czy nie sciana
                if board[px][py + r][1] == 0 and entered[(px, (py + r))] < 0:  # wejdz na wolne pole
                    board[px][py][1] = 0
                    board[px][py + r][1] = 1
                    states1.append([px, py + r, depth + 1])
                    entered[(px, (py + r))] = depth+1
                    board[px][py][1] = 1
                    board[px][py + r][1] = 0

        s_index = s_index + 1

    while entered[(pxd,pyd)] > 0:
        #print(pxd,pyd, entered[(pxd,pyd)])
        if entered[(pxd - 1, pyd)] >= 0 and entered[(pxd - 1, pyd)] < entered[(pxd, pyd)]:
            result.append('D')
            pxd = pxd - 1
        if entered[(pxd + 1, pyd)] >= 0 and entered[(pxd + 1, pyd)] < entered[(pxd, pyd)]:
            result.append('U')
            pxd = pxd + 1
        if entered[(pxd, pyd - 1)] >= 0 and entered[(pxd, pyd - 1)] < entered[(pxd, pyd)]:
            result.append('R')
            pyd = pyd - 1
        if entered[(pxd, pyd + 1)] >= 0 and entered[(pxd, pyd + 1)] < entered[(pxd, pyd)]:
            result.append('L')
            pyd = pyd + 1

result.reverse()
open('zad_output.txt', 'w+').write(''.join(result))