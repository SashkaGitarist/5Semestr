import random
import csv

def printf(file,massiv):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    i = 0
    for line in massiv:
        writer.writerow(line)
        i += 1
    outfile.close()

def printf2(file,massiv):
    dictlist = []
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    print(massiv)
    for i in range(len(massiv)):
        for key, value in massiv[i].items():
            #temp = str(key) + ';' + str(value)
            dictlist.append(key)
            # dictlist.append(':')
            dictlist.append(value)
            print(dictlist)
        j = 0
        writer.writerow(dictlist)
        j += 1
        dictlist.clear()
    outfile.close()
    printf3(massiv)

def printf3(massiv):
    dictlist = []
    outfile = open('4.csv', 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for i in range(len(massiv)):
        for key, value in massiv[i].items():
            #temp = str(key) + ';' + str(value)
            dictlist.append(key)
            # print(dictlist)
        j = 0
        writer.writerow(dictlist)
        j += 1
        dictlist.clear()
    outfile.close()

def g1(N,sv,file):
    A = []
    B = list(range(N))
    massiv = []
    for i in range(N):
        massiv.append([])
    c = random.choice(B)
    B.remove(c)
    A.append(c)
    while (B != []):
        c = random.choice(B)
        d = random.choice(A)
        massiv[c].append(d)
        B.remove(c)
        A.append(c)
    # print(massiv)
    for i in range(N):
        if len(massiv[i]) != 0:
            rand = random.randint(1, (sv - 1))
        else:
            rand = random.randint(1, sv)
        for j in range(rand):
            massiv[i].append(random.randint(0, N - 1))
    #print(massiv)
    printf(file,massiv)

def g2(N,sv,file,ves):
    A = []
    B = list(range(N))
    massiv = []
    for i in range(N):
        massiv.append({})
    c = random.choice(B)
    B.remove(c)
    A.append(c)
    while (B != []):
        c = random.choice(B)
        d = random.choice(A)
        massiv[c][d] = random.randint(1, ves)
        B.remove(c)
        A.append(c)
    #print(massiv)
    for i in range(N):
        if len(massiv[i]) != 0:
            rand = random.randint(1, (sv - 1))
        else:
            rand = random.randint(1, sv)
        for j in range(rand):
            massiv[i][random.randint(1, N - 1)] = random.randint(1, ves)
    #print(massiv)
    printf2(file, massiv)

def g3(N, sv, file, ves):
    A = []
    B = list(range(N))
    massiv = []
    for i in range(N):
        massiv.append({})
    c = random.choice(B)
    B.remove(c)
    A.append(c)
    while (B != []):
        c = random.choice(B)
        d = random.choice(A)
        jd = random.randint(1, ves)
        massiv[c][d] = jd
        massiv[d][c] = jd
        B.remove(c)
        A.append(c)
    #print(massiv)
    for i in range(N):
        rand = random.randint(1, sv)
        count = 0
        lenght = rand - len(massiv[i])
        if lenght > 0:
            while count != lenght:
                var = random.randint(0, N - 1)
                if len(massiv[var]) < sv:
                    jd2 = random.randint(1, ves)
                    massiv[i][var] = jd2
                    massiv[var][i] = jd2
                    count += 1
    #print(massiv)
    printf2(file, massiv)

def g4(N,sv,file):
    A = []
    B = list(range(N))
    massiv = []
    for i in range(N):
        massiv.append([])
    c = random.choice(B)
    B.remove(c)
    A.append(c)
    while (B != []):
        c = random.choice(B)
        d = random.choice(A)
        massiv[c].append(d)
        massiv[d].append(c)
        B.remove(c)
        A.append(c)
    #print(massiv)
    for i in range(N):
        rand = random.randint(1, sv)
        count = 0
        lenght = rand - len(massiv[i])
        if lenght > 0:
            while count != lenght:
                var = random.randint(0, N - 1)
                if len(massiv[var]) < sv:
                    massiv[i].append(var)
                    massiv[var].append(i)
                    count += 1
    #print(massiv)
    printf(file, massiv)

def g5(N,K,sv,file):
    massiv = []
    B = [i for i in range(K)]
    for i in range(N):
        massiv.append([])
    for i in range(N):
        A = []
        rand = random.randint(1, sv)
        count = 0
        while count != rand:
            if len(B) != 0:
                d = random.choice(B)
            else:
                d = random.randint(1, K-1)
            if d not in A:
                massiv[i].append(d)
                A.append(d)
                count += 1
                if d in B:
                    B.remove(d)
    printf(file, massiv)

print("Какой вы хотите увидеть граф?")
print("1) Ориентированный и не взвешенный")
print("2) Ориентированный и взвешенный")
print("3) Неориентированный и взвешенный")
print("4) Неориентированный и не взвешенный")
print("5) Двудольный")
vvod = input("Итак мое число: ")
N = int(input("Сколько будет вершин? "))
sv = int(input("А максимальное количество связей у одной вершины? "))
file = input("В какой файл вывести? ")
if vvod == '1':
    g1(N,sv,file)
if vvod == '2':
    ves = int(input("Максимальный вес ребра? "))
    g2(N,sv,file,ves)
if vvod == '3':
    ves = int(input("Максимальный вес ребра? "))
    g3(N,sv,file,ves)
if vvod == '4':
    g4(N,sv,file)
if vvod == '5':
    K = int(input("Сколько вершин будет во второй части? "))
    g5(N,K,sv,file)