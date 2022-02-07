import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import copy


def csv_v2(graph, filename):
    with open(filename, "w") as file:
        for n in range(len(graph)):
            file.write(',{}'.format(str(n)))
        file.write('\n')
        c = 0
        for i in graph:
            file.write(str(c) + ',' + str(i).replace('[', '').replace(']', '').replace(' ', '') + '\n')
            c += 1


def show_graph_with_labels(adjacency_matrix):
    rows, cols = np.where(adjacency_matrix != 0)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=400, with_labels=True)
    plt.show()


# print("Размер графа:")
graph_len = 25
# print("Максимальный вес вершины: ")
max_node_weight = 7

flag = True
while flag:
    # print("Минимальная степень вершины: ")
    min_degv = 10
    if min_degv <= graph_len:
        flag = False
    else:
        print("ERROR")

graph = [[0] * graph_len for i in range(graph_len)]

for m in range(len(graph)):
    c = 0
    while c != min_degv:
        node = random.randint(0, graph_len - 1)
        if graph[m][node] == 0:
            weight = random.randint(1, max_node_weight)
            graph[m][node] = weight
            graph[node][m] = weight
            c += 1
        else:
            pass

print(graph)

show_graph_with_labels(np.array(graph))

dict_ = {}
for m in range(len(graph)):
    for node in range(len(graph)):
        # print(m, node)
        if graph[m][node] != 0:
            if m == node:
                pass
            else:
                s = str(m) + '-' + str(node)
                dict_[s] = graph[m][node]
                graph[node][m] = 0

dict_ = {k: v for k, v in sorted(dict_.items(), key=lambda item: item[1])}

print(dict_)

graph_len = len(graph)

min_spanning_tree = [[0] * graph_len for i in range(graph_len)]
component = [i for i in range(graph_len)]

sum = 0

for key in dict_:
    node_1, node_2 = key.split('-')
    node_1 = int(node_1)
    node_2 = int(node_2)
    if component[node_1] != component[node_2]:
        min_spanning_tree[node_1][node_2] = dict_[key]
        min_spanning_tree[node_2][node_1] = dict_[key]
        sum += dict_[key]
        node_1_subset = component[node_1]
        node_2_subset = component[node_2]
        for node in range(len(component)):
            if component[node] == node_2_subset:
                component[node] = node_1_subset

print("Вес остовного дерева: ", sum)

show_graph_with_labels(np.array(min_spanning_tree))
