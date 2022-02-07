import csv


def csv_dict_reader(name):
    file = open(name, 'r')
    lines = file.readlines()
    arr = [list(map(str, lines[i].replace('\n', '').split(';'))) for i in range(len(lines))]
    file.close()
    step = {i[0]: i[1:] for i in arr[1:]}
    tmp = arr[0][1:]
    variables = {tmp[i]: i for i in range(len(tmp))}
    final = arr[0][0]
    print(step)
    print(variables)
    print(final)
    return step, variables, final


def closed(variables, step, line):
    line = line.split()
    tmp1 = set()
    first = set()
    first.add(list(step.keys())[0])
    for i in line:
        for s in first:
            index = variables[i]
            tmp1 = tmp1.union(step[s][variables['e']])
            if i != len(line):
                if len(step[s][index]) == 0:
                    tmp1.discard(s)
            tmp1 = tmp1.union(step[s][index])
        first = tmp1.copy()
    return first


step, variables, final = csv_dict_reader('lb2test2.csv')
line = '0 1 1 0 1 0'

result = closed(variables, step, line)

tt = 0
for i in range(len(final)):
    if final[i] in result:
        tt = 1
        break
if tt == 1:
    print('Строка удовлетворяет условию')
else:
    print('Строка не удовлетворяет условию')