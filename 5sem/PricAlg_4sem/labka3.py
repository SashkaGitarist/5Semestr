import csv

# https://www.youtube.com/watch?v=ex9sPLq5CRg - пример, который реализуется тут ;)

def csv_reader(file):
    graph = []
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        graph.append(row)
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if ',' in graph[i][j]:
                graph[i][j] = graph[i][j].split(',')
    return graph


# def minimization - берется входная таблица, ищется вход и выход,
# создается половинчатая матрица и ищутся пути сокращения / 1,2,3 + Эквиваленты

def minimization(matrix):
    dop_sost = []
    stolb = []
    for row in range(len(matrix)):
        i = matrix[row][0]
        if i.endswith('+'):
            matrix[row][0] = matrix[row][0].replace('+', '')
            begin = matrix[row][0]
        if i.endswith('*'):
            matrix[row][0] = matrix[row][0].replace('*', '')
            dop_sost.append(matrix[row][0])
        stolb.append(matrix[row][0])

    matrix1 = matrix
    while True:
        pairs = []
        for row1 in range(len(matrix1)):
            for row2 in range(len(matrix1)):
                if (matrix1[row1][1:] == matrix1[row2][1:]) and (row1 != row2):
                    pairs.append((matrix1[row1][0], matrix1[row2][0]))
        if len(pairs) == 0:
            for i in range(len(matrix1)):
                if matrix1[i][0] == begin:
                    matrix1[i][0] = matrix1[i][0] + '+'
                elif matrix1[i][0] in dop_sost:
                    matrix1[i][0] = matrix1[i][0] + '*'
            return matrix1
        mid = int(len(pairs) / 2)
        pairs = pairs[0:mid]

        for pair in pairs:
            if (pair[0] == begin) or (pair[1] == begin):
                begin = pair[0]
                for i in range(len(matrix1)):
                    if matrix1[i][0] == pair[1]:
                        index = i
                matrix1.pop(index)
                for i in range(len(matrix1)):
                    for j in range(len(matrix1[i])):
                        if matrix1[i][j] == pair[1]:
                            matrix1[i][j] = pair[0]
            elif (pair[1][0] in dop_sost):
                dop_sost.append(pair[0][0])
                for i in range(len(matrix1)):
                    if matrix1[i][0] == pair[1]:
                        index = i
                matrix1.pop(index)
                for i in range(len(matrix1)):
                    for j in range(len(matrix1[i])):
                        if matrix1[i][j] == pair[1]:
                            matrix1[i][j] = pair[0]
            else:
                for i in range(len(matrix1)):
                    if matrix1[i][0] == pair[1]:
                        index = i
                matrix1.pop(index)
                for i in range(len(matrix1)):
                    for j in range(len(matrix1[i])):
                        if matrix1[i][j] == pair[1]:
                            matrix1[i][j] = pair[0]


with open('matrix3.csv') as f_obj:
    matrix = csv_reader(f_obj)

print("Таблица до минимизации")
for row in matrix:
    print(row)

print("Таблица после минимизации")
matrix1 = minimization(matrix)

for row1 in matrix1:
    print(row1)
