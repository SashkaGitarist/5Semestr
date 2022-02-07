import csv
import re

global f, begin, str
matrix= []
graph = {}
magazine = []
dop_sost = []

# Функция csv_reader не нуждается в представлении, но все же
# Данная функция необходима для чтения данных из csv, в данном случае она ищет
# "," - они необходимы для выделения значений и "/" она необходима для разделения значений csv файла


def csv_reader(file):
    global matrix, matrix_, begin, dop_sost
    reader = csv.reader(file,delimiter=';')

    for row in reader:
        matrix.append(row)

    for i in range(len(matrix) - 1):
        graph[tuple(matrix[i][0].split(','))] = matrix[i][1].split('/')
        h = matrix[i][0].split(',')

    dop_sost = matrix[len(matrix) - 1][1].split(',')

    begin = matrix[len(matrix) - 1][0]

    print('Автомат : ', graph)
    print('Начальное состояние : ',begin)
    print('Конечные состояния : ', dop_sost)

# Функция Avtomat_with_MP - прогоняет автомат с магазинной памятью по заданному пути
# Также здесь рассматриваются случаи пустого автомата с магазинной паматью

def Avtomat_with_MP():
    global graph, magazine, str, begin
    sost = begin
    mag_symb = 'eps'
    for i in range(len(str)):
        s = str[i]
        for i in graph.keys():
            if sost == i[0] and (s == i[1] or i[1] == 'eps') and mag_symb == i[2]:
                value = graph[i]
                sost = value[0]
                if mag_symb == 'eps' and value[1] == 'eps':
                    pass
                elif mag_symb == 'eps':
                    magazine.extend(value[1].split(','))
                elif value[1] == 'eps':
                    magazine.pop()
                else:
                    magazine.pop()
                    magazine.extend(value[1].split(','))
                if len(magazine) == 0:
                    mag_symb = 'eps'
                else:
                    mag_symb = magazine[-1]
        print(sost, mag_symb, magazine)
    return sost, mag_symb



with open('matrix.csv', "r", newline='') as file:
    csv_reader(file)

# str - задается путь по которому будет идти автомат

str = ')(),(),()('
print('Входная строка: ' + str)

sost, mag_symb = Avtomat_with_MP()
if (sost in dop_sost) and mag_symb == 'eps':
    print('Допускающая по допускающему состоянию и по пустому магазину')
elif (sost in dop_sost):
    print('Допускающая по допускающему состоянию')
elif mag_symb == 'eps':
    print('Допускающая по пустому магазину')
else:
    print('Цепочка не допустима')
