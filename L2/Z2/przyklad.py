from itertools import groupby


# https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def lev(s1, s2):
    if len(s1) < len(s2):
        return lev(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


file_in = open('zad4_input.txt', 'r').read().splitlines()

result = []
for elem in file_in:
    current = 9001
    arr = elem.split(' ')

    bitmap = arr[0]
    target = int(arr[1])
    length = len(bitmap)

    for i in range(len(bitmap)-target+1):
        temp = (i * '0') + (target * '1') + ((length - i - target) * '0')
        current = min(current, lev(bitmap, temp))

    result.append(str(current))

open('zad4_output.txt', 'w+').write('\n'.join(result))