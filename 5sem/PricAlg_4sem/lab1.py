import csv


def csv_reader(file):
    graph = []
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        graph.append(row)
    return graph


def f(matrix, string):

    # Проверка алфавита строки на наличие постороннего символа
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
        # Если у вершины +, то это начальная вершина
        if i.endswith('+'):
            i = i.replace('+', '')
            begin = i
        # Если у вершины *, то это допускающая вершина
        if i.endswith('*'):
            i = i.replace('*', '')
            dop_sost.append(i)
        stolb.append(i)

    path = []
    for s in string:
        j = matrix[0].index(s)
        begin = matrix[stolb.index(begin)][j]
        path.append(begin)

    for i in matrix:
        print(i)

    print("\nДопускающее состояние в ", *dop_sost)
    for i in path:
        print(i, end=' ')

    print(" ")

    if begin in dop_sost:
        return True
    else:
        return False


with open('matrix.csv') as matrix:
    matrix_from_csv = csv_reader(matrix)

string = ''.join(['0101' for i in range(0, 100)])
if f(matrix_from_csv, string):
    print(f'Строка {string} допускающая')
else:
    print(f'Строка {string} не допускающая')
