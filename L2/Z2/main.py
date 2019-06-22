import copy

def copy_state(board, s_index, x):
    new_state = [0, [], s_index, x]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][1] == 1:
                new_state[0] = [i, j]
            if board[i][j][1] == 2:
                new_state[1].append([i, j])
    return new_state

file_in = open('zad2_input.txt', 'r').read().splitlines()

# cell = [x,y]
# x -> rodzaj podlogi pola, 0 -> zwykly tile, 1 -> sciana, 2 -> punkty docelowy
# y -> rodzaj obiektu znajdujacego sie polu, 0 -> brak, 1 -> gracz, 2 -> skrzynia

base_board = []
states = []
start = [0, [], 0, 0]

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
        if file_in[i][j] == '*':
            cell = [2, 0]
            start[1].append([i, j])
        if file_in[i][j] == '+':
            cell = [2, 0]
            start[0] = [i, j]
        line.append(cell)

    base_board.append(line)

# states = [state] -> zapisane dane dla bfs
# state = [pozycja_gracza, pozycje_skrzynek, indeks_poprzedniego_stanu, ostatni_ruch] -> stan gry
# pozycja_gracza = [x,y]
# pozycja_skrzynek = [[x0,y0],[x1,y1],...,[xn,yn]]

s_index = 0
states.append(start)

work = True
while work:

    board = copy.deepcopy(base_board)
    state = states[s_index]

    px = state[0][0]
    py = state[0][1]
    board[px][py][1] = 1

    boxes = state[1]
    for box in boxes:
        board[box[0]][box[1]][1] = 2

    #print(s_index)
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

    #if s_index > 20:
    #    work = False

    for r in range(-1,2,2): #os Y
        if board[px+r][py][0] != 1: #czy nie sciana

            if board[px+r][py][1] == 2 and board[px+r*2][py][0] != 1 and board[px+r*2][py][1] == 0: #przesun skrzynie
                board[px][py][1] = 0
                board[px+r][py][1] = 1
                board[px+r*2][py][1] = 2
                states.append(copy_state(board, s_index,r+1))
                board[px][py][1] = 1
                board[px+r][py][1] = 2
                board[px+r*2][py][1] = 0

            if board[px+r][py][1] == 0: #wejdz na wolne pole
                board[px][py][1] = 0
                board[px+r][py][1] = 1
                states.append(copy_state(board, s_index,r+1))
                board[px][py][1] = 1
                board[px+r][py][1] = 0

    for r in range(-1, 2, 2): #os X
        if board[px][py+r][0] != 1:  # czy nie sciana

            if board[px][py+r][1] == 2 and board[px][py+r*2][0] != 1 and board[px][py+r*2][1] == 0:  # przesun skrzynie
                board[px][py][1] = 0
                board[px][py+r][1] = 1
                board[px][py+r*2][1] = 2
                states.append(copy_state(board, s_index,r+2))
                board[px][py][1] = 1
                board[px][py+r][1] = 2
                board[px][py+r*2][1] = 0

            if board[px][py+r][1] == 0:  # wejdz na wolne pole
                board[px][py][1] = 0
                board[px][py+r][1] = 1
                states.append(copy_state(board, s_index,r+2))
                board[px][py][1] = 1
                board[px][py+r][1] = 0

    s_index = s_index + 1

s_index = s_index - 1
result = []
while s_index > 0:
    state = states[s_index]
    if state[3] == 0:
        result.append('U')
    if state[3] == 1:
        result.append('L')
    if state[3] == 2:
        result.append('D')
    if state[3] == 3:
        result.append('R')
    s_index = state[2]
open('zad2_output.txt', 'w+').write('\n'.join(reversed(result)))
