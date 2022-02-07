# когда нибудь тут будет 9 лаба по па
import csv


# Функция для записи данных
def csv_dict_reader(name):
    file = open(name, 'r')
    lines = file.readlines()
    arr = [list(map(str, lines[i].replace('\n', '').split(';'))) for i in range(len(lines))]
    file.close()
    initial_state = arr[0][0]
    final_states = [arr[0][1]]
    string = []
    for i in arr[0][2:]:
        if i != '':
            string.append(i + ' ')
    transition_function = {}
    for i in arr[1:]:
        for j in range(len(i)):
            if i[j] == '':
                i[j] = ' '
        transition_function[(i[0], i[1])] = (i[2], i[3], i[4])
    return initial_state, final_states, string, transition_function, arr


# Функция для записи данных в CSV
def file_print(arr, file):
    outfile = open('{}.csv'.format(file), 'w', newline='')
    writer = csv.writer(outfile, delimiter=';', quotechar='"')
    for i in arr:
        writer.writerow(i)
    outfile.close()


def TuringMachine(tape, current_state, transition_function, head_position):
    char_under_head = tape[head_position]
    x = (current_state, char_under_head)
    if x in transition_function:
        y = transition_function[x]
        tape = list(tape)
        tape[head_position] = y[1]
        if y[2] == "R":
            head_position += 1
        elif y[2] == "L":
            head_position -= 1
        current_state = y[0]
    return current_state, tape, head_position


def final(current_state, final_states):
    if current_state in final_states:
        return True
    else:
        return False


print('---Первая Машина: инвертирует символы---')
initial_state, final_states, string, transition_function, arr = csv_dict_reader('lb91.csv')
s = []
for i in string:
    current_state = initial_state
    head_position = 0
    if i == " ":
        print('Начальная лента пуста!')
    else:
        print("Начальная лента:\n" + i)
        while not final(current_state, final_states):
            current_state, i, head_position = TuringMachine(i, current_state, transition_function, head_position)
        print("Результат работы машины:")
        s.append(i)
        print("".join(i))
        print()
for i in range(len(s)):
    arr[0][i + 2] = "".join(s[i])[:len(s[i]) - 1]
print('Производим запись в файл...')
print('Результат хранится в файле lb93.csv')
file = 'lb93'
file_print(arr, file)
print()

print('---Вторая Машина: прибавляет единицу к каждому символу в двоичном представлении---')
initial_state, final_states, string, transition_function, arr = csv_dict_reader('lb92.csv')
s = []
for i in string:
    current_state = initial_state
    head_position = 0
    if i == " ":
        print('Начальная лента пуста!')
    else:
        print("Начальная лента:\n" + i)
        while not final(current_state, final_states):
            current_state, i, head_position = TuringMachine(i, current_state, transition_function, head_position)
        print("Результат работы машины:")
        s.append(i)
        print("".join(i))
        print()
for i in range(len(s)):
    arr[0][i + 2] = "".join(s[i])[:len(s[i]) - 1]
print('Производим запись в файл...')
print('Результат хранится в файле lb94.csv')
file = 'lb94'
file_print(arr, file)
