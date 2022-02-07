import csv
from random import randint

import matplotlib.pyplot as plt
import networkx
import numpy as np
import tqdm


class Graph:

    def __get_edges(self, minEdges, maxEdges):

        opLen = self.len - 2
        rMinE = minEdges
        rMaxE = maxEdges

        if not rMaxE or rMaxE > opLen:
            rMaxE = opLen
        elif rMaxE < 2:
            rMaxE = 2
        else:
            rMaxE = maxEdges

        if not rMinE or rMinE < 0:
            rMinE = 0
        elif rMinE > rMaxE:
            # min rMaxE = 2
            rMinE = rMaxE - 1
        else:
            rMinE = minEdges

        return rMinE, rMaxE

    def __get_len(self, len):
        if not len:
            return randint(3, 10)
        else:
            if len < 2:
                return 2
            return len
        # len > 2 [2, 3, 4, ...)

    def __get_avg_edges(self, avgEdges):
        if not avgEdges:
            if self.len == 2:
                return 1
            else:
                return randint(self.minEdges, self.maxEdges - 1)
        else:
            if avgEdges > self.len - 1:
                return round(self.len / 2)
            else:
                return avgEdges

    def __init__(self, directed=True, vert=False, avgEdges=2, useWeights=False, minEdges=False, maxEdges=False,
                 add_stock_sink=False, type='list'):
        self.directed = directed
        self.len = self.__get_len(vert)
        self.minEdges, self.maxEdges = self.__get_edges(minEdges, maxEdges)
        # print(f'min: {self.minEdges}\tmax: {self.maxEdges}')
        self.avgEdges = self.__get_avg_edges(avgEdges)
        self.useWeights = useWeights
        self.type = type
        self.G = {}
        # print(self.G)
        self.currentAvg = 0
        self.add_stock_sink = add_stock_sink

        for i in range(self.len+1 if self.add_stock_sink else self.len):
            self.G[i] = []

    def get_config(self):
        print(f'Current configuration: {self.__dict__}')

    def __is_from_a_to_b(self, a, b):
        return b in self.G[a]

    def __get_current_avg_edges(self):

        self.currentAvg = round(
            sum([len(i) for i in self.G.values()]) / len(self.G.keys()))
        # print('currentAvg:', self.currentAvg)

    def get_graph(self):

        arr = [i for i in range(
            0, self.len)]

        # print('arr:', arr)

        for i in tqdm.tqdm(arr):

            disp = self.currentAvg - self.avgEdges

            minE = self.minEdges
            maxE = self.maxEdges

            if i > 0:
                if disp > 0:
                    maxE = round(self.currentAvg)
                elif disp < 0:
                    minE = round(self.currentAvg)
            # print(f'generating from {minE} to {maxE}; disp: {disp}')

            rL = randint(minE + 1 if i == 0 else minE, maxE)

            tmp = arr.copy()
            tmp.remove(i)
            if not i == 0:
                tmp.remove(0)

            rand = list(
                list(self.G[i]) + list(sample_c(tmp, k=rL, use_weight=self.useWeights)))
            self.G[i] = rand

            if not self.directed:
                for to in self.G[i]:
                    # print(f'for to: {to} in {self.G[i]}')
                    self.G[to] = list(set(self.G[to] + [i]))
                # print(f'`adding to {to[0]}\t{i}')
                # self.G[to[0]].add((i, to[1]))
                # for to in self.G[i]:
                #     self.G[to] = list(set(self.G[to] + [i]))

            self.__get_current_avg_edges()
            # print(f'{i} -> {rL}')

        self.G[self.len-1] = []
        # pprint(self.G)

        return self.G if self.type == 'list' else self.get_matrix()

    def get_matrix(self):
        matrix = [[0 if i != j else 0 for i in range(len(self.G))]
                  for j in range(len(self.G))]

        for i in self.G:
            # k: 0; v: [(a,b), (c,d),...]
            # print(f'{i} {self.G[i]}')
            for j in self.G[i]:
                matrix[i][j] = 1

        return matrix

    def read_csv(self, graph):
        return graph

    def get_plot(self):
        if self.directed:
            graph = networkx.DiGraph()
        else:
            graph = networkx.Graph()
        for i in self.G.keys():
            for j in self.G[i]:
                graph.add_edge(i, j, label=i)

        networkx.draw(graph, with_labels=True)
        plt.show()

    def get_csv(self):
        print('CSV')
        with open('lb7.csv', mode='w') as csvF:
            writer = csv.writer(csvF)
            if self.useWeights:
                for i in range(self.len):
                    writer.writerow(
                        [i] + [f'{p[0]} {p[1]}' for p in self.G[i]])
            else:
                for i in range(self.len):
                    writer.writerow([i] + list(self.G[i]))


def get_randbelow(n):
    return randint(0, n - 1)


def sample_c(population, k, use_weight):
    randbelow = get_randbelow

    rand_weights = np.random.normal(0.5, 0.1, 4 * k)

    n = len(population)
    result = [None] * k
    pool = list(population)
    for i in range(k):  # invariant:  non-selected at [0,n-i)
        j = randbelow(n - i)
        if use_weight:
            # [s, k)
            result[i] = (pool[j], randint(1, 20000))
        else:
            result[i] = pool[j]
        pool[j] = pool[n - i - 1]  # move non-selected item into vacancy
    return result
