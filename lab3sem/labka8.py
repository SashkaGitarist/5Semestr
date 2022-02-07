from math import inf
import numpy as np
import csv

def Floyd_Warshall(T):
    if len(T)!= len(T[0]):
        return
    H = []
    for row in T:
        h_row = [0 for i in range(N)]
        for i in range(len(T[0])):
            if row[i]!=0 or not np.isinf(row[i]):
                h_row[i] = i+1
        H.append(h_row)
    for n in range(len(T[0])):
        mask = [[1 for i in range(N)] for i in T]
        mask[n] = [0 for i in range(N)]
        for i in range(len(T[0])):
            mask[i][n] = 0
            if T[n][i] == 0 or np.isinf(T[n][i]):
                for j in range(len(T[0])):
                    mask[j][i] = 0
            if T[i][n] == 0 or np.isinf(T[i][n]):
                mask[i] = [0 for i in range(N)]
        ind_mul = np.transpose(np.nonzero(np.array(mask)))
        for elem in ind_mul:
            i,j = elem[0],elem[1]
            if T[i][j] > T[n][j]+T[i][n]:
                T[i][j] = T[n][j] + T[i][n]
                H[i][j] = H[i][n]
    return T,H

def Check(inc):
    phi2 = [float("Inf")] * N
    phi2[0] = 0
    for i in range(N - 1):
        for u, v, w in inc:
            if phi2[u] != float("Inf") and phi2[u] + w < phi2[v]:
                phi2[v] = phi2[u] + w
    for u, v, w in inc:
        if phi2[u] != float("Inf") and phi2[u] + w < phi2[v]:
            return -1

def print__(T):
    marked = [i for i in range(N)]
    inc = []
    for i in marked:
        for j in range(N):
            if g[i][j] != np.inf:
                inc.append([i, j, g[i][j]])
    result = Check(inc)
    if result == -1:
        print("Граф имеет отрицательный цикл")
        return
    T_,H_= Floyd_Warshall(T)
    for i in range(1,len(g)+1):
        for j in range(1,len(g)+1):
            if i != j:
                if T_[i-1][j-1] != np.inf:
                    result2 = {'Путь':[],
                        'Длина':T_[i-1][j-1]}
                else:
                    result2 = {'Путь': [],
                           'Длина': 'Пути нет!'}
                current = i
                result2['Путь'].append(current)
                while current !=j:
                    current = H_[current-1][j-1]
                    result2['Путь'].append(current)
                print(result2)

N = 10
g = []
for i in range(N):
    g.append([])
    k = 0
    while k < N:
        if k == i:
            g[i].append(0)
        else:
            g[i].append(np.inf)
        k += 1
file = "graph10"
T = []
j = 0
with open('{}.csv'.format(file), newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        d = row
        T.append([])
        d = d[0]
        q = ''
        for i in range(len(str(d))):
            if d[i] != ';':
                q = q + d[i]
                if i == len(str(d)) - 1:
                    T[j].append(q)
            else:
                if d[i] == ';':
                    T[j].append(q)
                    q = ''
        j += 1
    c = 0
    r = 0
    while c < len(T):
        for i in range(len(T[c])):
            if i < len(T[c]) - r:
                g[c][int(T[c][i + r])] = int(T[c][i + 1 + r])
                r = i + 1
        c += 1
        r = 0
print__(g)
