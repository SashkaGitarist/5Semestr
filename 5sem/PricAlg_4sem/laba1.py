import csv

def csv_reader(file):
    graph = []
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        graph.append(row)
    return graph

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

    for s in string:
        j = matrix[0].index(s)
        begin = matrix[stolb.index(begin)][j]
    if begin in dop_sost:
        return True
    else:
        return False

with open('matrix.csv') as f_obj:
    matrix = csv_reader(f_obj)

string = 'babababababa'

if f(matrix, string):
    print('Допускающая')
else:
    print('Не допускающая')