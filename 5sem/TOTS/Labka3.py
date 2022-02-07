import threading
import time

import networkx as nx
import random
import matplotlib.pyplot as plt


def generator_graph(type_topology: int, count_nodes: int, count_links: int):
    queue = []
    adjacency_list = []
    graph = nx.Graph()
    if type_topology == 1:  # Граф кольцо

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        for i in range(0, count_nodes, 1):
            graph.add_edge(i, i + 1, weight=random.randint(0, 9))

        graph.add_edge(0, count_nodes, weight=random.randint(0, 9))

    elif type_topology == 2:  # Граф звездочка

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        random_node = random.randint(0, count_nodes)

        for i in range(count_nodes):
            if random_node == i:
                continue
            else:
                graph.add_edge(i, random_node, weight=random.randint(0, 9))

    elif type_topology == 3:  # Случайный график

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        for j in range(count_nodes):
            for i in range(count_links):
                rand = random.randint(0, count_nodes)
                if rand == j:
                    continue
                else:
                    graph.add_edge(j, rand, weight=random.randint(0, 9))
    return graph


def statistics(graph, count_nodes: int, list_of_time_treatment, list_of_length_queue):
    middle_degree = []
    tmp = graph.degree
    for i in range(count_nodes):
        middle_degree.append(tmp[i])
    print("Средняя степень вершин: ", sum(middle_degree) / count_nodes)
    time_middle_package = []

    for i in range(len(list_of_time_treatment)):
        for j in list_of_time_treatment[i]:
            time_middle_package.append(sum(list_of_time_treatment[i][j]) / len(list_of_time_treatment[i][j]))

    average_length_queue = list_of_length_queue
    if len(average_length_queue) != 0:
        print(
            f"Максимальная длина очереди - {max(average_length_queue)},"
            f" средняя длина очереди - {sum(average_length_queue) / len(average_length_queue)}")
    else:
        print("length list queue is Empty")

    print(f"Среднее время обработки пакетов в сети - {sum(time_middle_package) / len(time_middle_package)}")


def draw_and_save(graph, type_topology: int):
    # Создание неорграфов. Если нужен орграф - добавляем arrows=True в draw-ку
    if type_topology == 1:  # ring
        nx.draw_circular(graph, with_labels=True, node_size=230, label={'weight'}, node_color="orange")
    elif type_topology == 2:  # star
        nx.draw(graph, with_labels=True, node_size=230, node_color="orange")
    elif type_topology == 3:  # random
        nx.draw(graph, with_labels=True, node_size=230, node_color="orange")

    plt.savefig("graph.png")
    plt.show()


def generator_of_package(graph, count_nodes):
    path = None
    source_node = random.randint(0, count_nodes)  # Откуда пакет
    target_node = random.randint(0, count_nodes)  # Куда пакет
    while source_node == target_node:
        source_node = random.randint(0, count_nodes)
        target_node = random.randint(0, count_nodes)
    try:
        # Образовывается "Путь", реализованный через алгоритм дейсктры
        path = nx.dijkstra_path(graph, source=source_node, target=target_node)
    except:
        print("################# Были сгенерированы вершины, к одной из которых нет пути! #####################")
        generator_of_package(graph, count_nodes)
    return path


def list_of_adjacency_list_this_node_creator(lst):
    list_of_nodes = []
    for i in lst:
        list_of_nodes.append(i)
    return list_of_nodes


list_of_time_treatment = []


def treatment_package():  # обработка пакета
    global list_of_time_treatment
    rand = random.random()
    time.sleep(rand)  # Реализация некой "задержки"
    return round(rand, 3)


locker = threading.Lock()
list_of_length_queue = []


def routing_executor(graph, package: list, list_of_delivered_package: list):
    temp_list = []
    for i in package:
        temp_node = i
        print(f'Пакет в узле - {i}, {threading.currentThread().name}')
        try:
            if package not in graph.nodes[temp_node]['queue']:
                graph.nodes[temp_node]['queue'].append(package)
            list_of_length_queue.append(len(graph.nodes[temp_node]['queue']))
        except KeyError:
            print(
                f"##ALERT## Пакет в узле {threading.currentThread().name} немного заблуждал! ##ALERT##")

        temp_list.append(treatment_package())
        if temp_node == package[-1]:
            list_of_time_treatment.append({threading.currentThread().name: temp_list})

            print(
                f"\n------------ Пакет отправлен в узел {i}, {threading.currentThread().name} ------------\n")
    try:
        for i in package:
            if len(graph.nodes[i]['queue']) != 0:
                graph.nodes[i]['queue'].pop(0)
    except KeyError:
        print(f"##ALERT## Пакет в {threading.currentThread().name} немного заблуждал! ##ALERT##")
    list_of_delivered_package.append({threading.currentThread().name: package})


def reformat_adjacency_list_nodes(graph, count_nodes: int):
    for i in range(count_nodes):
        graph.nodes[i]['adjacency_list'] = list_of_adjacency_list_this_node_creator(graph.adj[i])


def main():
    type_topology = int(input("Введите топологию: 1 - кольцо, 2 - звезда, 3 - случайный граф: "))
    count_nodes = int(input("Напишите количество узлов: "))
    count_links = None
    list_of_delivered_package = []

    if type_topology == 3:
        count_links = int(input("Напишите максимально возможное количество связей между узлами: "))

    graph = generator_graph(type_topology, count_nodes, count_links)

    draw_and_save(graph, type_topology)

    reformat_adjacency_list_nodes(graph, count_nodes)
    count_iterations = int(input('Напишите количество пакетов: '))
    list_of_threads = []
    for i in range(count_iterations):
        package = generator_of_package(graph, count_nodes)
        print(f"{i}-й пакет - {package}")
        thr = threading.Thread(target=routing_executor, args=(graph, package, list_of_delivered_package),
                               name=f"Поток-{i}")
        list_of_threads.append(thr)
        thr.start()
    for i in list_of_threads:
        i.join()

    print("Статистика графа и сетки:")
    print(f'Количество доставленных пакетов {len(list_of_delivered_package)}')
    print(f"Количество потерянных пакетов {count_iterations - len(list_of_delivered_package)}")
    statistics(graph, count_nodes, list_of_time_treatment, list_of_length_queue)
    input("Чтобы выйти нажмите любую клавишу")


if __name__ == "__main__":
    main()


