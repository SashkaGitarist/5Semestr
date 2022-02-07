import csv

def printf(file,massiv):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    i = 0
    for line in massiv:
        writer.writerow(line)
        i += 1
    outfile.close()

Edges = []
T = []
j = 0

# graph3 - 10 вершин, graph3_10 - 10 вершин, graph10 - 10 вершин, graph100 - 100 вершин, graph2000 - 2000
with open('graph10.csv', newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        d = row
        T.append([])
        d = d[0]
        q = ''
        for i in range(len(str(d))):
            if d[i] != ';':
                q = q+d[i]
                if i == len(str(d))-1:
                    T[j].append(q)
            else:
                if d[i] == ';':
                    T[j].append(q)
                    q = ''
        j += 1
    c = 0
    r = 0
    while c < len(T):
        for i in range(len(T[c])):
            if i < len(T[c])-r:
                Edges.append([int(T[c][i+1+r]), int(c), int(T[c][i+r])])
                r = i+1
        c += 1
        r = 0
    print(Edges)

N = 10

Edges.sort()
# print(Edges)
Comp = [i for i in range(N)]
massiv = []
for i in range(N):
    massiv.append([])
# print(Comp)
Ans = 0

for weight, start, end in Edges:
    if Comp[start] != Comp[end]:
        Ans += weight
        massiv[start].append(end)
        massiv[end].append(start)
        a = Comp[start]
        b = Comp[end]
        for i in range(N):
            if Comp[i] == b:
                Comp[i] = a
print("Вес остовного дерева: ", Ans)

# файл куда будем выводить
file = "ans_lab_3"
printf(file, massiv)
