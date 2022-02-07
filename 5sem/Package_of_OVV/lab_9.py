class Node:
    def __init__(self, id, neighborlist):
        self.id: int = id
        self.neighbors = tuple(neighborlist)    #кортеж соседей
        self.busy_colors = []   #список занятых уже цветов

def pow_sort(powers): # сортирует вершины по их степени связности
    list_powers = list(powers.items())
    list_powers.sort(reverse=True, key=lambda i: i[1])
    list_powers = list(i for i, j in list_powers)
    return list_powers

def refactor(Matrix, size):
    V = []
    for i in range(size):
        neighborlist = []#список соседей
        for j in range(size):
            if int(Matrix[i][j]) != 0:
                neighborlist.append(j)
        V.append(Node(i, neighborlist))
    return V

def painting_edges(V, sorted, edges):
    maxcolor = 0
    while len(sorted) > 0:
        current_Vertex = sorted.pop(0)
        for j in V[current_Vertex].neighbors:
            if edges[current_Vertex][j] == -1:
                for k in range(0, maxcolor+1):
                    if k not in V[current_Vertex].busy_colors and k not in V[j].busy_colors:
                        V[current_Vertex].busy_colors.append(k)
                        V[j].busy_colors.append(k)
                        edges[current_Vertex][j] = k
                        edges[j][current_Vertex] = k
                        break
                if edges[current_Vertex][j] == -1:
                    maxcolor += 1
                    V[current_Vertex].busy_colors.append(maxcolor)
                    V[j].busy_colors.append(maxcolor)
                    edges[current_Vertex][j] = maxcolor
                    edges[j][current_Vertex] = maxcolor
    print("Матрица раскраски рёбер по цветам:")
    for i in edges:
        for j in i:
            if j==-1: print("*", end='\t')
            else: print(f"{j}", end = '\t')
        print()
    print(f"Хроматический индекс: {maxcolor+1}")

if __name__ == '__main__':
    import csv
    #with open("adj_list_lab_1_for_3_new_type.csv", mode='r', encoding="utf-8", )as r_file:#-----------------string4
    with open("adj_list_lab_1_for_9.csv", mode='r', encoding="utf-8", )as r_file:#real
        file_reader = csv.reader(r_file, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        Adj_list = []
        for row in file_reader:
            Adj_list.append(row)
    size = len(Adj_list)
    Adj_list_final = [[int(j) for j in i] for i in Adj_list]

    Matrix = []
    for i in range(size):
        Matrix.append([0] * size)

    for i in range(len(Adj_list_final)):#преобразование из списка смежности в матрицу смежности
        for j in range(0, len(Adj_list_final[i]) - 1, 2):
            edge_temp = Adj_list_final[i][j]
            weight_temp = Adj_list_final[i][j + 1]
            Matrix[i][edge_temp] = weight_temp

    size = len(Matrix)
    edges = [[-1]*size for i in range(size)]
    powers = {}
    for i in range(size):
        pow = 0
        for j in range(size):
            if Matrix[i][j]!=0: pow+=1
        powers[i] = pow

    sorted = pow_sort(powers)
    print("Отсортированный список вершин и их степеней связности")
    print("vertex\t\tdegree of connectivity")
    for i in range(len(Matrix)):
        print(sorted[i], "\t\t\t", powers[sorted[i]])
    V = refactor(Matrix, size)
    painting_edges(V, sorted, edges)