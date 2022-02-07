import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import L2_p

np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)

ff2 = open("TT2.txt", "r")
ff1 = open("TT1.txt", "r")

def neogran_zadacha(capacity, item_list):
    k = 0
    x1 = len(item_list) // item_list[k][1]

    f1 = item_list[k][0]
    knapsack = [[] for i in range(capacity + 1)]
    knapsack_ = [[0, 0] for i in range(capacity + 1)]
    knapsack.append(knapsack_)

    for i in range(capacity + 1):
        knapsack_[i][1] = i // item_list[k][1]
        knapsack_[i][0] = item_list[k][0] * knapsack_[i][1]

    k = k + 1
    f_max = 0
    max = 0

    while k != len(item_list) + 1:
        knapsack_1 = knapsack_
        max = 0
        f_max = 0

        for i in range(capacity + 1):
            if (i // item_list[k - 1][1]) == 0:
                max = 0
                f_max = item_list[k - 1][0] * max + knapsack_1[i - item_list[k - 1][1] * max][0]

            else:
                x_ = [l for l in range((i // item_list[k - 1][1]) + 1)]
                f_max = 0
                for j in x_:
                    f_ = item_list[k - 1][0] * j + knapsack_1[i - item_list[k - 1][1] * j][0]
                    if f_ >= f_max:
                        max = j
                        f_max = f_

            knapsack_[i][0] = f_max
            knapsack_[i][1] = max
        k = k + 1
    return knapsack_


def ogran_zadacha(capacity, item_list):
    k = 0
    knapsack_ = [[0, 0] for i in range(capacity + 1)]
    knapsack_1 = [0 for i in range(capacity + 1)]
    x_ = []
    k = 0
    while k != len(item_list):
        k = k + 1
        for i in range(len(knapsack_)):
            knapsack_1[i] = (knapsack_[i][0], knapsack_[i][1])
        max = 0
        f_max = 0
        for i in range(capacity + 1):
            if (i // item_list[k - 1][1]) == 0:
                max = 0
                f_max = item_list[k - 1][0] * max + knapsack_1[i - item_list[k - 1][1] * max][0]
            else:
                for l in range((i // item_list[k - 1][1]) + 1):
                    if l <= item_list[k - 1][2]:
                        x_.append(l)
                for j in x_:
                    f_ = item_list[k - 1][0] * j + knapsack_1[i - item_list[k - 1][1] * j][0]
                    if f_ >= f_max:
                        max = j
                        f_max = f_
                x_ = []
            knapsack_[i][0] = f_max
            knapsack_[i][1] = max
    return knapsack_


def graph_knapsack(y1, y2, f, f1, f2):
    x = [y1 + i for i in range(y2 - y1 + 1)]
    fig, ax = plt.subplots()
    plt.title("")
    ax.plot(x, f, marker='.', color='y', linewidth=1)
    print("Значения желтого графика:", *f)
    ax.plot(x, f1, marker='.', color='k', linewidth=1)
    print("Значения черного графика: ", *f1)
    ax.plot(x, f2, marker='.', color='c', linewidth=1)
    print("Значения голубого графика: ", *f2)
    plt.ylabel("ось y", fontsize=12)

    axes = plt.gca()
    axes.set_xlim([y1, y2])
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(50))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    ax.grid(which='major', color='gray')
    ax.grid(which='minor', color='gray', linestyle=':')
    fig.set_figwidth(6)
    fig.set_figheight(4)
    plt.show()


def main():
    for oif in ff1:
        print(oif)

    # Данные для п.1 практического задания 1, где
    #      [0 - [ci, wi], 1 - [], ...]
    item_list = [[50, 9],
                 [59, 10],
                 [70, 11],
                 [71, 13],
                 [69, 15]]

    # Данные для п.5 практического задания 1, где
    #       [0 - [ci, wi, bi], 1 - [], ...]
    item_list2 = [[10, 4, 3],
                  [15, 6, 2],
                  [13, 7, 2],
                  [24, 9, 3]]

    y1 = 25  # начало интервала задачи №1
    y2 = 50  # конец интервала задачи №1

    y1_ = 27  # начало интервала задачи №2
    y2_ = 54  # конец интервала задачи №2

    f = []
    f_ = []

    f1 = []
    f2 = []

    f1_ = []
    f2_ = []

    # print('Задача 1')
    matrix1 = []
    for i in range(y2 - y1 + 1):
        f.append(neogran_zadacha(y1 + i, item_list)[y1 + i][0])
        matrix1.append(neogran_zadacha(y1 + i, item_list))
    a = np.array(matrix1)

    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = a[i][j][0]

    matrix2 = []
    for i in range(len(item_list)):
        item_list[i][1] = item_list[i][1] - 1
    for i in range(y2 - y1 + 1):
        f1.append(neogran_zadacha(y1 + i, item_list)[y1 + i][0])
        matrix2.append(neogran_zadacha(y1 + i, item_list))
    a = np.array(matrix2)
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = a[i][j][0]

    matrix3 = []
    for i in range(len(item_list)):
        item_list[i][1] = item_list[i][1] - 1
    for i in range(y2 - y1 + 1):
        f2.append(neogran_zadacha(y1 + i, item_list)[y1 + i][0])
        matrix3.append(neogran_zadacha(y1 + i, item_list))
    a = np.array(matrix3)
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = a[i][j][0]

    # Метод для вывода графика, где
    # желтый - исходные данные Wi, чёрный - Wi = Wi - 1, голубой - Wi = Wi+1
    input("Нажмите любую клавишу, чтобы построить график для 1 задачи")
    graph_knapsack(y1, y2, f, f1, f2)

    matrix4 = []

    input("\nНажмите любую кнопку, чтобы показать решение 2 задачи... ")

    print('\nЗадача 2')
    for i in range(y2_ - y1_ + 1):
        f_.append(ogran_zadacha(y1_ + i, item_list2)[y1_ + i][0])
        matrix4.append(ogran_zadacha(y1_ + i, item_list2))
    a = np.array(matrix4)
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = a[i][j][0]

    matrix5 = []
    for i in range(len(item_list2)):
        item_list2[i][2] = item_list2[i][2] - 1
    for i in range(y2_ - y1_ + 1):
        f1_.append(ogran_zadacha(y1_ + i, item_list2)[y1_ + i][0])
        matrix5.append(ogran_zadacha(y1_ + i, item_list2))
    a = np.array(matrix5)
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = a[i][j][0]
    for i in ff2:
        print(i)

    matrix6 = []
    for i in range(len(item_list2)):
        item_list2[i][2] = item_list2[i][2] + 2
    for i in range(y2_ - y1_ + 1):
        f2_.append(ogran_zadacha(y1_ + i, item_list2)[y1_ + i][0])
        matrix6.append(ogran_zadacha(y1_ + i, item_list2))
    a = np.array(matrix6)
    for i in range(len(a)):
        for j in range(len(a[i])):
            a[i][j] = a[i][j][0]

    input("Нажмите любую клавишу, чтобы построить график для 2 задачи")
    graph_knapsack(y1_, y2_, f_, f1_, f2_)


if __name__ == '__main__':
    main()
