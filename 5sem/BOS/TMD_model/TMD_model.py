"""
ТИПЫ субъектов: root, user, guest
только root может создавать субъектов
Типы объектов: "1 - 10"
root может читать/писать любые, user только меньше "7", guest меньше "3"
Соответсвенно, создавать объекты субъекты могут по тем же принципам
Если у субъекта тип совпал с типом объекта, то у субъекта есть привилегии на объект
root или владелец может менять эти привилегии по желанию
При создании объекта указывается его тип и список родительских типов
На основе полного списка наследования всех типов строится граф порождения типов
Список наследования - словарь, где ключи - названия типов, значения - списки родительских типов
json файл с пользователями, содержащий в качестве ключа - имя субъекта, а значения - словарь, где ключ - имя объекта,
значение - права доступа у этого субъекта на этот объект
По идее  - если у субъекта есть право на чтение/ запись и его тип удовлетворяет типу объекта, то субъект может использовать свои привилегии бесперпятственно
Важно, чтобы именно оба эти параметра были соблюдены.
"""

import csv
import json
import os
import sys

import matplotlib.pyplot as plt
import networkx as nx


def help_about():
    print("""

ТИПЫ субъектов: root, user, guest
только root может создавать субъектов
Типы объектов: "1 - 10"
root может читать/писать любые, user только меньше "7", guest меньше "3"
Соответсвенно, создавать объекты субъекты могут по тем же принципам
Если у субъекта "тип" совпал с типом объекта, то у субъекта есть привилегии на объект
root или владелец может менять эти привилегии по желанию
При создании объекта указывается его тип и список родительских типов
На основе полного списка наследования всех типов строится граф порождения типов
Список наследования - словарь, где ключи - названия типов, значения - списки родительских типов
json файл с пользователями, содержащий в качестве ключа - имя субъекта, а значения - словарь, где ключ - имя объекта,
значение - права доступа у этого субъекта на этот объект.
    
    """)


def help():
    print("command's : \n"
          "remove_file - удалить файл\n"
          "read_file - прочитать файл\n"
          "write_file - вписать в файл\n"
          "clear_file - удалить содержимое файла\n"
          "logout_user - логаут\n"
          "whose_object - узнать чей объект\n"
          "create_object - создать объект\n"
          "create_user - создать субъекта\n"
          "create_graph - строит граф наследования типов\n"
          "login_user - зайти в систему под другим пользователем\n"
          "print_lists - вывести список существующих пользователей системы\n"
          "help_about - информация о программе\n"
          "")


users_dict: dict = {}  # Словарь субъектов


def save_json():
    with open("users.json", "w") as json_file:
        json.dump(users_dict, json_file, indent=2)


def remove_file(filename: str, user: str):
    if user == "root":
        try:
            os.remove(filename)
        except IOError:
            print("Файл отсутствует!")
    else:
        if filename in users_dict[user]['objects'] and users_dict[user]['objects'][filename] == [1, 1, 1]:
            try:
                os.remove(filename)
            except IOError:
                print("Файл отсутствует!")
        else:
            print("Чтобы сделать это нужно авторизоваться!")
            executor()


def transfer_rights(filename: str, user_source: str, user_target: str, read: int, write: int, execute: int):
    if user_source == "root":
        users_dict[user_target]['objects'][filename] = [read, write, execute]
        save_json()
    else:
        if filename in users_dict[user_source]['objects'] and users_dict[user_source]['objects'][filename] == [1, 1, 1]:
            users_dict[user_target]['objects'][filename] = [read, write, execute]
        else:
            print("Чтобы сделать это нужно авторизоваться!")
            executor()


def clear_file(filename: str, user: str):  # ready
    if user == "root":
        try:
            with open(filename, "w") as c_f:
                pass
        except IOError:
            print("IO Error!")
    else:
        if filename in users_dict[user]['objects'] and users_dict[user]['objects'][filename] == [1, 1, 1]:
            try:
                with open(filename, "w") as c_f:
                    pass
            except IOError:
                print("IO Error!")
        else:
            print("Чтобы сделать это нужно авторизоваться!")
            executor()


def write_file(filename: str, message: str, user: str):
    if user == "root":
        try:
            handle = open(filename, 'a')
            handle.writelines(message)
        except IOError:
            print("IO Error!")
        finally:
            handle.close()
    else:
        if filename in users_dict[user]['objects'] and users_dict[user]['objects'][filename][1] == 1:
            try:
                handle = open(filename, 'a')
                handle.writelines(message)
            except IOError:
                print("IO Error!")
            finally:
                handle.close()

        else:
            print("Чтобы сделать это нужно авторизоваться!")
            executor()


def save_types_objects():
    with open("types_objects.json", "w") as json_file:
        json.dump(exstends_type_dict, json_file, indent=2)


def get_json_types_objects():
    global exstends_type_dict
    try:
        with open('types_objects.json', 'r') as json_file:
            exstends_type_dict = json.load(json_file)
    except:
        print("ОШИБКА! Файл пуст")


def read_file(filename: str, user: str):
    if user == "root":
        try:
            handle = open(filename, "r")
            print(handle.read())
        except IOError:
            print("Файл не найден!")
        finally:
            handle.close()
    else:
        if filename in users_dict[user]['objects'] and users_dict[user]['objects'][filename][0] == 1:
            try:
                handle = open(filename, "r")
                print(handle.read())
            except IOError:
                print("Файл не найден!")
            finally:
                handle.close()
        else:
            print("Чтобы сделать это нужно авторизоваться!")
            executor()


def logout_user():
    sys.exit()


def create_graph():
    graph = nx.Graph()
    for i in exstends_type_dict:
        graph.add_node(i)
    for i in exstends_type_dict:
        for j in exstends_type_dict[i]:
            graph.add_edge(i, j)

    options = {
        'node_color': 'blue',
        'node_size': 500,
        'arrowstyle': '-|>',
        'arrowsize': 12,
    }
    nx.draw_networkx(graph, arrows=True, **options)
    plt.show()


def create_object(filename: str, user: str, object_type: str):
    if user == "root":
        handle = open(filename, "w")
        handle.write("")
        handle.close()
        users_dict[user]['objects'] = {filename: [1, 1, 1]}
        save_json()
        return 1
    else:
        if users_dict[user]['user_type'] == "user" and int(object_type) >= 7:
            print("Чтобы сделать это нужно авторизоваться!")
            executor()
            return 0
        elif users_dict[user]['user_type'] == 'guest' and int(object_type) >= 3:
            print("Чтобы сделать это нужно авторизоваться!")
            executor()
            return 0
        elif users_dict[user]['user_type'] == 'root':
            handle = open(filename, "w")
            handle.write("")
            handle.close()
            users_dict[user]['objects'][filename] = [1, 1, 1]
            save_json()
            return 1
        else:
            handle = open(filename, "w")
            handle.write("")
            handle.close()
            users_dict[user]['objects'][filename] = [1, 1, 1]
            save_json()
            return 1


login_list = []
password_list = []
login_password_list = []
login_list.append("root")
password_list.append("1234")

with open("login_password.csv", 'r') as r_file:
    file_reader = csv.reader(r_file, delimiter=",")
    for row in file_reader:
        login_password_list.append(row)

for i in range(len(login_password_list)):
    login_list.append(login_password_list[i][0])
    password_list.append(login_password_list[i][1])

login = ""
password = ""

check = True


def print_lists():
    global login_list, password_list
    print(login_list)
    print(password_list)


def login_user():
    global login, password
    login = str(input("Напишите логин: "))
    password = str(input("Напишите пароль: "))
    if login not in login_list and password not in password_list:
        print("Логин или пароль неверны!")
        login_user()


login_user()

while check:
    if login not in login_list or password not in password_list:
        print("Логин или пароль неверны!")
        login_user()
    else:
        check = False
        break


def whose_object(filename: str):
    for i in users_dict:
        for j in users_dict[i]['objects']:
            if filename == j:
                print(f"Этот объект принадлежит ему - {i}")
                break


def create_user():
    global login_list, password_list, login, password
    if login == "root" and password == "1234":
        login_new_user = str(input("Логин нового пользователя: "))
        password_new_user = str(input("Пароль нового пользователя: "))
        user_type = str(input("Напишите тип нового пользователя: "))
        if login_new_user not in login_list:
            tmp = [login_new_user, password_new_user]
            with open("login_password.csv", 'a', newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(tmp)
            users_dict[login_new_user] = {"user_type": user_type,
                                          "objects": {}}
            # создание нового субъекта,
            # т.е. добавление соответствующего ключа в словарь субъектов
            save_json()
        else:
            print("Такой пользователь уже существует")
    else:
        print("Чтобы сделать это нужно авторизоваться !!!")
        executor()


if login == "exit":
    sys.exit()

exstends_type_dict: dict = {  # список наследования типов
}


def command_executor(command: str):
    if command == "create_object":
        question = int(input("Хотите сбросить конфигурацию наследования? (1)yes (2)no -> "))
        if question == 1:
            exstends_type_dict.clear()
        if question == 2:
            get_json_types_objects()
        name_object = str(input("Напишите имя объекта, используя расширение '.txt' : "))
        type_object = str(input("Напишите тип этого объекта: "))
        temp_question = int(input("Как много родительских типов? -> "))
        temp_list = []
        print("Напиши здеся: ")
        for i in range(temp_question):
            temp_list.append("type_" + input(f"{i}'th parents type: "))
        tmp = create_object(name_object, login, type_object)
        if tmp == 1:
            try:
                exstends_type_dict["type_" + type_object] = temp_list
            except:
                print("this key is already exists")
        save_types_objects()
    if command == "create_user":
        create_user()
    if command == "help_about":
        help_about()
    if command == "login_user":
        login_user()
    if command == "logout_user":
        logout_user()
    if command == "create_graph":
        create_graph()
    if command == "whose_object":
        filename = input("write filename: ")
        whose_object(filename)
    # if command == "transfer_rights":
    #     filename = input("Напишите название файла: ")
    #     user_source = login
    #     user_target = input("write user target: ")
    #     read = int(input("write read: "))
    #     write = int(input("write write: "))
    #     execute = int(input("write execute: "))
    #     transfer_rights(filename, user_source, user_target, read, write, execute)
    if command == "remove_file":
        filename = str(input("Напишите название файла: "))
        remove_file(filename, login)
    if command == "write_file":
        filename = str(input("Напишите название файла: "))
        message = str(input("Напиишите сообщение: "))
        write_file(filename, message, login)
    if command == "read_file":
        filename = str(input("Напишите название файла: "))
        read_file(filename, login)
    if command == "print_lists":
        print_lists()
    if command == "clear_file":
        filename = str(input("Напишите название файла: "))
        clear_file(filename, login)
    if command == "help":
        help()


flag = True


def get_data_from_json():
    global users_dict
    try:
        with open('users.json', 'r') as json_file:
            users_dict = json.load(json_file)
    except:
        print("ОШИБКА! Файл пуст")


def executor():
    global flag
    get_data_from_json()
    while flag:
        print(f"-----Логин: {login} ---------")
        temp_question = int(input("Закрыть программу? (1)ДА (2)Неть: "))
        if temp_question == 2:
            command = str(input("Введите комманду: "))
            command_executor(command)
        if temp_question == 1:
            flag = False
            break
        if temp_question != 2 and temp_question != 1:
            print("Неверные данные!")
            break


get_json_types_objects()
executor()
