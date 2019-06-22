def V(i,j):
    return 'V%d_%d' % (i,j)


def domains(Vs):
    return [ q + ' in 1..9' for q in Vs ]


def all_different(Qs):
    return 'all_distinct([' + ', '.join(Qs) + '])'


def get_column(j):
    return [V(i,j) for i in range(9)]


def get_raw(i):
    return [V(i,j) for j in range(9)]


def horizontal():
    return [ all_different(get_raw(i)) for i in range(9)]


def vertical():
    return [all_different(get_column(j)) for j in range(9)]


def block(i):
    x = (i // 3) * 3
    y = (i % 3) * 3
    return all_different([V(i, j) for i in range(x, x + 3) for j in range(y, y + 3)])


def blocks():
    return [block(i) for i in range(9)]


def print_constraints(Cs, indent, d):
    position = indent
    writeln((indent - 1) * ' ')
    for c in Cs:
        writeln(c + ',')
        position += len(c)
        if position > d:
            position = indent
            writeln((indent - 1) * ' ')


def sudoku(assigments):
    variables = [ V(i,j) for i in range(9) for j in range(9)]

    writeln(':- use_module(library(clpfd)).')
    writeln('solve([' + ', '.join(variables) + ']) :- ')

    cs = domains(variables) + vertical() + horizontal() + blocks()
    for i,j,val in assigments:
        cs.append('{} #= {}'.format(V(i,j), val))

    print_constraints(cs, 4, 70)

    writeln('labeling([ff], [' + ', '.join(variables) + ']).')
    writeln('')
    writeln(':- solve(X), write(X), nl.')


def writeln(s):
    output.write(s + '\n')


txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

raw = 0
triples = []

for x in txt:
    x = x.strip()
    if len(x) == 9:
        for i in range(9):
            if x[i] != '.':
                triples.append( (raw,i,int(x[i])) )
        raw += 1

sudoku(triples)
