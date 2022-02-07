import csv


def BFS(s, t, pp):
    visited = [False] * len(g)
    q = []
    q.append(s)
    visited[s] = True
    while q:
        u = q.pop(0)
        for ind, val in enumerate(g[u]):
            if not visited[ind] and val > 0:
                q.append(ind)
                visited[ind] = True
                pp[ind] = u
    return True if visited[t] else False


def MaxFlow(beginning, end):
    pp = [-1] * len(g)
    maxflow = 0

    while BFS(beginning, end, pp):
        value = float("Inf")
        s = end
        way = [s]
        while (s != beginning):
            value = min(value, g[pp[s]][s])
            s = pp[s]
            way.append(s)
        way.reverse()
        print("Путь", way, "с потоком:", value)
        maxflow += value

        v = end
        while (v != beginning):
            u = pp[v]
            g[u][v] -= value
            g[v][u] += value
            v = pp[v]
    return maxflow


N = 2000
g = []
for i in range(N):
    g.append([])
    k = 0
    while k < N:
        g[i].append(0)
        k += 1
# print(g)
T = []
j = 0
with open('graph2000.csv', newline='') as File:  # тест на graph100, graph2000
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
    # print(T)
    while c < len(T):
        for i in range(len(T[c])):
            if i < len(T[c]) - r:
                g[c][int(T[c][i + r])] = int(T[c][i + 1 + r])
                r = i + 1
        c += 1
        r = 0
    # print(g)
s = 0
t = N - 1
result = MaxFlow(s, t)
print("Максимальный поток равен", result)
