import csv


# Читалка csv-файла
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


# функция для нахождения недопустимого символа, начального и допускающего состояния
# Также эта функция отвечает за принадлежность строки к автомату
def f(matrix, string):
    for i in string:
        if i in matrix[0]:
            continue
        else:
            print('Недопустимый символ в цепи')
            return False

    dop_sost = []
    stolb = []
    for row in matrix:
        i = row[0]
        if i.endswith('+'):
            i = i.replace('+', '')
            begin = i
        if i.endswith('*'):
            i = i.replace('*', '')
            dop_sost.append(i)
        stolb.append(i)
    return f1(matrix, string, 0, begin, stolb, dop_sost)


def f1(matrix, string, c, begin, stolb, dop_sost):
    if matrix[stolb.index(begin)][1] != '':
        finish = matrix[stolb.index(begin)][1]

        # Проверка finish-а к принадлежности к классу - list
        if not isinstance(finish, list):
            if f1(matrix, string, c, finish, stolb, dop_sost):
                return True
            else:
                return
        else:
            for i in finish:
                if f1(matrix, string, c, i, stolb, dop_sost):
                    return True
                else:
                    continue
    elif (c == len(string)):
        if begin in dop_sost:
            return True
        else:
            return False

    else:
        s = string[c]
        finish = matrix[stolb.index(begin)][matrix[0].index(s)]
        if finish == '':
            if begin in dop_sost:
                return True
            else:
                return
        elif not isinstance(finish, list):
            if f1(matrix, string, c + 1, finish, stolb, dop_sost):
                return True
            else:
                return
        else:
            for i in finish:
                if f1(matrix, string, c + 1, i, stolb, dop_sost):
                    return True
                else:
                    continue


with open('matrix2.csv') as csv_matrix:
    matrix = csv_reader(csv_matrix)

string = 'bbb'

if f(matrix, string):
    print('Допускающая')
else:
    print('Не допускающая')
