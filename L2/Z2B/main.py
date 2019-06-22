import copy
import math

base_board = []
goals = []
states = []
path = {}
gpath = {}
mirror = {}


def deep(boxes, depth, taken):
    s = 1000000
    if depth < len(boxes):
        for i in range(len(goals)):
            if not taken[i]:
                taken[i] = True

                mn = gpath[(boxes[depth][0],boxes[depth][1],i)]
                mn = mn + deep(boxes, depth+1, taken)
                if mn < s:
                    s = mn

                taken[i] = False
    else:
        return 0
    return s


def heuristic(boxes):
    s = 0
    global goals
    for box in boxes:
        mx = 100000
        for goal in goals:
            if abs(goal[0] - box[0]) + abs(goal[1] - box[1]) < mx:
                mx = abs(goal[0] - box[0]) + abs(goal[1] - box[1])
        s = s + mx
    return s


def check_mirror(px, py, boxes, xbox, ybox, depth):
    state_tuple = (px, py)
    for box in boxes:
        if px == box[0] and py == box[1]:
            state_tuple = state_tuple + (xbox, ybox)
        else:
            state_tuple = state_tuple + tuple(box)
    if state_tuple not in mirror:
        mirror[state_tuple] = depth
        return True
    else:
        if mirror[state_tuple] <= depth:
            return False
        else:
            mirror[state_tuple] = depth;
            return True


def copy_state(board, s_index, x, index, depth):
    new_state = [0, [], s_index, x, index, depth, 0]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][1] == 1:
                new_state[0] = [i, j]
            if board[i][j][1] == 2:
                new_state[1].append([i, j])

    mn = 10000
    for i in range(len(new_state[1])):
        if path[(new_state[0][0],new_state[0][1],new_state[1][i][0],new_state[1][i][1])] < mn:
            mn = path[(new_state[0][0],new_state[0][1],new_state[1][i][0],new_state[1][i][1])]

    taken = []
    for i in range(len(goals)):
        taken.append(False)
    #print(new_state[0],mn)
    new_state[6] = deep(new_state[1],0,taken) + depth + mn
    return new_state


file_in = open('zad2_input.txt', 'r').read().splitlines()

# cell = [x,y]
# x -> rodzaj podlogi pola, 0 -> zwykly tile, 1 -> sciana, 2 -> punkty docelowy
# y -> rodzaj obiektu znajdujacego sie polu, 0 -> brak, 1 -> gracz, 2 -> skrzynia

start = [0, [], 0, 0, 0, 0, 0]

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

#liczymy sciezki z kazdego punktu na mapie do kazdego pola

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
                        if board[px + r][py][1] == 0 and entered[((px + r),py)] != -1:  # wejdz na wolne pole
                            board[px][py][1] = 0
                            board[px + r][py][1] = 1
                            states.append([px + r, py, depth + 1])
                            entered[((px+r),py)] = -1
                            board[px][py][1] = 1
                            board[px + r][py][1] = 0

                for r in range(-1, 2, 2):  # os X
                    if board[px][py + r][0] != 1:  # czy nie sciana
                        if board[px][py + r][1] == 0 and entered[(px,(py + r))] != -1:  # wejdz na wolne pole
                            board[px][py][1] = 0
                            board[px][py + r][1] = 1
                            states.append([px, py + r, depth + 1])
                            entered[(px,(py+r))] = -1
                            board[px][py][1] = 1
                            board[px][py + r][1] = 0

                s_index = s_index + 1

# states = [state] -> zapisane dane dla bfs
# state = [pozycja_gracza, pozycje_skrzynek, indeks_poprzedniego_stanu, ostatni_ruch, depth, koszt] -> stan gry
# pozycja_gracza = [x,y]
# pozycja_skrzynek = [[x0,y0],[x1,y1],...,[xn,yn]]
n_index = 1

start[6] = heuristic(start[1])
states.clear()
states = []
states.append(start)

g_index = 0

work = True

while work:
    #states = sorted(states, key = lambda x: x[6])
    states.sort(key = lambda x: x[6])
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

    #print(index)
    #for line in board:
    #    print(line)
    #print()

    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == [2,1] or board[i][j] == [2,0]:
                count = count + 1

    if count == 0:
        work = False
        g_index = index

    for r in range(-1,2,2): #os Y
        if board[px+r][py][0] != 1: #czy nie sciana

            if board[px+r][py][1] == 2 and board[px+r*2][py][0] != 1 and board[px+r*2][py][1] == 0: #przesun skrzynie
                if check_mirror(px+r, py, boxes, px+r*2, py, depth):
                    board[px][py][1] = 0
                    board[px+r][py][1] = 1
                    board[px+r*2][py][1] = 2
                    states.append(copy_state(board, index, r+1, n_index, depth+1))
                    n_index = n_index + 1
                    board[px][py][1] = 1
                    board[px+r][py][1] = 2
                    board[px+r*2][py][1] = 0

            if board[px+r][py][1] == 0: #wejdz na wolne pole
                if check_mirror(px + r, py, boxes, -1, -1, depth):
                    board[px][py][1] = 0
                    board[px+r][py][1] = 1
                    states.append(copy_state(board, index, r+1, n_index, depth+1))
                    n_index = n_index + 1
                    board[px][py][1] = 1
                    board[px+r][py][1] = 0

    for r in range(-1, 2, 2): #os X
        if board[px][py+r][0] != 1:  # czy nie sciana

            if board[px][py+r][1] == 2 and board[px][py+r*2][0] != 1 and board[px][py+r*2][1] == 0:  # przesun skrzynie
                if check_mirror(px, py+r, boxes, px, py+r*2, depth):
                    board[px][py][1] = 0
                    board[px][py+r][1] = 1
                    board[px][py+r*2][1] = 2
                    states.append(copy_state(board, index, r+2, n_index, depth+1))
                    n_index = n_index + 1
                    board[px][py][1] = 1
                    board[px][py+r][1] = 2
                    board[px][py+r*2][1] = 0

            if board[px][py+r][1] == 0:  # wejdz na wolne pole
                if check_mirror(px, py + r, boxes, -1, -1, depth):
                    board[px][py][1] = 0
                    board[px][py+r][1] = 1
                    states.append(copy_state(board, index, r+2, n_index, depth+1))
                    n_index = n_index + 1
                    board[px][py][1] = 1
                    board[px][py+r][1] = 0

states = sorted(states, key = lambda x: x[4])
result = []
while g_index > 0:
    state = states[g_index]
    if state[3] == 0:
        result.append('U')
    if state[3] == 1:
        result.append('L')
    if state[3] == 2:
        result.append('D')
    if state[3] == 3:
        result.append('R')
    g_index = state[2]
open('zad2_output.txt', 'w+').write('\n'.join(reversed(result)))
