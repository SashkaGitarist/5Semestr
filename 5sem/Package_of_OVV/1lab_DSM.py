import csv
# допускает цепочки, которые начинаются на "10"
import sys

with open("DSM_word", encoding="utf-8") as r_file:
    file_reader = csv.reader(r_file)
    word_temp = []
    for row in file_reader:
        word_temp.append(row)

word = ""  # слово
for i in range(len(word_temp[0])):
    word += word_temp[0][i]
for i in word:  # проверка на принадлежность слова к допустимому алфавиту автомата
    if i != '1' and i != '0':
        print(f"Слово: {word}")
        print("Алфавит данного слова не удовлетворяет этому атвомату")
        sys.exit()

word_rand = ""


state = 0  # состояние автомата
print(f"Слово: {word}")
for i in word:
    if state == 0:
        if i == '0':  # если в начале ноль - выход
            state = 0
            break
        if i == '1':  # если в начале единица - идем дальше
            state = 1
            continue
    if state == 1:
        if i == '0':  # если после единицы втречается ноль - выход из цикла, так как условие соблюдено.
            state = 1
            break
        if i == '1':  # если единица - выход
            state = 0
            break

if state == 1:  # если автомат оказался в допускающем состоянии, то слово - допустимое
    print("Вывод: Слово является допустимым")
elif state == 0:
    print("Вывод: Слово не является допустимым")
