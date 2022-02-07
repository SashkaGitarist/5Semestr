"""
Модель Белла - Лаппадулы - каноничный пример модели с мандатным разграничением доступа.
Есть метка конфиденциальности у объектов и субъектов.
У объектов - 1, 2, 3. Что соответсвует "С", "СС", "ОВ"
У субъектов - 1, 2, 3. Что соответсвует "guest", "user", "root"
Реализована политика "no write down" и "no read up".
"""

import csv
import json
import os
import sys

users_dict: dict = {}  # Словарь с информацией субъектов


def help():
    print("команды : "
          "cr - посмотреть права пользователя на файл\n"
          "df - удалить файл\n"
          "rf - прочитать файл\n"
          "wf - вписать в файл\n"
          "cf - удалить содержимое файла\n"
          "logout - логаут\n"
          "rto - поменять метку конфиденциальности у объекта\n"
          "co - создать объект\n"
          "cu - создать субъекта\n"
          "lu - зайти в систему под другим пользователем\n"
          "print - вывести список существующих пользователей системы\n"
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
        print("Нет привилегий для этого!")
        main()


def clear_file(filename: str, user: str):
    if users_dict["users"][user] >= users_dict["objects"][filename]:  # Если у субъекта мандат больше или
        # равен мандату объекта, то он может его очистить от содержимого
        try:
            with open(filename, "w") as c_f:
                pass
        except IOError:
            print("IO Error!")
    else:
        print("Нет привилегий для этого")
        main()


def write_file(filename: str, message: str, user: str):
    if users_dict["users"][user] <= users_dict["objects"][filename]:  # Если у субъекта мандат ниже или равен
        # мандату объекта, то он может в него писать, иначе - нет, т.е NWD - no write down
        try:
            handle = open(filename, 'a')
            handle.writelines(message)
        except IOError:
            print("Ошибка ввода/вывода")
        finally:
            handle.close()
    else:
        print("Нет привилегий для этого! (NWD)")
        main()


def refactor_type_object(filename: str, user: str):  # Если у субъекта мандат выше чем у объекта, то он не может
    # записать в него ничего, поэтому ему надо поднимать мандат у объекта
    if users_dict["users"][user] > users_dict["objects"][filename]:
        new_type_this_object = int(input("Новый тип объекта: "))
        users_dict["objects"][filename] = new_type_this_object
        save_users_file()
    else:
        print("Нет привилегий для этого!")
        main()


def read_file(filename: str, user: str):
    if users_dict["users"][user] >= users_dict["objects"][filename]:  # Если мандат субъекта больше или равен
        # мандату объекта, то он может его читать, а если нет, то нет) т.е NRU - no read up
        try:
            handle = open(filename, "r")
            print(handle.read())
        except IOError:
            print("Файл не найден!")
        finally:
            handle.close()
    else:
        print("Нет привилегий для этого! (NRU)")
        main()


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
        print("Файлик пуст")


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
        print("Логин и/или пароль неверны")
        login_user()


login_user()

while check:
    if login not in login_list or password not in password_list:
        print("Логин и/или пароль неверны")
        login_user()
    else:
        check = False
        break


def create_user():
    global login_list, password_list, login, password
    if login == "root" and password == "1234":
        login_new_user = str(input("Логин нового пользователя: "))
        password_new_user = str(input("Пароль нового пользователя: "))
        if login_new_user not in login_list:
            tmp = [login_new_user, password_new_user]
            with open("login_password.csv", 'a', newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(tmp)
            type_user = int(input("Напишите тип пользователя: "))
            users_dict["users"][login_new_user] = type_user
            save_users_file()
        else:
            print("Такой пользователь уже есть")
    else:
        print("Нет привилегий для ентого действия")
        main()


if login == "exit":
    sys.exit()


def command_executor(command: str):
    match command:
        case "co":
            name_object = str(input("Напишите имя файла, используя расширение .txt ): "))
            type_object = int(input("Напишите тип объекта: "))
            create_object(name_object, type_object)
        case "cu":
            create_user()
        case "lu":
            login_user()
        case "logout":
            logout_user()
        case "rto":
            filename = input("Название файла:")
            refactor_type_object(filename, login)
        case "df":
            filename = str(input("Название файла: "))
            remove_file(filename, login)
        case "wf":
            filename = str(input("Название файла: "))
            message = str(input("Сообщение: "))
            write_file(filename, message, login)
        case "rf":
            filename = str(input("Название файла: "))
            read_file(filename, login)
        case "print":
            print_lists()
        case "cf":
            filename = str(input("Название файла: "))
            clear_file(filename, login)
        case "help":
            help()


def main():
    get_data_from_users_json()
    while True:
        print(f"--(0_0)-- {login} --(0_0)--")
        temp_question = int(input("Выйти? да-1 нет-2: "))
        match temp_question:
            case 1:
                break
            case 2:
                command = str(input("Напишите команду: "))
                command_executor(command)

            case _:
                print("Неверный данные")
                break


if __name__ == __name__:
    main()

