import random
import threading
import time

import matplotlib.pyplot as plt
import networkx as nx


def generator_graph(type_topology: int, count_nodes: int, count_links: int):
    queue = []
    adjacency_list = []
    graph = nx.Graph()
    if type_topology == 1:  # кольцо

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        for i in range(0, count_nodes, 1):
            graph.add_edge(i, i + 1, weight=random.randint(0, 9999))

        graph.add_edge(0, count_nodes, weight=random.randint(0, 9999))

    elif type_topology == 2:  # звезда

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        random_node = random.randint(0, count_nodes)

        for i in range(count_nodes):
            if random_node == i:
                continue
            else:
                graph.add_edge(i, random_node, weight=random.randint(0, 9999))

    elif type_topology == 3:  # случайная хрень

        for i in range(count_nodes):
            graph.add_node(i, queue=queue, adjacency_list=adjacency_list)

        for j in range(count_nodes):
            for i in range(count_links):
                rand = random.randint(0, count_nodes)
                if rand == j:
                    continue
                else:
                    graph.add_edge(j, rand, weight=random.randint(0, 9999))

    return graph


def generator_of_package(graph, count_nodes):
    return random.randint(0, count_nodes)


def package_treatment():
    time_sleep = random.random() * 1.5
    time.sleep(time_sleep)
    return round(time_sleep)


# Функция для отображения графа
def create_graphics(treatment: dict, list_of_length_queue: list):  # рисует графики
    x_treatment = []
    y_treatment = []
    for i in treatment:
        x_treatment.append(i)
        y_treatment.append(treatment[i])
    x_treatment.sort()
    gpraphik_one = plt.plot(x_treatment, y_treatment)
    plt.show()
    x_treatment.clear()
    for i in range(len(list_of_length_queue)):
        x_treatment.append(i)
    gpraphik_two = plt.plot(x_treatment, list_of_length_queue)
    plt.show()


def draw_and_save(graph, type_topology: int):
    if type_topology == 1:  # ring
        nx.draw_circular(graph, with_labels=True, node_size=230, label={'weight'}, node_color="red")
    elif type_topology == 2:  # star
        nx.draw(graph, with_labels=True, node_size=230, node_color="red")
    elif type_topology == 3:  # random
        nx.draw(graph, with_labels=True, node_size=230, node_color="red")

    plt.savefig("graph.png")
    plt.show()


delivered_package = 0
lost_package = 0

dict_of_package_treatment = {}
list_of_length_queue = []

locker = threading.Lock()


def routing_executor(graph, package: list, source_node: int):
    global dict_of_package_treatment, list_of_length_queue, lost_package, delivered_package
    try:
        graph.nodes[source_node]['queue'].append(package)
    except KeyError:
        lost_package += 1
    try:
        graph.nodes[source_node]['queue'].sort(key=lambda x: x[2])
    except KeyError:
        pass
    try:
        package = graph.nodes[source_node]['queue'].pop(0)
    except KeyError:
        pass
    print(f"{package[1]}-ый пакет с приоритетом {package[2]} в узле {source_node},{threading.current_thread().name}")
    dict_of_package_treatment[package[1]].append(package_treatment())
    summator = 0
    for i in range(len(graph.nodes)):
        try:
            summator += len(graph.nodes[i]['queue'])
        except KeyError:
            summator += 0
    list_of_length_queue.append(
        summator / len(graph.nodes))
    while True:
        try:
            path = nx.dijkstra_path(graph, source_node, package[0])
        except:
            print(
                f"###(*=*)### Здеся нет пути к этому узлу из узла , {package[1]}-ый пакет с приоритетом {package[2]}"
                f" в узле {source_node} потерялся :( {threading.current_thread().name} ###(*=*)###")
            lost_package += 1
            break
        if package[0] == source_node:
            print(
                f"\n{package[1]}-ый пакет с приоритетом {package[2]} доставлен в узел {source_node},  {threading.current_thread().name} ---(0_0)---\n")
            delivered_package += 1
            break
        else:
            try:
                graph.nodes[path[1]]['queue'].append(
                    package)
            except KeyError:
                print(f"###(*=*)### {package[1]}-ый пакет с приоритетом {package[2]} потерялся :( ###(*=*)###")
                lost_package += 1
        source_node = path[1]


def main():
    type_topology = int(input("Напишите топологию: 1 - кольцо, 2 - звезда, 3 - случайный граф: "))
    count_nodes = int(input("Напишите количество узлов: "))
    count_links = None

    if type_topology == 3:
        count_links = int(input("Количество связей от узла: "))

    graph = generator_graph(type_topology, count_nodes, count_links)
    draw_and_save(graph, type_topology)
    count_package = int(input("Количество пакетов: "))
    list_of_threads = []
    packages_list = []
    for i in range(count_package):
        packages_list.append([generator_of_package(graph, count_nodes), i, random.randint(0, 89)])

    for i in range(count_package):
        package = packages_list.pop(0)
        print(f"{i}-ый пакет - {package} с приоритетом {package[2]}")
        source_node = random.randint(0, len(graph.nodes))
        dict_of_package_treatment[package[1]] = []
        thr = threading.Thread(target=routing_executor, args=(graph, package, source_node), name=f"поток-{i}")
        list_of_threads.append(thr)
        thr.start()

    for i in list_of_threads:
        i.join()

    print(list_of_length_queue)
    print(f"Количество доставленных пакетов: {delivered_package}")
    print(f"Количество потерянных пакетов: {count_package - delivered_package}")
    print(f"Выходная средняя длина очереди: {sum(list_of_length_queue) / len(list_of_length_queue)}")
    # create_graphics(dict_of_package_treatment, list_of_length_queue)


if __name__ == "__main__":
    main()
