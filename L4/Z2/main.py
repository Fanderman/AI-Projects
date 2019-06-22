import random
from copy import deepcopy

def new_board():
    board = []
    for i in range(9):
        board.append([])
        for j in range(7):
            board[i].append([0, 0])

    board[0][2][0] = 2
    board[0][3][0] = 3
    board[0][4][0] = 2
    board[1][3][0] = 2

    board[3][1][0] = 1
    board[3][2][0] = 1
    board[3][4][0] = 1
    board[3][5][0] = 1

    board[4][1][0] = 1
    board[4][2][0] = 1
    board[4][4][0] = 1
    board[4][5][0] = 1

    board[5][1][0] = 1
    board[5][2][0] = 1
    board[5][4][0] = 1
    board[5][5][0] = 1

    board[7][3][0] = 2
    board[8][2][0] = 2
    board[8][3][0] = -3
    board[8][4][0] = 2

    board[2][0][1] = 1
    board[1][5][1] = 2
    board[1][1][1] = 3
    board[2][4][1] = 4
    board[2][2][1] = 5
    board[0][6][1] = 6
    board[0][0][1] = 7
    board[2][6][1] = 8

    board[6][6][1] = -1
    board[7][1][1] = -2
    board[7][5][1] = -3
    board[6][2][1] = -4
    board[6][4][1] = -5
    board[8][0][1] = -6
    board[8][6][1] = -7
    board[6][0][1] = -8

    return board


def show(board):
    for row in board:
        line = ''
        for l in row:
            if l[1] == 0:
                if l[0] == 0:
                    line += '.'
                if l[0] == 1:
                    line += '-'
                if l[0] == 2:
                    line += '#'
                if abs(l[0]) == 3:
                    line += '*'

            if l[1] == 1:
                line += 'R'
            if l[1] == 2:
                line += 'C'
            if l[1] == 3:
                line += 'D'
            if l[1] == 4:
                line += 'W'
            if l[1] == 5:
                line += 'J'
            if l[1] == 6:
                line += 'T'
            if l[1] == 7:
                line += 'L'
            if l[1] == 8:
                line += 'E'

            if l[1] == -1:
                line += 'r'
            if l[1] == -2:
                line += 'c'
            if l[1] == -3:
                line += 'd'
            if l[1] == -4:
                line += 'w'
            if l[1] == -5:
                line += 'j'
            if l[1] == -6:
                line += 't'
            if l[1] == -7:
                line += 'l'
            if l[1] == -8:
                line += 'e'
        print(line)
    print()


def correct(x, y):
    return 0 <= x < 9 and 0 <= y < 7


def check_pos(board, p, i, j, di, dj):
    if correct(i + di, j + dj):
        if board[i][j][1]*p == 1:
            if board[i][j][0] == 0 and board[i + di][j + dj][0] == 0 and board[i + di][j + dj][0] != 3*p and (
                    board[i + di][j + dj][1]*p == -8 or board[i + di][j + dj][1]*p == -1 or board[i + di][j + dj][1]*p == 0):
                return [i, j, i + di, j + dj]

            if board[i][j][0] == 0 and board[i + di][j + dj][0] == 1 and board[i + di][j + dj][1]*p == 0:
                return [i, j, i + di, j + dj]

            if board[i][j][0] == 1 and board[i + di][j + dj][0] == 1 and (
                    board[i + di][j + dj][1]*p == 0 or board[i + di][j + dj][1]*p == -1):
                return [i, j, i + di, j + dj]

            if board[i + di][j + dj][0] == 2 and board[i + di][j + dj][1]*p <= 0:
                return [i, j, i + di, j + dj]

        if 2 <= board[i][j][1]*p <= 8:
            if board[i + di][j + dj][0] != 1 and board[i + di][j + dj][1]*p <= 0 and abs(board[i + di][j + dj][1]) <= \
                    board[i][j][1]*p and board[i + di][j + dj][0] != 3*p and not(board[i + di][j + dj][1]*p == -1 and board[i][j][1]*p == 8):
                return [i, j, i + di, j + dj]

            if board[i + di][j + dj][0] == 2 and board[i + di][j + dj][1]*p <= 0 and board[i + di][j + dj][0] != 3*p:
                return [i, j, i + di, j + dj]

            if 6 <= board[i][j][1]*p <= 7 and board[i + di][j + dj][0] == 1 and abs(board[i + di][j + dj][1]) != 1:
                multi = 2
                while correct(i + di*multi, j + dj*multi) and board[i + di*multi][j + dj*multi][0] == 1 and \
                        abs(board[i + di*multi][j + dj*multi][1]) != 1:
                    multi += 1
                if correct(i + di*multi, j + dj*multi) and board[i + di*multi][j + dj*multi][0] != 1 and \
                        board[i + di*multi][j + dj*multi][1]*p <= 0 and abs(board[i + di*multi][j + dj*multi][1]) <= board[i][j][1]*p:
                    return [i, j, i + di*multi, j + dj*multi]

    return None


def generate_moves(board, player):
    if board[0][3][1] != 0 or board[8][3][1] != 0:
        return None

    moves = []
    for i in range(9):
        for j in range(7):
            res = check_pos(board, player, i, j, 0, 1)
            if res is not None:
                moves.append(res)
            res = check_pos(board, player, i, j, 0, -1)
            if res is not None:
                moves.append(res)
            res = check_pos(board, player, i, j, -1, 0)
            if res is not None:
                moves.append(res)
            res = check_pos(board, player, i, j, 1, 0)
            if res is not None:
                moves.append(res)
    return moves


def random_player(board, player):
    options = generate_moves(board, player)
    if options is not None and len(options) > 0:
        return random.choice(options)
    return None


def bot_simulation(board, player, turn):
    won = 0
    while won == 0 and turn < 60:
        won = check_win(board)
        move = random_player(board, player)
        board = resolve(board, move)

        turn += 1
        player = -player

    if won == 0:
        won = -1
        pieces = set()
        for row in board:
            for spot in row:
                pieces.add(spot[1])

        for i in range(8, 0, -1):
            if i in pieces and -i not in pieces:
                won = 1
                break
            if -i in pieces and i not in pieces:
                won = -1
                break

    return won, turn


def botA(board, player, turn):
    options = generate_moves(board, player)
    info = []
    for move in options:
        current_board = resolve(deepcopy(board), move)
        info.append([move, current_board, 0, 0])

    total = 0
    while True:
        for i in range(len(info)):
            if total > 10000:
                mx = -1
                res = None
                for x in info:
                    #print(x)
                    if x[2]/x[3] > mx:
                        mx = x[2]/x[3]
                        res = x[0]
                return res

            res, t_a = bot_simulation(deepcopy(info[i][1]), deepcopy(player), deepcopy(turn))
            total += t_a-turn + 1
            if res == player:
                info[i][2] += 1
            info[i][3] += 1


def end_heuristic(board, player):
    end_x = 0
    end_y = 3
    if player == 1:
        end_x = 8

    dist = 1000
    for i in range(9):
        for j in range(7):
            if board[i][j][1]*player > 0:
                new_dist = abs(i-end_x) + abs(j-end_y)
                if new_dist < dist:
                    dist = new_dist

    if dist == 0:
        return 1000
    return -dist


def pieces_heuristic(board, player):
    sum = 0

    for i in range(9):
        for j in range(7):
            if board[i][j][1]*player > 0:
                sum += board[i][j][1]*player

    return sum


def battle_heuristic(board, player):
    positions = {}
    score = 0

    for i in range(9):
        for j in range(7):
            if board[i][j][1] != 0:
                positions[board[i][j][1]] = (i, j)

    for i in range(1, 9):
        if i*player in positions:
            x = positions[i*player][0]
            y = positions[i*player][1]
            dist = 1000
            closest = 1
            for j in range(1, 9):
                if j*player*-1 in positions:
                    ex = positions[j*player*-1][0]
                    ey = positions[j*player*-1][1]
                    new_dist = abs(ex-x) + abs(ey-y)
                    if new_dist < dist:
                        dist = new_dist
                        closest = j

            multiplier = 1/dist
            if i == 1:
                if closest == 8:
                    score += multiplier*8
                else:
                    score -= multiplier*1

            if i == 8:
                if closest == 1:
                    score -= multiplier*8
                else:
                    score += multiplier*closest

            if 1 < i < 8:
                if closest > i:
                    score -= multiplier*i
                else:
                    score += multiplier*closest

    return score


def total_heuristic(board, player):
    player_score = 0
    opponent_score = 0

    player_score += end_heuristic(board, player)*1
    player_score += pieces_heuristic(board, player)*5
    player_score += battle_heuristic(board, player)*2

    opponent_score += end_heuristic(board, -player)*1
    opponent_score += pieces_heuristic(board, -player)*5
    opponent_score += battle_heuristic(board, -player)*2

    return player_score - opponent_score


def minimax(board, player, depth, maxing):
    options = generate_moves(board, player)
    if depth == 0 or options is None:
        return [total_heuristic(board, player), (-1, -1)]

    if not maxing:
        best_move = (-1, -1)
        value = 100000
        for move in options:
            current_board = resolve(deepcopy(board), move)
            res = minimax(current_board, -player, depth - 1, True)
            if res[0] < value:
                value = res[0]
                best_move = deepcopy(move)

    else:
        best_move = (-1, -1)
        value = -100000
        for move in options:
            current_board = resolve(deepcopy(board), move)
            res = minimax(current_board, -player, depth - 1, False)
            if res[0] > value:
                value = res[0]
                best_move = deepcopy(move)

    return [value, best_move]


def botB(board, player, turn):
    depth = 3
    maxing = False
    if depth % 2 == 0:
        maxing = True
    return minimax(board, player, depth, maxing)[1]


def resolve(board, move):
    if move is not None:
        xs = move[0]
        ys = move[1]
        xf = move[2]
        yf = move[3]

        board[xf][yf][1] = board[xs][ys][1]
        board[xs][ys][1] = 0

    return board


def check_win(board):
    for row in board:
        for spot in row:
            if spot[0] == 3 and spot[1] != 0:
                return -1
            if spot[0] == -3 and spot[1] != 0:
                return 1
    return 0


def simulation(board, player, turn):
    won = 0
    while won == 0 and turn < 60:
        won = check_win(board)
        if not won:
            if player == -1:
                move = botB(board, player, turn)

            if player == 1:
                move = botA(board, player, turn)

            board = resolve(board, move)

            turn += 1
            player = -player
            show(board)

    if won == 0:
        won = -1
        pieces = set()
        for row in board:
            for spot in row:
                pieces.add(spot[1])

        for i in range(8, 0, -1):
            if i in pieces and -i not in pieces:
                won = 1
                break
            if -i in pieces and i not in pieces:
                won = -1
                break

    return won


table = new_board()
show(table)
print(simulation(table, 1, 0))
