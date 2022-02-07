import random
from collections import defaultdict


def dijkstra(k, graf):
    print('введите начальный индекс вершины')
    start_index = int(input())
    d = [10 ** 10 for i in range(k)]
    visited = [1 for i in range(k)]
    d[start_index] = 0

    while True:
        minindex = -1
        minimum = 10 ** 10

        for i in range(k):
            if ((visited[i] == 1) and (d[i] < minimum)):
                minimum = d[i]
                minindex = i
        if minindex != -1:
            for i in range(k):
                if graf[minindex][i] > 0:
                    temp = minimum + graf[minindex][i]
                    if temp < d[i]:
                        d[i] = temp
            visited[minindex] = 0
        if visited[k - 1] == 0:
            break;

    print("Кратчайшие расстояния до вершин: ")
    print(d)

    ver = []
    end = k - 1
    ver.append(end)
    # ver[0] = end
    weight = d[end]

    while end != start_index:
        for i in range(k):
            if graf[i][end] != 0:
                temp = weight - graf[i][end]
                if temp == d[i]:
                    weight = temp
                    end = i
                    ver.append(i)
                    # ver[pw] = i
    print("кратчайший путь от стока к истоку")
    print(ver)


print('Введите количество вершин')
k = int(input())

print('Введите максимальный вес ребра')
w = int(input())

graf2 = [[0] * k for i in range(k)]
graf = defaultdict(list)
unvisited = [i for i in range(k)]
unmarked = [i for i in range(k)]

def rand_vertex(unmarked, m):
  n = m
  while n == m:
    n = random.choice(unmarked)
  return n

while len(unvisited) != 0:
  m = random.choice(unvisited)
  unvisited.remove(m)
  u = 0
  q = random.randint(1,8)
  while u != q:
    if len(unmarked) != 0:
      n = rand_vertex(unmarked, m)
      unmarked.remove(n)
      graf2[m][n] = random.randint(1,w)
      u = u+1
    else:
      n = random.randint(1,k-1)
      if n != m and graf2[m][n] == 0:
        graf2[m][n] = random.randint(1,w)
        u = u+1
      else:
        pass

dijkstra(k, graf2)