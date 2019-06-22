import copy

file_in = open('zad_input.txt', 'r').read().splitlines()

file_in[0] = file_in[0].split(' ')
l = int(file_in[0][0])
u = int(file_in[0][1])

help_l = []
help_u = []

for i in range(1,l+1):
    numbers = []
    file_in[i] = file_in[i].split(' ')
    for word in file_in[i]:
        numbers.append(int(word))
    help_l.append(numbers)

for i in range(l+1, l+u+1):
    numbers = []
    file_in[i] = file_in[i].split(' ')
    for word in file_in[i]:
        numbers.append(int(word))
    help_u.append(numbers)

print(help_l)
print(help_u)

board_l = []
for i in range(l):
    row = []
    for j in range(u):
        row.append(0)
    board_l.append(row)

board_u = []
for i in range(u):
    col = []
    for j in range(l):
        col.append(0)
    board_u.append(col)


def deep(row, wip, at, help, depth):
    if depth == len(help):
        wrong = False
        for i in range(at, len(row)):
            if row[i] == 1:
                wrong = True
                break
            wip[i] = -1

        if wrong:
            return -1
        return wip.copy()

    else:
        base = wip.copy()
        answer = -1
        first = True

        for i in range(at, len(row)-help[depth]+1):
            wip = base.copy()
            wrong = False

            for j in range(at, i):
                if row[j] == 1:
                    wrong = True
                    break
                wip[j] = -1

            for j in range(i, i+help[depth]):
                if row[j] == -1:
                    wrong = True
                    break
                wip[j] = 1

            now_at = i+help[depth]
            if now_at < len(row):
                if row[now_at] == 1:
                    wrong = True
                wip[now_at] = -1
                now_at += 1

            if wrong:
                continue

            ret = deep(row, wip, now_at, help, depth+1)
            if ret != -1:
                if first:
                    answer = ret
                    first = False
                else:
                    for j in range(len(ret)):
                        if answer[j] != ret[j]:
                            answer[j] = 0

        return answer


def compare(row, help):
    wip1 = []
    for i in range(len(row)):
        wip1.append(0)
    return deep(row, wip1, 0, help, 0)


def solve(board_l, board_u):
    changes = 1
    while changes > 0:
        changes = 0
        for i in range(len(board_l)):
            result = compare(board_l[i], help_l[i])
            if result == -1:
                return -1, -1
            if result != -1 and result != board_l[i]:
                changes += 1
                board_l[i] = result
                for j in range(len(board_u)):
                    board_u[j][i] = board_l[i][j]

        for i in range(len(board_u)):
            result = compare(board_u[i], help_u[i])
            if result == -1:
                return -1, -1
            if result != -1 and result != board_u[i]:
                changes += 1
                board_u[i] = result
                for j in range(len(board_l)):
                    board_l[j][i] = board_u[i][j]

    return board_l, board_u


def check(board_l):
    for i in range(len(board_l)):
        for j in range(len(board_l[i])):
            if board_l[i][j] == 0:
                return False

    return True


def check2(board_l, board_u):
    for i in range(len(board_l)):
        if compare(board_l[i], help_l[i]) == -1:
            return False

    for i in range(len(board_u)):
        if compare(board_u[i], help_u[i]) == -1:
            return False

    return True


def plan(board_l, board_u):
    answer1, answer2 = solve(board_l, board_u)
    if answer1 == -1:
        return -1, -1

    if check(board_l):
        return answer1, answer2

    print("guessing")
    for i in range(len(board_l)):
        for j in range(len(board_l[i])):
            if board_l[i][j] == 0:

                board_l[i][j] = -1
                board_u[j][i] = -1

                ret1, ret2 = plan(copy.deepcopy(board_l), copy.deepcopy(board_u))
                if ret1 == -1:
                    board_l[i][j] = 1
                    board_u[j][i] = 1
                else:
                    return ret1, ret2

    print("failed")
    return -1, -1


board_l,board_u = plan(board_l, board_u)

out = open('zad_output.txt', 'w+')
for col in board_l:
    for nbr in col:
        if nbr == -1:
            out.write('.')
        if nbr == 0:
            out.write('?')
        if nbr == 1:
            out.write('#')
    out.write('\n')

