import csv
def dfs(v):
    if (used[v]):
        return False
    used[v] = True
    for to in g[v]:
        if (matching[to] == -1 or dfs(matching[to])):
            matching[to] = v
            return True
    return False

matching = []
# g = [
#     [0],
#     [0],
#     [1],
#     [1]
# ]
used = []
# N = 4
# K = 2
N = int(input("Введите количество вершин в первой части: "))
K = int(input("Введите количество вершин во второй части: "))
g = []
for i in range(N):
    g.append([])
file = input("Введите название файла: ")
T = []
j = 0
with open('{}.csv'.format(file), newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        T.append([])
        d = row
        d = d[0]
        c = 0
        a = ''
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
# print(T)
for k in range(len(T)):
    for h in range(len(T[k])):
        g[k].append(int(T[k][h]))
for i in range(K):
    matching.append(-1)
for i in range(N):
    for j in range(N):
        used.append(False)
    dfs(i)
ll =0
for i in range(K):
    if (matching[i] != -1):
        ll = 1
        print(matching[i],i)
if ll == 0:
    print("Паросочетаний в графе нет!")