import csv
from itertools import groupby

def bfs(G,i):
    if i not in G:
        print("Не найдено",i)
        return None
    order = []
    visited = [i]
    queue = [i]
    while len(queue)!=0:
        v = queue.pop()
        order.append(v)
        al = G[v]
        al = list(filter((lambda a:a not in visited),al))
        visited.extend(al)
        for a in al:
            queue.insert(0,a)
    return order

def dfs(G,i):
    if i not in G:
        print("Не найдено",i)
        return None
    order = []
    visited = [i]
    stack = [i]
    while len(stack)!=0:
        v = stack.pop()
        order.append(v)
        al = G[v]
        al = list(filter((lambda a:a not in visited),al))
        visited.extend(al)
        for a in al:
            stack.append(a)
    return order

def main():
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
                    a = a+d[i]
                else:
                    T[j].append(a)
                    a = ''
            j += 1
    print(T)
    for k in range(len(T)):
        T[k] = sorted(T[k])
        T[k] = [el for el, _ in groupby(T[k])]
        G[str(k)] = T[k]
    print(G)
    # G = {0:[1],
    #     1:[0,1,1,2,4,3,6,7],
    #      2:[0,1,4],
    #      3:[7,1],
    #      4:[5,2,1],
    #      5:[4],
    #      6:[1,8,7],
    #      7:[3,6],
    #      8:[6]}
    initial = str(input("С какой вершины начать обход?"))
    print("Обход в ширину "+ str(bfs(G, initial)))
    print("Обход в глубину "+ str(dfs(G,initial)))

if __name__ == '__main__':
    main()