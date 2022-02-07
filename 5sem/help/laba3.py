# Алгоритм Бржозовского
import random

def csv_dict_reader2(name):
    file = open(name, 'r')
    lines = file.readlines()
    arr = [list(map(str, lines[i].replace('\n', '').split(';'))) for i in range(len(lines))]
    file.close()
    fa[Q] = [int(i[0]) for i in arr[1:]]
    tmp = arr[0][1:]
    fa[A] = [tmp[i]for i in range(len(tmp))]
    fa[T] = []
    g = 0
    for i in arr[1:]:
        fa[T].append([])
        for j in range(1,len(i)):
            if g == 0:
                fa[S] = [int(i[g])]
            if i[j] != '':
                fa[T][g].append([int(i[j])])
            else:
                fa[T][g].append([])
        g += 1
    fa[F] = [int(arr[0][0])]
    return fa

def fa_gv(fa, filename):
    f = open(filename, 'w')
    f.write('digraph fa {\n')
    f.write('rankdir=LR;\n')
    f.write('node[shape=doublecircle];')
    for i in fa[F]:
        f.write('"' + str(fa[Q][i]) + '";')
    f.write('\nnode[shape=circle];\n')
    for t1 in range(0, len(fa[Q])):
        for a in range(0, len(fa[A])):
            for t2 in fa[T][t1][a]:
                f.write('"' + str(fa[Q][t1]) +'"' + '->' + '"' + \
                    str(fa[Q][t2]) + '"')
                f.write('[label="' + str(fa[A][a]) + '"];\n')
    f.write('}\n')
    f.close()
    return fa

def fa_rev(fa):
    rfa = [list(fa[Q]), list(fa[A]), [], list(fa[F]), list(fa[S])]
    rfa[T] = [[[] for i in range(0, len(fa[A]))] for j in range(0, len(fa[Q]))]
    for t1 in range(0, len(fa[Q])):
        for a in range(0, len(fa[A])):
            for t2 in fa[T][t1][a]:
                rfa[T][t2][a].append(t1)
    return rfa

def fa_det(fa):
    def reachable(q, l):
        t = []
        for a in range(0, len(fa[A])):
            ts = set()
            for i in q[l]:
                ts |= set(fa[T][i][a])
            if not ts:
                t.append([])
                continue
            try:
                i = q.index(ts)
            except ValueError:
                i = len(q)
                q.append(ts)
            t.append([i])
        return t
    dfa = [[], list(fa[A]), [], [0], []]
    q = [set(fa[S])]
    while len(dfa[T]) < len(q):
        dfa[T].append(reachable(q, len(dfa[T])))
    dfa[Q] = range(0, len(q))
    dfa[F] = [q.index(i) for i in q if set(fa[F]) & i]
    return dfa

def fa_min(fa):
    return fa_det(fa_rev(fa_det(fa_rev(fa))))

def check(fa, line):
    line = line.split()
    first = fa[S][0]
    variables = {fa[A][i]:i for i in range(len(fa[A]))}
    for i in line:
        index = variables[i]
        first = fa[T][first][index][0]
    return first

if __name__ == '__main__':
    line = ''
    while True:
        fa = [None] * 5
        Q, A, T, S, F = 0, 1, 2, 3, 4

        fa = csv_dict_reader2('input.csv')
        lenght = random.randint(1, 5)
        for i in range(0, lenght):
            line += str(random.randint(0, 1)) + ' '
        print(line)
        line = ''
        result = check(fa, line)
        fa1 = fa_gv(fa_min(fa), 'fa_min.gv')
        result2 = check(fa1, line)
        if (result2 == fa1[F][0]) == (result == fa[F][0]):
            print('Автоматы эквивалентны')
        else:
            print('Где то возникли проблемы')
        print(fa1)
        print(fa)