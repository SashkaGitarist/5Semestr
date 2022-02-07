"""
Модель Биба.
Основные принципы: no read down, no write up
В данной модели мандат рассматривается как некая целостность субъекта или оъекта.
Или как достоверность.
Т.е. Субъект с низкой достоверностью не может писать в более достоверный объект.
Также Субъект с высокой достоверностью не может читать менее достоверный объект.
"""

import csv
import json
import os
import sys

users_dict: dict = {}  # Словарь с информацией субъектов


def help():
    print("Существующие команды : "
          "df - удалить файл\n"
          "rf - прочитать файл\n"
          "wf - вписать в файл\n"
          "cf - удалить содержимое файла\n"
          "rto - поменять метку конфиденциальности у объекта\n"
          "rts - поменять метку конфиденциальности у субъекта\n"
          "co - создать объект\n"
          "cu - создать субъекта\n"
          "lu - зайти в систему под другим пользователем\n"
          "logout - логаут\n"
          "pl - вывести список существующих пользователей системы\n"
          "")


def save_users_file():
    with open("users.json", 'w') as json_file:
        json.dump(users_dict, json_file, indent=2)


def remove_file(filename: str, user: str):
    if users_dict["users"][user] >= users_dict["objects"][filename]:  # Если у субъекта мандат больше или
        # равен мандату объекта, то он может его удалить
        try:
            os.remove(filename)
        except IOError:
            print("Файл отсутствует!")
    else:
        print("У вас нет таких полномочий!")
        executor()


def clear_file(filename: str, user: str):
    if users_dict["users"][user] >= users_dict["objects"][filename]:  # Если у субъекта мандат больше или
        # равен мандату объекта, то он может его очистить от содержимого
        try:
            with open(filename, "w") as c_f:
                pass
        except IOError:
            print("IO Error!")
    else:
        print("У вас нет таких полномочий!")
        executor()


def write_file(filename: str, message: str, user: str):
    if users_dict["users"][user] >= users_dict["objects"][filename]:  # Если у субъекта мандат больше или равен
        # мандату объекта, то он может в него писать, иначе - нет, т.е NWU - no write up
        try:
            handle = open(filename, 'a')
            handle.writelines(message)
        except IOError:
            print("IO Error!")
        finally:
            handle.close()
    else:
        print("Вы не можете этого совершить по причине - NWU!")
        executor()


def refactor_type_object(filename: str, user: str):  # Если требуется поменять мандат у объекта, то это может сделать
    # только root
    if user == "root":
        new_type_this_object = int(input("Напишите новый тип объекта: "))
        users_dict["objects"][filename] = new_type_this_object
        save_users_file()
    else:
        print("У вас нет таких полномочий!")
        executor()


def refactor_type_subject(changing_user: str, user: str):  # Если требуется поменять мандат у субъекта, то это может
    # сделать только root
    if user == "root":
        new_type_user = int(input("Напишите новый тип пользователя: "))
        users_dict["users"][changing_user] = new_type_user
        save_users_file()
    else:
        print("У вас нет таких полномочий!")
        executor()


def read_file(filename: str, user: str):
    if users_dict["users"][user] <= users_dict["objects"][filename]:  # Если мандат субъекта меньше или равен
        # мандату объекта, то он может его читать, а если нет, то нет) т.е NRD - no read down
        try:
            handle = open(filename, "r")
            print(handle.read())
        except IOError:
            print("Файл отсутствует! Найдите его, а потом вызывайте!")
        finally:
            handle.close()
    else:
        print("Вы не можете это совершить по причине - NRD")
        executor()


def logout_user():
    sys.exit()


def create_object(filename: str, type_object: int):
    handle = open(filename, "w")
    handle.write("")
    handle.close()
    users_dict["objects"][filename] = type_object
    save_users_file()


def get_data_from_users_json():
    global users_dict
    try:
        with open('users.json', 'r') as json_file:
            users_dict = json.load(json_file)
    except:
        print("Файл пуст")


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
        print("Логин и/или пароль неверные!")
        login_user()


login_user()

while check:
    if login not in login_list or password not in password_list:
        print("Логин и/или пароль неверные!")
        login_user()
    else:
        check = False
        break


def create_user():
    global login_list, password_list, login, password
    if login == "root" and password == "1234":
        login_new_user = str(input("Логин нового пользователя: "))
        password_new_user = str(input("пароль нового пользователя: "))
        if login_new_user not in login_list:
            tmp = [login_new_user, password_new_user]
            with open("login_password.csv", 'a', newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(tmp)
            type_user = int(input("напишите тип пользователя: "))
            users_dict["users"][login_new_user] = type_user
            save_users_file()
        else:
            print("такой пользователь уже есть!")
    else:
        print("У вас нет привелегий, чтобы сделать это!")
        executor()


if login == "exit":
    sys.exit()


def command_executor(command: str):
    match command:
        case "co":
            name_object = str(input("Напишите имя объекта, используя расширение .txt: "))
            type_object = int(input("Напишите тип объекта: "))
            create_object(name_object, type_object)

        case "cu":
            create_user()

        case "lu":
            login_user()

        case "logout":
            logout_user()

        case "rto":
            filename = input("Напишите имя файла:")
            refactor_type_object(filename, login)

        case "rts":
            changing_user = input("Напишите пользователя: ")
            refactor_type_subject(changing_user, login)

        case "df":
            filename = str(input("Напишите имя файла: "))
            remove_file(filename, login)

        case "wf":
            filename = str(input("Напишите имя файла: "))
            message = str(input("Напишите сообщение: "))
            write_file(filename, message, login)

        case "rf":
            filename = str(input("Напишите имя файла: "))
            read_file(filename, login)

        case "pl":
            print_lists()

        case "cf":
            filename = str(input("Напишите имя файла: "))
            clear_file(filename, login)

        case "help":
            help()


def executor():
    get_data_from_users_json()
    while True:
        print(f"--(0_0)-- {login} --(0_0)--")
        temp_question = int(input("Выйти? Да - 1 / Нет - 2: "))
        match temp_question:
            case 1:
                break
            case 2:
                command = str(input("Напишите команду: "))
                command_executor(command)

            case _:
                print("Введите нужную цифру!")
                break


executor()
