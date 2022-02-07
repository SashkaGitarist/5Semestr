# Функция для кодирования строки в зашифрованный вид
import random

from numpy import sort


def encode(array):
    chip_arr = []
    ind = 0
    for i in range(len(array)):
        chip_arr.append(ind)
        ind += 1

    # print(chip_arr)
    sort_chip_arr = sorted(chip_arr, key=lambda x: random.random())

    print("Список со случ. генерацией позиций - ", sort_chip_arr)

    res_chi_arr = []
    for j in sort_chip_arr:
        res_chi_arr.append(array[j])
    # print("Расшифровка по буквам - ", res_chi_arr)
    print("Зашифрованная строка: "+''.join(res_chi_arr))

    dechi_arr = []
    for k in sort_chip_arr:
        # print(k)
        # print(array[k])
        dechi_arr.append(k)

    # print(dechi_arr)

    res_dechi_arr = sorted(dechi_arr)

    # print(res_dechi_arr)

    fin_res_dechi_arr = [0]*len(res_dechi_arr)

    for tt in range(len(res_dechi_arr)):
        fin_res_dechi_arr[tt] = array[tt]

    print("Расшифрованная строка: "+''.join(fin_res_dechi_arr))
# main code


arr_of_word = []  # массив для считывания ФИО
word = "Шелудянкин Александр Константинович"# str(input("Введите своё ФИО: "))
for i in word:
    arr_of_word.append(i)

encode(arr_of_word)
