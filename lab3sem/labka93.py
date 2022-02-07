import random
from numpy.random import poisson


class Node:
    def __init__(self, id, neighborlist):
        self.id: int = id
        self.neighbors = tuple(neighborlist)
        self.used_colors = []

    def print_me(self):
        print(f"id: {self.id}, connects: {self.neighbors}")


# функция для сортировки вершин по их степени, а именно от наиболее встречаемой к наименее
def pow_sort(powers):
    list_ = list(powers.items())
    list_.sort(reverse=True, key=lambda i: i[1])
    list_ = list(i for i, j in list_)
    return list_


def refactor(q, size):
    V = []
    for i in range(size):
        list_neighbours = []
        for j in range(size):
            if int(q[i][j]) != 0:
                list_neighbours.append(j)
                # print(list_neighbours)
        V.append(Node(i, list_neighbours))
        # print(V)
    return V


# Метод для поиска соседей, а именно:
# возвращается -1, если не нашлось цвета, с вершинами, где нет смежности
def search_neighbors(g, index, painted):
    col_id = 0
    for i in painted:
        z = 1
        for j in i:
            if g[j][index] == 1:
                z = 0
        if z == 1:
            return col_id + 1
        col_id += 1
    return -1


def painting_vertices(V, sorted, edges):
    maxcolor = 0
    # print(sorted)
    while len(sorted) > 0:
        thisV = sorted.pop(0)
        for j in V[thisV].neighbors:
            if edges[thisV][j] == -1:
                for k in range(0, maxcolor + 1):
                    if k not in V[thisV].used_colors and k not in V[j].used_colors:
                        V[thisV].used_colors.append(k)
                        V[j].used_colors.append(k)
                        edges[thisV][j] = k
                        edges[j][thisV] = k
                        break
                if edges[thisV][j] == -1:
                    maxcolor += 1
                    V[thisV].used_colors.append(maxcolor)
                    V[j].used_colors.append(maxcolor)
                    edges[thisV][j] = maxcolor
                    edges[j][thisV] = maxcolor
    print("\nМатрица раскраски рёбер по цветам:")
    for i in edges:
        for j in i:
            if j == -1:
                print("-", end='\t')
            else:
                print(f"{j}", end='\t')
        print()
    print(f"\nХроматический индекс: {maxcolor + 1}")


def graph_making_mid(N, graph, mid_deg):
    for i in range(N):
        graph.append([0]*N)

    # Заполняем матрицу числами, основываясь на средней степени;
    for i in range(0, len(graph), 1):
        for j in range(random.randint(0, mid_deg), mid_deg, 1):
            graph[i][j] = poisson(mid_deg)

    # Заполняем диагональ 0 - исключаем петли, которые могли получиться в результате рандомного заполнения на шаге выше;
    # Также мы исключаем не симметричность матрицы;
    for i in range(N):
        for j in range(N):
            graph[i][j] = graph[j][i]
            graph[i][i] = 0
    """
    for row in range(N):
        print(graph[row])
    """


if __name__ == '__main__':

    graph = []

    # Входные данные
    N = int(input("Введите кол-во вершин: "))
    middle_degree = int(input("Введите среднюю степень связности: "))
    graph_making_mid(N, graph, middle_degree)

    gr_size = len(graph)
    edges = [[-1] * gr_size for i in range(gr_size)]

    powers = {}
    for i in range(gr_size):
        pow = 0
        for j in range(gr_size):
            if graph[i][j] != 0:
                pow += 1
        powers[i] = pow

    # print(powers)
    sorted = pow_sort(powers)
    # print(sorted)

    V = refactor(graph, gr_size)

    # Вывод
    painting_vertices(V, sorted, edges)
