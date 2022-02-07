from Graph import Graph
import math
import queue


def bfs(C, F, s, t):  # C is the capacity matrix
    n = len(C)
    queue = []
    queue.append(s)
    global level
    level = n * [0]  # initialization
    level[s] = 1
    while queue:
        k = queue.pop(0)
        for i in range(n):
            if (F[k][i] < C[k][i]) and (level[i] == 0):  # not visited
                level[i] = level[k] + 1
                queue.append(i)
    return level[t] > 0


def dfs(C, F, k, cp):
    tmp = cp
    if k == len(C) - 1:
        return cp
    for i in range(len(C)):
        if (level[i] == level[k] + 1) and (F[k][i] < C[k][i]):
            f = dfs(C, F, i, min(tmp, C[k][i] - F[k][i]))
            F[k][i] = F[k][i] + f
            F[i][k] = F[i][k] - f
            tmp = tmp - f
    return cp - tmp


def get_max_flow(C, s, t, gr):
    n = len(C)
    F = [n * [0] for i in range(n)]  # F - матрица потока

    flow = 0
    while bfs(C, F, s, t):
        flow = flow + dfs(C, F, s, 100000)
    return flow


# С = тут нужно генерировать пропускная способность
#
C = [
    [0, 2, 13, 1],
    [3, 4, 7, 12],
    [0, 5, 2, 0],
    [1, 3, 0, 8],
]

# len - кол-во вершин
g = Graph(len=4, add_stock_sink=True, useWeights=True)
gr = g.get_graph()
print(gr)

max_flow_value = get_max_flow(C, 0, len(C) - 1, gr)
print("Значение максимального потока: ", max_flow_value)
