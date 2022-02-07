import csv

N = 10
graph = []
for i in range(N):
    graph.append([])
    k = 0
    while k < N:
        graph[i].append(0)
        k += 1

# Список для цветов 
col_gr = []
for i in range(N):
    col_gr.append([])
    k = 0
    while k < N:
        col_gr[i].append(-1)
        k += 1

adj_list = []
j = 0

# Читалка документа
with open('graph10.csv', newline='') as File:
    reader = csv.reader(File)
    for row in reader:
        adj_list.append([])
        d = row
        d = d[0]
        c = 0
        a = ''
        q = ''
        for i in range(len(str(d))):
            if d[i] != ';':
                q = q + d[i]
                if i == len(str(d)) - 1:
                    adj_list[j].append(q)
            else:
                if d[i] == ';':
                    adj_list[j].append(q)
                    q = ''
        j += 1

print("\nСписок связности: ", adj_list)

# Помечаем вершины, которые имеют связь
for k in range(len(adj_list)):
    for h in range(len(adj_list[k])):
        graph[k][int(adj_list[k][h])] = 1

print("\nМатрица связанных между собой вершин:")
for ver in graph:
    print(ver)
    pass

amount_conn = []  # Список для записи кол-ва связей
a_c_i = 0  # Индекс для вставки в список выше
sum = 0
for row in graph:
    for edge in range(len(row)):
        # print(row[edge])
        sum += row[edge]
    amount_conn.insert(a_c_i, sum)
    sum = 0
    a_c_i += 1

print('<=============>')
print("Вывод кол-ва связей у вершин")
print(amount_conn)  # Кол-во связей и хроматическое число

max_am_con = max(amount_conn)
index_of_max_ac = amount_conn.index(max_am_con)
print(index_of_max_ac)

palitra = [i for i in range(1, N + 100)]  # Используемые цвета
# print(palitra)
col_used = []  # Цвета, которые уже были использованы

# Раскраска вершины с максимальной связностью
for i in range(N):
    for j in range(N):
        if graph[index_of_max_ac][j] == 1 and col_gr[index_of_max_ac][j] == -1:

            colour_take = min(palitra)
            palitra.remove(colour_take)
            col_used.append(colour_take)
            # print(palitra)

            col_gr[index_of_max_ac][j] = colour_take
            col_gr[j][index_of_max_ac] = colour_take


"""
1) Нужно проверить есть ли ребро между вершинами (1 в graph) и не окрашено ли ребро (-1 в col_gr)
2) Смотрим какие ребра исходят из вершин, связанных с нашим ребром: (v1--e1--v2), где v1,2 - вершины, а e1 - ребро
3) 
"""
temp_ar_cu = col_used.copy()
for i in range(N):
    for j in range(N):
        if graph[i][j] == 1 and col_gr[i][j] == -1:
            for col in col_gr[i]:
                if col != -1:
                    temp_ar_cu.remove(col)
                    """
Если у нас список не пустой,т.е есть доступные цвета, то красим в минимальный допустимый цвет
Иначе берём минимальный из палитры, т.е. берём новый цвет
"""
                    if len(temp_ar_cu) != 0:
                        colour_take = min(temp_ar_cu)
                        col_gr[i][j] = colour_take
                        col_gr[j][i] = colour_take
                        break

                    else:
                        colour_take = min(palitra)
                        palitra.remove(colour_take)
                        col_used.append(colour_take)

                        col_gr[i][j] = colour_take
                        col_gr[j][i] = colour_take
                        break


print('<=================>')
for ver in col_gr:
    print(ver)
