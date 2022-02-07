import csv
from itertools import groupby

def printf(file,massiv):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    i = 0
    for line in massiv:
        writer.writerow(line)
        i += 1
    outfile.close()

def dbfs(G,i):
    if i not in G:
        print('Данной вершины нет в графе')
        return None
    order =[]
    visited =[i]
    stack =[i]
    while len(stack) != 0:
        v = stack.pop()
        order.append(v)
        al =  G[v]
        al = list(filter((lambda a: a not in visited),al))
        visited.extend(al)
        for a in al:
            stack.append(a)
    return order
def transpose(G):
    P ={}
    for v in G.keys():
        for w in G[v]:
            if w not in P.keys():
                P[w]= [v]
            else:
                P[w].append(v)
    for v in G.keys():
        if v not in P.keys():
            P[v] = []
    return P
def try_dict(D):
    for i in D.keys():
        if D[i] == False:
            return False
    return True

def first_unvisited(D):
    for i in D.keys():
        if D[i] == False:
            return i
    return None
def kosaraju(G):
    stack = []
    visited = {}
    for k in G.keys():
        visited[k] = False
    while not try_dict(visited):
        l = first_unvisited(visited)
        c = dbfs(G,l)
        c.reverse()
        for i in c:
            if not visited[i]:
                stack.append(i)
                visited[i] = True
    P = transpose(G)
    ret = []
    for k in G.keys():
        visited[k] = False
    while len(stack) != 0:
        a = stack.pop()
        if not visited[a]:
            c = dbfs(P,a)
            c = list(filter(lambda p : not visited[p], c))
            ret.append(c)
            if c is not None:
                for i in c:
                    visited[i] = True
    return ret




if __name__ == '__main__':
    file = input("Введите название файла: ")
    G = {}
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
            for i in range(len(str(d))):
                if d[i] != ';':
                    a = a + d[i]
                else:
                    T[j].append(a)
                    a = ''
            j += 1
    print(T)
    for k in range(len(T)):
        # T[k] = sorted(T[k])
        # T[k] = [el for el, _ in groupby(T[k])]
        G[str(k)] = T[k]
    print(G)
    # G= {
    #     0:[1],
    #     1:[2],
    #     2:[5,3],
    #     3:[0,4],
    #     4:[6],
    #     5:[4],
    #     6:[5]
    # }
    #print(transpose(G))
    R = kosaraju(G)
    print("Компоненты связности ", R)
    m = []
    maxs = -1
    for i in range(len(R)):
        if len(R[i]) > maxs:
            m = R[i]
            maxs = len(R[i])
    print("Максимально связная компонента", m)
    R1 = []
    for i in range(len(G)):
        R1.append([])
    for j in G.keys():
        for i in range(len(G[str(j)])):
            if G[str(j)][i] and j in m:
                if int(G[str(j)][i]) not in R1[int(j)]:
                    R1[int(j)].append(int(G[str(j)][i]))
    #print(R1)
    file = input("Введите название файла в который вывести сильную компоненту связности: ")
    printf(file, R1)