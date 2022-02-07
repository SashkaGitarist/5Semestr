# номер варианта 18
# Нужно написать ПС для решения 3х задач методом динамического программирования с выводом на экран динамической шкалы\
# для максимального значения объема финансирования (Y) из предложенного диапазона в каждой задаче.
#
# Необходимо максимизировать: F(x) = Сумма всех перемножений (Ci * Xi)
# При этом необходимо выполнение условия: Сумма перемножений (Wi * Xi) <= Y

from prettytable import PrettyTable


def Max_f(Y, type, dict, Ci, Wi):
    print("Y = ", Y)
    chain = [0] * type
    res_N = [0] * type
    result = 0
    if type == 1:
        for i in range(1, int(Y / dict[type][Wi])):
            if i * Wi <= Y:
                if result < i * dict[type][Ci]:
                    chain[0] = i
                    result = i * dict[type][Ci]
        print(result)

        res_N[type-1] = result
        str = []
        for i in range(len(chain)):
            if i == chain[i]:
                str.append(chain[i])

            else:
                str.append(chain[i])
                str.append(', ')

        res_N[type - 1] = str

    elif type == 2:
        for i in range(1, int(Y / dict[type][Wi])):
            if i * Wi <= Y:
                if result < i * dict[type][Ci]:
                    chain[0] = i

                    result = i * dict[type][Ci]
        print(result)

        res_N[type-1] = result
        str = []
        for i in range(len(chain)):
            if i == chain[i]:
                str.append(chain[i])

            else:
                str.append(chain[i])
                str.append(', ')

        res_N[type - 1] = str
    print(str)


m = 4  # кол-во типов
n = 18  # кол-во значений переменной Y в заданном диапазоне

f_max_1_type = {}
f_max_2_type = {}
f_max_3_type = {}
f_max_4_type = {}

f1 = [0] * n
f2 = [0] * n
f3 = [0] * n

Y_start = 17  # - x1 = 17, ..., x18 = 34
Y_stop = 34

Y = [i for i in range(Y_start, Y_stop + 1)]  # Диапазон Y

table_Y = PrettyTable()

table_Y.field_names = ["i", "Wi", "Ci"]
table_Y.add_rows(
    [
        ["1", 6, 23],
        ["2", 7, 28],
        ["3", 8, 31],
        ["4", 9, 40]
    ]
)
print(table_Y)

# | i |  Wi | Ci |  i - Номер типа СрЗИ
# |---|-----|----|  Wi - стоимость СрЗИ каждого типа
# | 1 |  6  | 23 |  Ci - ценность СрЗИ каждого типа
# | 2 |  7  | 28 |  Xi - кол-во СрЗИ i-го типа
# | 3 |  8  | 31 |
# | 4 |  9  | 40 |
# |---|-----|----|

dict1 = {1: [6, 23], 2: [7, 28], 3: [8, 31], 4: [9, 40]}
#  print(dict1[key][0-Wi, 1 - Ci])


# TODO 2. Необходимо определить кол-во СрЗИ каждого типа выбор,
#  которых даёт максимальное значение ЦФ fi(Yi), j = i,n ,
#  где n - кол-во значений переменной Y в заданном диапазоне.

"""Решение 1 этапа с 1 типом"""

for i in range(len(Y)):
    #print("Y = ", Y[i])
    for type in range(m):
        tmp_arr = []
        Wi = dict1[type + 1][0]
        Ci = dict1[type + 1][1]

        if (type <= (Y[i] / Wi)) and (Y[i] - type * Wi >= 0) and (type + 1 == 1):
            tmp_arr.append((Ci * type))
            #print(tmp_arr)
        elif (type <= (Y[i] / Wi)) and (Y[i] - type * Wi >= 0) and (type + 1 == 2):
            tmp_arr.append((Ci * type) + f1[Y[i] - (Wi * type)])
            #print(tmp_arr)
        elif (type <= (Y[i] / Wi)) and (Y[i] - type * Wi >= 0) and (type + 1 == 3):
            tmp_arr.append((Ci * type) + f2[Y[i] - Wi * type])
            #print(tmp_arr)

        elif (type <= (Y[i] / Wi)) and (Y[i] - type * Wi >= 0) and (type + 1 == 4):
            tmp_arr.append((Ci * type) + f3[Y[i] - Wi * type])
            #print(tmp_arr)

        else:
            continue

        max_of_arr = max(tmp_arr)

        if (type + 1) == 1:
            f1.append(max_of_arr)
        elif (type + 1) == 2:
            f2.append(max_of_arr)
        elif (type + 1) == 3:
            f3.append(max_of_arr)
        else:
            pass

ff2 = open("T2.txt", "r")

for oit in ff2:
    print(oit)
