def storm(rows, columns, known):
    writeln(':- use_module(library(clpfd)).')

    R = len(rows)
    C = len(columns)

    bs = [S(i,j) for i in range(R) for j in range(C)]

    writeln('solve([' + ', '.join(bs) + ']) :- ')

    constraints_SQ = [[S(i, j), S(i + 1, j), S(i, j + 1), S(i + 1, j + 1)] for i in range(R - 1) for j in range(C - 1)]
    constraints_HA = [[S(i, j), S(i + 1, j), S(i + 2, j)] for i in range(R - 2) for j in range(C)]
    constraints_HB = [[S(i, j), S(i, j + 1), S(i, j + 2)] for i in range(R) for j in range(C - 2)]

    storm_SQ = [[0,0,0,0], [1,1,1,1], [1,0,1,0], [0,1,0,1], [1,1,0,0], [0,0,1,1], [1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
    storm_H = [[0,0,0], [1,1,1], [1,0,1], [1,0,0], [0,0,1], [1,1,0], [0,1,1]]

    writeln('tuples_in({},{}),'.format(str(constraints_SQ).replace("'", ""), storm_SQ))
    writeln('tuples_in({},{}),'.format(str(constraints_HA).replace("'", ""), storm_H))
    writeln('tuples_in({},{}),'.format(str(constraints_HB).replace("'", ""), storm_H))

    rows_constraints = [' + '.join([S(i, j) for j in range(C)]) + ' #= ' + str(rows[i]) for i in range(R)]
    columns_constraints = [' + '.join([S(i, j) for i in range(R)]) + ' #= ' + str(columns[j]) for j in range(C)]

    for constraint in rows_constraints + columns_constraints:
        writeln(constraint + ',')

    for t in known:
        writeln('{} #= {},'.format(S(t[0], t[1]), t[2]))

    writeln('labeling([ff], [' + ', '.join(bs) + ']).')
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")


def S(i,j):
    return 'S_%d_%d' % (i,j)


def writeln(s):
    out.write(s + '\n')


input = open('zad_input.txt').readlines()
rows = list(map(int, input[0].split()))
columns = list(map(int, input[1].split()))
known = []

for i in range(2, len(input)):
    if input[i].strip():
        known.append(list(map(int, input[i].split())))

out = open('zad_output.txt', 'w')
storm(rows, columns, known)
