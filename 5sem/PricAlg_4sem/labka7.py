import re
import csv
import time

global rules, graph, flag, string, result
rules = []
graph = {}
alphabet = []
start = ''
flag = False
string = ''
result=''

# csv reader - необходим для чтения данных из csv файла, также здесь читается алфавит и условия правил(->)

def csv_reader(file):
    global rules, graph, alphabet, start
    l = []
    reader = csv.reader(file,delimiter=';')
    for row in reader:
        rules.append(row)
    #print(rules)
    for i in range(len(rules)):
        rules[i] = re.split(r'->',rules[i][0])
        if re.findall(r'[a-z]',rules[i][1]) not in alphabet:
            alphabet.extend(re.findall(r'[a-z]',rules[i][1]))
    for i in range(len(rules)):
        if rules[i][0] not in graph.keys():
            graph[rules[i][0]] = []
        graph[rules[i][0]].append(rules[i][1])
    #print(graph)
    start = rules[0][0]
    alphabet = list(set(alphabet))

#задача правил для автомата с пустым магазином

def KS_to_MPAvtomat():
    global graph, alphabet
    avtomat = {}
    for i in graph.keys():
        if len(graph[i]) != 1:
            avtomat[('q', 'lambda', i)] = []
            for j in graph[i]:
                avtomat[('q', 'lambda', i)].append(('q',j))
        else:
            avtomat[('q', 'lambda', i)] = ('q',''.join(graph[i]))
    for i in alphabet:
        avtomat[('q',i,i)] = ('q','lambda')
    return avtomat

# Создание пустых ячеек, для таблицы

def create_cell(first, second):
    res = set()
    if first == set() or second == set():
        return set()
    for flag in first:
        for s in second:
            res.add(flag+s)
    return res

# Данная функция необходима для построения таблицы, черрез графы

def f(graph, inp):
    terms = []
    varies = []
    for i in graph.keys():
        for j in range(len(graph[i])):
            if str.islower(graph[i][j]):
                terms.append([i,graph[i][j]])
            else:
                varies.append([i, graph[i][j]])
    #print(varies, terms)
    length = len(inp)
    var0 = [va[0] for va in varies]
    var1 = [va[1] for va in varies]

    table = [[set() for _ in range(length-i)] for i in range(length)]

    for i in range(length):
        for te in terms:
            if inp[i] == te[1]:
                table[0][i].add(te[0])

    for i in range(1, length):
        for j in range(length - i):
            for k in range(i):
                #print(i, j, k)
                row = create_cell(table[k][j], table[i-k-1][j+k+1])
                for ro in row:
                    if ro in var1:
                        table[i][j].add(var0[var1.index(ro)])
    return table

#Функция необходима для того, чтобы проверять что будет если при том или ином значении лямбды

def ex(mag_sym, value, stack):
    if mag_sym == 'lambda' and value[1] == 'lambda':
        pass
    elif mag_sym == 'lambda':
        stack.extend(list(value[1]))
    elif value[1] == 'lambda':
        stack.pop()
    else:
        stack.pop()
        stack.extend(list(value[1]))
    if len(stack) == 0:
        mag_sym = 'lambda'
    else:
        mag_sym = stack[-1]
    return mag_sym, stack

def find(avtomat, string):
    global start
    #return find_(avtomat,string,'q',start,[start])
    return proverka(avtomat,string, 0, start, [start], [start], start)

# Данная функция проверяет цепочку на соответствие грамматике

def vivod(tab, inp):
    for c in inp:
        print("\t{}".format(c), end="\t")
    print()
    for i in range(len(inp)):
        print(i+1, end="")
        for c in tab[i]:
            if c == set():
                print("\t{}".format("_"), end="\t")
            else:
                print("\t{}".format(c), end=" ")
        print()

    if 'S' in tab[len(inp)-1][0]:
        print("Цепочка соответствует грамматике")
        return 'S'
    else:
        print("Цепочка не соответствует грамматике")

# Проверка на допускающую и что делать, если она не допускающая
        
def proverka(avtomat, string, i, m, st1, st2, m2):
    global flag,start
    mag_sym = m
    stack = st1
    if len(string) <= i:
        if len(stack) == 0:
            flag = True
            print('Допускающая')
            exit(0)
        return mag_sym, stack
    elif len(stack) > len(string):
        if len(stack) == 0:
            flag = True
            print('Допускающая')
            exit(0)
        return m2, st2
    else:
        word_symbol = string[i]
        for j in avtomat.keys():
            if (word_symbol == j[1] or j[1] == 'lambda') and mag_sym == j[2]:
                value = avtomat[j]
                if isinstance(value, tuple) == False:
                    for k in range(len(value)):
                        stack_ = stack.copy()
                        mag_sym_ = mag_sym
                        mag_sym_, stack_ = ex(mag_sym_, value[k], stack_)
                        if j[1] == 'lambda':
                            mag_sym_, stack_  = proverka(avtomat, string, i, mag_sym_, stack_, stack, mag_sym)
                        else:
                            mag_sym_, stack_ = proverka(avtomat, string, i+1, mag_sym_, stack_, stack, mag_sym)
                    stack = stack_.copy()
                    mag_sym = mag_sym_
                    return mag_sym, stack
                else:
                    mag_sym_, stack_ = ex(mag_sym, value, stack)
                    if j[1] == 'lambda':
                        mag_sym_, stack_ = proverka(avtomat, string, i, mag_sym_, stack_, stack, mag_sym)
                    else:
                        mag_sym_, stack_ = proverka(avtomat, string, i + 1, mag_sym_, stack_, stack, mag_sym)
                    stack = stack_.copy()
                    mag_sym = mag_sym_
                    return mag_sym, stack
                break
        return mag_sym, stack

csv_file = "lab7.csv"
with open(csv_file, "r", newline='') as f_obj:
    csv_reader(f_obj)
avtomat = KS_to_MPAvtomat()
print(avtomat)
#print(graph)

string = 'aaass'

string = list(string)
for i in string:
    if i not in alphabet:
        print('Недопустимые символы')
        exit(0)
result = vivod(f(graph, string), string)
string.reverse()
mag_sym, stack = find(avtomat, string)
if flag == False:
    print('Недопускающая')