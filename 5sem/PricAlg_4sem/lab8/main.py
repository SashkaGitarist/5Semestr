import csv


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
                    tree.insert(0, [rules[flag][0], str[beg + 1:end + 1]])
                    str[beg + 1:end + 1] = rules[flag][0]
                    return str
                s = s[::-1]
        p -= 1


def treeWrite(tree):
    file = open('lab8.csv', 'w', newline='')
    writer = csv.writer(file, delimiter=';', quotechar='"')
    dict = []
    for i in range(len(tree)):
        dict.append(tree[i][0])
        for j in range(len(tree[i][1])):
            dict.append(tree[i][1][j])
        j = 0
        writer.writerow(dict)
        j += 1
        dict.clear()
    file.close()


rules = []
chain = ''

file1 = open("structure", "r")
print("Файл: ")
while True:
    line = file1.readline().strip()
    if not line:
        break
    rules.append(line.split(","))
file1.close
print("rul: ", rules)

print("Цепочка с файла: ")
file_chain = open("chain", "r")
chain = file_chain.readline().strip()
print(chain)

flag = False
tree = []
s = list(chain)
if len(s) == 1:
    print('Недопускающая')
    flag = True
while len(s) != 1:
    s = Tree(rules, s)
    if s is None:
        flag = True
        print('Недопускающая')
        break
if not flag:
    print('Допускающая, дерево разбора в файле -> lab8.csv')
    treeWrite(tree)

