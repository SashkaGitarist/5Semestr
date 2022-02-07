import csv


# Функция для построения правильного построения языка по правилам
def Tree(rules, str):
    p = len(str) - 1
    while p >= 0:
        s = ''
        beg = p
        for i in str[p::-1]:
            end = p
            s += i
            beg -= 1
            for flag in range(len(rules)):
                rule = rules[flag][1:]
                s = s[::-1]
                if s in rule:
                    tree.insert(0, [rules[flag][0], '-', str[beg + 1:end + 1]])
                    str[beg + 1:end + 1] = rules[flag][0]
                    return str
                s = s[::-1]
        p -= 1


# Построение дерева в выходном файле csv
def tree_write(tree):
    file = open('lab8.csv', 'w', newline='')
    writer = csv.writer(file, delimiter=';', quotechar='"')
    dict = []
    for i in range(len(tree)):
        dict.append(tree[i][0])
        dict.append(tree[i][1])
        for j in range(len(tree[i][2])):
            dict.append(tree[i][2][j])
        j = 0
        writer.writerow(dict)
        j += 1
        dict.clear()
    file.close()


alphabet = ['x', '+', '-', '*', '/', '(', ')']
rules = [['S', 'S+S', '|', 'S-L', '|', 'L', '(S)'],
         ['L', 'L*M', '|', 'L/M', '|', 'M'],
         ['M', '(S)', '|', 'x']]

string = '(x*x)'

# Условия, результат которых будет дерево или вывод сообщения, что язык недопускающий
flag = False

for i in string:
    if i not in alphabet:
        flag = True

if not flag:
    tree = []
    s = list(string)
    if len(s) == 1:
        print('Недопускающая!')
        flag = True
    while len(s) != 1:
        s = Tree(rules, s)
        if s is None:
            flag = True
            print('Недопускающая')
            break
    if not flag:
        tree_write(tree)
else:
    print('Неверные символы')
