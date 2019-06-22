import random
import sys
import pickle

D = 7
H = 6

def four(x, y, dx, dy):
    return [ (x + i * dx, y + i * dy) for i in range(4)]

verticals   = [four(x, y, 0, 1) for x in range(D) for y in range(H - 4)]
horizontals = [four(x, y, 1, 0) for x in range(D - 4) for y in range(H)]
diagonals   = [four(x, y, 1, 1) for x in range(D - 4) for y in range(H - 4)]
diagonals  += [four(x, y, 1, -1) for x in range(D - 4) for y in range(4,H)]
all_fours = verticals + horizontals + diagonals

def is_winning(S):
    return S == ['o', 'o', 'o', 'o'] or S == ['#', '#', '#', '#']


class TD():
    def __init__(self, board, learning_rate=0.1, discount_rate=1.0, epsilon=0.1, initial_value=0.5, value_function=None, should_stop_learning=False):
        self.board = board
        self.game = 0
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.epsilon = epsilon
        self.initial_value = initial_value
        if value_function is None:
            value_function = {}
        self.value_function = value_function
        self.saved_game_states = {}
        self.should_stop_learning = should_stop_learning

    def get_value(self, state_key):
        return self.value_function.get(state_key, self.initial_value)

    def save_state(self, state_key):
        self.saved_game_states[self.game] = self.saved_game_states.get(self.game, []) + [state_key]

    def next_move(self, player):
        available_positions = board.moves(player)

        if random.random() < self.epsilon:
            position = random.choice(available_positions)
            board.do_move(position)
            next_state_key = board.all_counts(player)
            board.undo_move(position)

        else:
            options = []
            for position in available_positions:
                board.do_move(position)
                next_state_key = board.all_counts(player)
                board.undo_move(position)
                action_value = self.get_value(next_state_key)
                options.append((action_value, position, next_state_key))

            max_value = max(options)[0]
            best_options = [m for m in options if m[0] == max_value]
            _, position, next_state_key = random.choice(best_options)

        self.save_state(next_state_key)

        return position

    def get_saved_game_states(self):
        states = self.saved_game_states.get(self.game, None)
        if states is None:
            states = []
            self.saved_game_states[self.game] = states

        return states

    def set_board(self, board):
        self.board = board

    def new_game(self):
        self.game += 1
        self.saved_game_states = {}

    def stop_learning(self):
        self.should_stop_learning = True

    def get_value_function(self):
        return self.value_function

    def reward(self, reward):
        if not self.should_stop_learning:
            states = self.get_saved_game_states()
            self.value_function[states[-1]] = reward

            for i in range(len(states)-1, 0, -1):
                self.value_function[states[i-1]] = self.get_value(states[i-1]) + self.learning_rate * (reward + self.discount_rate * self.get_value(states[i]) - self.get_value(states[i-1]))


class Board:
    def __init__(self):
        self.board = [['.'] * D for i in range(H+1)]
        self.cnt = 0

    def height(self, x):
        return min(y for y in range(H+1) if self.board[y][x] == '.')

    def counts(self, count, piece, lst):
        return [fs.count(piece) == count for fs in lst].count(True)

    def all_counts(self, player):
        vs = [self.get_fields(fs) for fs in verticals]
        hs = [self.get_fields(fs) for fs in horizontals]
        ds = [self.get_fields(fs) for fs in diagonals]

        if player == 0:
            piece = 'o'
        else:
            piece = '#'

        return (self.counts(2, piece, vs), self.counts(2, piece, hs), self.counts(2, piece, ds),
                self.counts(3, piece, vs), self.counts(3, piece, hs), self.counts(3, piece, ds),
                self.counts(4, piece, vs), self.counts(4, piece, hs), self.counts(4, piece, ds))

    def moves(self, player):
        hs = [(self.height(x), x) for x in range(D)]
        return [(player, x) for (h,x) in hs if h < H]

    def draw(self):
        bs = self.board[:-1]
        for raw in bs[::-1]:
            print (''.join(raw))
        print ('')

    def random_move(self, player):
        return player, random.choice(self.moves(player))[1]

    def do_move(self, m):
        player, x = m
        if player == 0:
            c = 'o'
        else:
            c = '#'
        self.board[self.height(x)][x] = c
        self.cnt += 1

    def undo_move(self, m):
        player, x = m
        self.board[self.height(x)-1][x] = '.'
        self.cnt -= 1

    def get_fields(self, fs):
        res = []
        for x,y in fs:
            res.append( self.board[y][x])
        return res

    def end_of_game(self):
        if self.cnt == D * H:
            return True
        return self.victory()

    def victory(self):
        return any(is_winning(self.get_fields(fs)) for fs in all_fours)



td_player = TD(None)
reinforcement_games = 10000
test_games = 1000

td_victories = 0
random_victories = 0
draws = 0

write = False
read = True

for game_no in [reinforcement_games, test_games]:
    if read is True:
        read = False
        with open('pickle', 'rb') as file:
            td_player = TD(None, value_function = pickle.load(file), should_stop_learning=True)

        print("File loaded")
        continue

    games_played = 0
    td_victories = 0
    random_victories = 0
    draws = 0

    while games_played < game_no:
        games_played += 1
        current_player = 0
        td_player_turn = games_played%2
        board = Board()
        td_player.set_board(board)
        td_player.new_game()

        while True:
            if current_player is td_player_turn:
                move = td_player.next_move(current_player)
            else:
                move = board.random_move(current_player)

            board.do_move(move)

            if board.victory():
                if current_player is td_player_turn:
                    td_player.reward(3.0)
                    td_victories += 1
                else:
                    td_player.reward(-3.0)
                    random_victories += 1

                break

            elif board.end_of_game():
                draws += 1
                td_player.reward(0.0)
                break

            current_player = 1 - current_player

    td_player.stop_learning()

if write is True:
    with open('pickle', 'wb') as file:
        pickle.dump(td_player.get_value_function(), file, protocol=pickle.HIGHEST_PROTOCOL)

print((td_victories / test_games) * 100, '% winrate', sep='')
print((draws / test_games) * 100, '% draws', sep='')
