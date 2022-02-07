import csv
import math
import time as t

time_start = t.time()

with open ("adj_list_lab_1_for_3_new_type.csv", mode = 'r', encoding = "utf-8",)as r_file:
    file_reader = csv.reader(r_file, delimiter =",", quoting=csv.QUOTE_MINIMAL)
    Adj_list = []
    for row in file_reader:
        Adj_list.append(row)
size = len(Adj_list)
Adj_list_final = [[int(j) for j in i]for i in Adj_list]

Matrix = []
for i in range(size):
    Matrix.append([0]*size)

for i in range(len(Adj_list_final)):
    for j in range(0, len(Adj_list_final[i]) - 1, 2):
        edge_temp = Adj_list_final[i][j]
        weight_temp = Adj_list_final[i][j+1]
        Matrix[i][edge_temp] = weight_temp
for i in range(len(Matrix)):
    print(Matrix[i])
count_edge = 0
for i in range(len(Matrix)):
    for j in range(len(Matrix[i])):
        if Matrix[i][j] != 0:
            count_edge += 1
print("count edges is ", count_edge/2)

"""
DIJKSTRA-ALGORITM---------------------------------------------------------------------------------
"""
Adjacency_matrix = Matrix
def get_link_v(current_vertex, Adjacency_matrix):# на вход поступает текущая рассматриваемая вершина и матрица смежности
    for i, weight in enumerate(Adjacency_matrix[current_vertex]):#перебираются строки матрицы смежности
        #enumerate() возвращает индекс и значение элемента из списка, то есть в нашем случае вернет индекс вершины и вес ребра
        if weight > 0:#если полученный вес ребра больше нуля
            yield i#возвращаем список смежных вершин с текущей вершиной (при выходе из функции)

def arg_min(Result_list, Set_of_considered_vertices):#ф -ция возвращает вершину с минимальным весом ребра, соединяющего ее с предыдущей рассматриваемой вершиной
    index_min_vertex = -1#номер вершины, для которой было подсчитано минимальное значение, если в конце работы этой функции знаечение окажется "-1", то работа алгоритма завершается, так как были пройдены все вершины
    max_value_in_Result_list = max(Result_list)#максимальное значение из результирующей строки
    for i, value in enumerate(Result_list):# перебор значений из результирующей строки
        if value < max_value_in_Result_list and i not in Set_of_considered_vertices:#нахождение минмального значения из результирующей строки
            max_value_in_Result_list = value#обмен значениями
            index_min_vertex = i#обмен значениями
    return index_min_vertex#возвращаем индекс вершины


count_vertex = len(Adjacency_matrix)#Кол-во вершин
Result_list = [math.inf]*count_vertex# строка результирующей таблицы, куда пока что записываются бесконечности

current_vertex = 0#текущая рассматриваемая вершина(изначально ноль)
Set_of_considered_vertices = {current_vertex}#множество рассмотреных вершин
Result_list[current_vertex] = 0#вес ребра (для стартовой вершины - ноль)

while current_vertex != -1:#
    for j in get_link_v(current_vertex, Adjacency_matrix): #перебор всех смежных вершин с текущей(v)
         #Здесь ф-ция get_link_v вернет список из всех смежных вершин с текущей
        if j not in Set_of_considered_vertices: #если текущая вершина не входит в множество рассмотреных вершин
            current_weight = Result_list[current_vertex] + Adjacency_matrix[current_vertex][j] #формирование текушего веса связи для j-ой вершины
            if current_weight < Result_list[j]: #если текущий вес меньше. чем тот что уже есть в матрице смежности
                Result_list[j] = current_weight #то происходит сохранение нового веса связи

    current_vertex = arg_min(Result_list, Set_of_considered_vertices) #выбор вершины с минимальным весом ребра, соединяющего ее с предыдущей рассматриваемой вершиной
    if current_vertex > 0:
        Set_of_considered_vertices.add(current_vertex)#добавление вершины в множество просмотренных вершин

for i in range(len(Result_list)):
    print("кратчайший путь до", i, " = ", Result_list[i])

time = t.time() - time_start
print('running time program is ->', round(time, 4), '<- seconds')

