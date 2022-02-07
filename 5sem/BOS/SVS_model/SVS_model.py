"""
Система военных сообщений
Управление доступом на основе ролей.
Контейнер - словарь, где ключ - название объекта, значение_1 - метка конфиденциальности контейнера, зн_2 - список объектов
Типы объектов: public, official_use, secret, top_secret - Общедоступная, для служебного пользования, секретная, соверш. секретная информация
Типы субъектов: R, S, L, G, root
"""
import csv
import json
import os
import sys

users_dict: dict = {}  # Словарь с информацией субъектов
actions_dict: dict = {}  # Словарь действий за текущую сессию
containers_dict: dict = {}  # Словарь контейнеров


def help():
    print("Существующие команды : "
          "df - удалить файл\n"
          "rf - прочитать файл\n"
          "wf - вписать в файл\n"
          "cf - удалить содержимое файла\n"
          "rr - поменять роль у субъекта\n"  # Выполнение только от root - администратор
          "rto - поменять метку конфиденциальности объекта\n"  # Выполнение только от root
          "co - создать объект\n"
          "cu - создать субъекта\n"
          "cc - создать контейнер\n"
          "lu - зайти в систему под другим пользователем\n"
          "logout - выйти из программы\n"
          "pl - вывести список существующих пользователей системы\n"
          "")


def save_actions_file():
    with open("actions.json", "w") as json_file:
        json.dump(actions_dict, json_file, indent=2)


def save_users_file():
    with open("users.json", 'w') as json_file:
        json.dump(users_dict, json_file, indent=2)


def check_right(filename: str, user: str):  # проверка прав доступа у субъекта на объект
    flag = False
    if users_dict["users"][user] == "R" and users_dict["objects"][filename] == "public":
        flag = True
    if users_dict["users"][user] == "S" and users_dict["objects"][filename] == "official_use":
        flag = True
    if users_dict["users"][user] == "L" and users_dict["objects"][filename] == "secret":
        flag = True
    if users_dict["users"][user] == "G" and users_dict["objects"][filename] == "top_secret":
        flag = True
    return flag


def first_check_right(type_object: str, user: str):  # первая проверка прав доступа у субъекта на объект
    flag = False
    if users_dict["users"][user] == "R" and type_object == "public":
        flag = True
    if users_dict["users"][user] == "S" and type_object == "official_use":
        flag = True
    if users_dict["users"][user] == "L" and type_object == "secret":
        flag = True
    if users_dict["users"][user] == "G" and type_object == "top_secret":
        flag = True
    return flag


def remove_file(filename: str, user: str):
    if user == "root":
        try:
            os.remove(filename)
        except IOError:
            print("Файл отсутствует!")
    else:
        if check_right(filename, user) is True:
            try:
                os.remove(filename)
            except IOError:
                print("Файл отсутствует!")
            actions_dict[user]["objects"].append(f"Remove file -> {filename}")
            save_actions_file()
        else:
            print("Нет привилегий для этого! ")
            main()


def clear_file(filename: str, user: str):
    if user == "root":
        try:
            with open(filename, "w") as c_f:
                pass
        except IOError:
            print("Ошибка ввода!")
    else:
        if check_right(filename, user) is True:
            try:
                with open(filename, "w") as c_f:
                    pass
            except IOError:
                print("Ошибка ввода!")
            actions_dict[user]["objects"].append(f"Clean file -> {filename}")
            save_actions_file()
        else:
            print("Нет привилегий для этого!")
            main()


def write_file(filename: str, message: str, user: str):
    if user == "root":
        try:
            handle = open(filename, 'a')
            handle.writelines(message)
        except IOError:
            print("Ошибка ввода!")
        finally:
            handle.close()
    else:
        if check_right(filename, user) is True:
            try:
                handle = open(filename, 'a')
                handle.writelines(message)
            except IOError:
                print("Ошибка ввода!")
            finally:
                handle.close()
            actions_dict[user]["objects"].append(f"Write file {filename}: ")
            save_actions_file()
        else:
            print("Неть привилегий :(")
            main()


def refactor_role(user_1: str, user_2: str):
    if user_1 == "root":
        new_role = input("Напишите новую роль для этого субъекта: ")
        users_dict["users"][user_2] = new_role
        save_users_file()
    else:
        print("Нет привилегий для этого действия!")
        main()


def refactor_type_object(filename: str, user: str):
    if user == "root":
        new_type_object = input("Напишите новый тип объекту: ")
        users_dict["objects"][filename] = new_type_object
        save_users_file()

    else:
        print("нет привилегий для этого!")
        main()


def create_container(user: str):
    global containers_dict
    container: list = []
    name_container = input("Напишите имя контейнера: ")
    containers_dict[name_container] = {}
    count_objects = int(input("Напишите кол-во объектов в контейнере: "))
    for i in range(count_objects):
        temp_name_object = input(f"Напишите объект №{str(i + 1)}:")
        container.append(temp_name_object)
        containers_dict[name_container]["objects"] = container

    dict_values: dict = {
        "public": 0,
        "official_use": 1,
        "secret": 2,
        "top_secret": 3
    }

    dict_keys: dict = {
        0: "public",
        1: "official_use",
        2: "secret",
        3: "top_secret"
    }
    temp_list = []
    temp_list_2 = []
    for i in container:
        temp_list.append(users_dict["objects"][i])
    for i in temp_list:
        temp_list_2.append(dict_values[i])
    type_container = max(temp_list_2)
    containers_dict[name_container]["type"] = dict_keys[type_container]
    print(f"Был создан контейнер {name_container} с типом {containers_dict[name_container]['type']}")
    actions_dict[user]["containers"].append(f"Create conteiner {name_container} with type {containers_dict[name_container]['type']}")
    save_actions_file()


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
        temp = check_right(filename, user)
        if temp is True:
            try:
                handle = open(filename, "r")
                print(handle.read())
            except IOError:
                print("Файл не найден!")
            finally:
                handle.close()
            actions_dict[user]["objects"].append(f"Read file {filename}")
            save_actions_file()
        else:
            print("Нет привилегий!")
            main()


def logout_user():
    sys.exit()


def create_object(filename: str, user: str):
    type_object = input("Напишите тип объекта: ")
    temp = first_check_right(type_object, user)
    if temp is True:
        handle = open(filename, "w")
        handle.write("")
        handle.close()
        users_dict['objects'][filename] = type_object
        actions_dict[user]["objects"].append(f"Create object {filename} with type {type_object}")
        save_users_file()
        save_actions_file()
    else:
        print("Нет привилегий для этого!")
        main()


def get_data_from_users_json():
    global users_dict
    try:
        with open('users.json', 'r') as json_file:
            users_dict = json.load(json_file)
    except:
        print("Файл пуст :(")


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
    actions_dict[login] = {"commands": [],
                           "objects": [],
                           "containers": []
                           }
    if login not in login_list and password not in password_list:
        print("Логин и/или пароль не такие какие у нас есть!")
        login_user()


login_user()

while check:
    if login not in login_list or password not in password_list:
        print("Логин и/или пароль не такие верные")
        login_user()
    else:
        check = False
        break
actions_dict[login] = {"commands": [],
                       "objects": [],
                       "containers": []
                       }


def create_user():  # создавать субъектов может только root
    global login_list, password_list, login, password
    if login == "root" and password == "1234":
        login_new_user = str(input("Логин нового пользователя: "))
        password_new_user = str(input("Пароль нового пользователя: "))
        if login_new_user not in login_list:
            tmp = [login_new_user, password_new_user]
            with open("login_password.csv", 'a', newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(tmp)
            type_user = input("Напишите тип пользователя: ")
            users_dict["users"][login_new_user] = type_user
            actions_dict[login_new_user] = {"commands": [], "objects": [], "containers": []}
            save_users_file()
            save_actions_file()
        else:
            print("Такой пользователь уже есть!")
    else:
        print("Нет привилегий :(")
        main()


def command_executor(command: str):
    match command:
        case "co":
            name_object = str(input("Напишите имя объекта, используя расширение .txt : "))
            create_object(name_object, login)
        case "cu":
            create_user()
        case "cc":
            create_container(login)
        case "rr":
            temp_user = input("Напишите пользователя: ")
            refactor_role(login, temp_user)
        case "rto":
            filename = input("Напишите имя пользователя: ")
            refactor_type_object(filename, login)
        case "lu":
            login_user()
        case "logout":
            logout_user()
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


flag = True


def main():
    global flag
    get_data_from_users_json()
    while flag:
        print(f"--(0_0)-- {login} --(0_0)--")
        temp_question = int(input("Выйти? Да - 1 / Нет - 2: "))
        match temp_question:
            case 1:
                flag = False
                break

            case 2:
                command = str(input("Напишите команду: "))
                actions_dict[login]["commands"].append(f"Write command {command}")
                save_actions_file()
                command_executor(command)

            case _:
                print("Не те данные!")
                break


if __name__ == '__main__':
    main()
