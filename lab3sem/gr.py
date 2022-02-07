import csv
import random
from math import inf as infinity


class Vertice:
    count = 0

    def __init__(self):
        Vertice.count += 1
        self.id = Vertice.count - 1
        self.label = ""

    def set_label(self, label):
        self.label = label

    def get_index(self):
        return self.id

    def get_label(self):
        return self.label

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __str__(self):
        return f"{self.id}"

    def __int__(self):
        return self.id

    def __hash__(self):
        return self.id


class Connection:
    def __init__(self, from_vertice, to_vertice, weight=0):
        self.connection = True
        self.from_vertice = from_vertice
        self.to_vertice = to_vertice
        if not weight:
            self.weight = int(abs(random.gauss(10, 5))) + 1
        else:
            self.weight = weight

    def __eq__(self, other):
        if self.from_vertice == other.from_vertice and self.to_vertice == other.to_vertice:
            return True
        return False

    def __ne__(self, other):
        if self.from_vertice != other.from_vertice and self.to_vertice != other.to_vertice:
            return True
        return False

    def __hash__(self):
        return self.to_vertice.get_index()

    def __str__(self):
        return f"{self.to_vertice.get_index()}"  # ({self.weight})"

    def __int__(self):
        return self.to_vertice.get_index()


class Graph:
    def __init__(self, vertices_num, average_adjacency, oriented=False):
        self.oriented = oriented
        self.vertices_list = []
        self.vertices_num = vertices_num
        alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(self.vertices_num):
            vert = Vertice()
            self.vertices_list.append(vert)
        self.average_adjacency = average_adjacency
        self.adjacency_list = []
        self.adjacency_matrix = []
        for i in range(self.vertices_num):
            self.adjacency_list.append([])
            self.adjacency_matrix.append([infinity] * self.vertices_num)
        for i in range(self.vertices_num):
            self.adjacency_matrix[i][i] = 0

    def count_rows(self):
        return len(self.adjacency_list)

    def convert_inf_to_zeroes(self):
        for i in range(self.vertices_num):
            for j in range(self.vertices_num):
                if self.adjacency_matrix[i][j] is infinity:
                    self.adjacency_matrix[i][j] = 0

    def convert_to_transport_network(self):
        self.adjacency_list[self.vertices_num - 1] = []
        for adj in self.adjacency_list:
            for con in adj:
                if con.to_vertice.get_index() == 0:
                    adj.remove(con)

    def count_columns(self, row_num):
        return len(self.adjacency_list[row_num])

    def count_vertices(self):
        return len(self.vertices_list)

    def generate_adjacency_list(self):
        if not self.oriented:
            self.generate_not_oriented_graph()
        elif self.oriented:
            self.generate_oriented_graph()

    def generate_oriented_graph(self):
        if self.average_adjacency < self.vertices_num / 2:
            adjacencies = self.generate_adjacency(self.average_adjacency, self.average_adjacency / 8)
        else:
            adjacencies = self.generate_adjacency(self.average_adjacency,
                                                  (self.vertices_num - self.average_adjacency) / 8)
        for i in range(self.vertices_num):

            for j in range(int(adjacencies[i])):
                from_vertice = self.vertices_list[i]
                random_vertices_list = random.sample(self.vertices_list, len(self.vertices_list))
                to_vertice = random_vertices_list[0]
                con = Connection(from_vertice, to_vertice)
                back_con = Connection(to_vertice, from_vertice)
                while con in self.adjacency_list[i]:
                    random_vertices_list = random.sample(self.vertices_list, len(self.vertices_list))
                    to_vertice = random_vertices_list[0]
                    con = Connection(from_vertice, to_vertice)
                    back_con = Connection(con.to_vertice, con.from_vertice)
                while back_con in self.adjacency_list[back_con.from_vertice.get_index()]:
                    random_vertices_list = random.sample(self.vertices_list, len(self.vertices_list))
                    to_vertice = random_vertices_list[0]
                    con = Connection(from_vertice, to_vertice)
                    back_con = Connection(to_vertice, from_vertice)
                while con.from_vertice == con.to_vertice:
                    random_vertices_list = random.sample(self.vertices_list, len(self.vertices_list))
                    to_vertice = random_vertices_list[0]
                    con = Connection(from_vertice, to_vertice)
                    back_con = Connection(con.to_vertice, con.from_vertice)
                self.adjacency_list[i].append(con)
        for i in range(len(self.adjacency_list)):
            self.adjacency_list[i] = list(set(self.adjacency_list[i]))

    def generate_adjacency(self, m, d):
        adjacencies = []
        for i in range(self.vertices_num):
            adjacencies.append(int(random.gauss(m, d)))
        # for j in adjacencies:
        #     print(j)
        return adjacencies

    def generate_not_oriented_graph(self):
        if self.average_adjacency < self.vertices_num / 2:
            adjacencies = self.generate_adjacency(self.average_adjacency, self.average_adjacency / 8)
        else:
            adjacencies = self.generate_adjacency(self.average_adjacency,
                                                  (self.vertices_num - self.average_adjacency) / 8)
        if self.average_adjacency < 10:
            for i in range(len(adjacencies)):
                adjacencies[i] = int(adjacencies[i] / 1.5)
        else:
            for i in range(len(adjacencies)):
                adjacencies[i] = int(adjacencies[i] / 2)
        for i in range(self.vertices_num):
            for j in range(adjacencies[i]):
                if adjacencies[i] > self.vertices_num:
                    adjacencies[i] = self.vertices_num - 1
                if adjacencies[i] < 0:
                    adjacencies[i] = 0
                from_vertice = self.vertices_list[i]
                random_vertices_list = random.sample(self.vertices_list, len(self.vertices_list))
                to_vertice = random_vertices_list[j]
                con = Connection(from_vertice, to_vertice)
                back_con = Connection(con.to_vertice, con.from_vertice)
                while con in self.adjacency_list[i]:
                    random_vertices_list = random.sample(self.vertices_list, len(self.vertices_list))
                    to_vertice = random_vertices_list[j]
                    con = Connection(from_vertice, to_vertice)
                    back_con = Connection(con.to_vertice, con.from_vertice)
                while con.from_vertice == con.to_vertice:
                    random_vertices_list = random.sample(self.vertices_list, len(self.vertices_list))
                    to_vertice = random_vertices_list[j]
                    con = Connection(from_vertice, to_vertice)
                    back_con = Connection(con.to_vertice, con.from_vertice)
                if con.from_vertice.get_index() == i:
                    self.adjacency_list[i].append(con)
                    # print(con.to_vertice, end=", ")
                if con.to_vertice.get_index() == back_con.from_vertice.get_index():
                    self.adjacency_list[con.to_vertice.get_index()].append(back_con)
            # print("generated vertice", i)
            for k in range(len(self.adjacency_list)):
                self.adjacency_list[k] = list(set(self.adjacency_list[k]))
            temp_dict = {}
            for row in self.adjacency_list:
                for con in row:
                    fr = frozenset([con.to_vertice, con.from_vertice])
                    if fr not in temp_dict:
                        temp_dict[fr] = con.weight
                    else:
                        con.weight = temp_dict[fr]

    def get_adjacency(self):
        sum_adj = 0
        for _ in self.adjacency_list:
            sum_adj += len(_)
        return sum_adj / len(self.adjacency_list)

    def convert_to_adjacency_matrix(self):
        for i in range(self.vertices_num):
            for con in self.adjacency_list[i]:
                self.adjacency_matrix[i][con.to_vertice.get_index()] = con.weight


if __name__ == "__main__":
    g = Graph(10, 5)
    g.generate_adjacency_list()
    g.convert_to_adjacency_matrix()
    file = open('graph.csv', 'w')
    with file:
        for i in range(g.vertices_num):
            print(i, end=", ")
            for j in g.adjacency_list[i]:
                print(j.to_vertice.id, "(", j.weight, ")", sep="", end=", ")
            print()
            writer = csv.writer(file)
            writer.writerow([i] + g.adjacency_list[i])
        # print(g.get_adjacency())
    for row in g.adjacency_matrix:
        for con in row:
            print(con, end="\t")
        print()
