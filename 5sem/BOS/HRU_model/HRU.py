import csv
import os
import sys


def help():
    print("command's : \n"
          "check_rights - посмотреть права пользователя на файл\n"
          "remove_file - удалить файл\n"
          "read_file - прочитать файл\n"
          "write_file - вписать в файл\n"
          "clear_file - удалить содержимое файла\n"
          "logout_user - логаут\n"
          "transfer_rights - наделить правами другого пользователя\n"
          "create_object - создать объект\n"
          "create_user - создать субъекта\n"
          "login_user - зайти в систему под другим пользователем\n"
          "print_lists - вывести список существующих пользователей системы\n"
          "")


def check_rights(user: str, filename: str):
    with open(user + '.csv', mode='r', encoding='utf-8') as r_file:
        filereader = csv.reader(r_file, delimiter=",")
        temp = []
        for row in filereader:
            temp.append(row)
    normal = False
    for i in range(len(temp)):
        if temp[i][0] == filename:
            normal = True
            print("user: ", user, " file: ", temp[i][0], " r: ", temp[i][1], " w: ", temp[i][2], " e: ", temp[i][3])
    if not normal:
        print("No result!")
        executor()


def remove_file(filename: str, user: str):
    if user == "root":
        try:
            os.remove(filename)
        except IOError:
            print("Файл отсутствует!")
    else:
        with open(user + ".csv", mode="r") as r_file:
            filereader = csv.reader(r_file, delimiter=",")
            temp = []
            for row in filereader:
                temp.append(row)
        normal = False
        for i in range(len(temp)):
            if temp[i][0] == filename:
                if temp[i][1] == "1" and temp[i][2] == "1" and temp[i][3] == "1":  # Если пользователь является
                    # владельцем, то можно удалять файл
                    normal = True
                    try:
                        os.remove(filename)
                    except IOError:
                        print("Файл отсутствует!")
        if normal == False:
            print("You are not authorized to do this.")
            executor()


def clear_file(filename: str, user: str):
    if user == "root":
        try:
            with open(filename, "w") as c_f:
                pass
        except IOError:
            print("IO Error!")
    else:
        with open(user + ".csv", mode="r") as r_file:
            filereader = csv.reader(r_file, delimiter=",")
            temp = []
            for row in filereader:
                temp.append(row)
        normal = False
        for i in range(len(temp)):
            if temp[i][0] == filename:
                if temp[i][2] == "1":
                    normal = True
                    try:
                        with open(filename, "w") as c_f:
                            pass
                    except IOError:
                        print("IO Error!")
        if not normal:
            print("You are not authorized to do this.")
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
        with open(user + ".csv", mode="r") as r_file:
            filereader = csv.reader(r_file, delimiter=",")
            temp = []
            for row in filereader:
                temp.append(row)
        normal = False
        for i in range(len(temp)):
            if temp[i][0] == filename:
                if temp[i][2] == "1":
                    normal = True
                    try:
                        handle = open(filename, 'a')
                        handle.writelines(message)
                    except IOError:
                        print("IO Error!")
                    finally:
                        handle.close()
        if not normal:
            print("You are not authorized to do this.")
            executor()


def read_file(filename: str, user: str):
    if user == "root":
        try:
            handle = open(filename, "r")
            print(handle.read())
        except IOError:
            print("File is not found!")
        finally:
            handle.close()
    else:
        with open(user + ".csv", mode="r") as r_file:
            filereader = csv.reader(r_file, delimiter=",")
            temp = []
            for row in filereader:
                temp.append(row)
        normal = False
        for i in range(len(temp)):
            if temp[i][0] == filename:
                if temp[i][1] == "1" or temp[i][3] == "1":
                    normal = True
                    try:
                        handle = open(filename, "r", encoding="utf-8")
                        print(handle.read())
                    except IOError:
                        print("File is not found!")
                    finally:
                        handle.close()
        if not normal:
            print("You are not authorized to do this.")
            executor()


def logout_user():
    sys.exit()


def transfer_rights(filename: str, user_1: str, user_2: str, read: str, write: str,
                    execute: str):  # Нужно проверить: есть ли привилегии у пользователя на этот файл. если да,то он может наделить правами на него и другого пользователя
    if user_1 == "root":
        temp_array_user_2 = []
        with open(user_2 + ".csv", mode='r', encoding="utf-8") as r_file:
            filereader = csv.reader(r_file, delimiter=",")
            temp = []
            for row in filereader:
                temp.append(row)
        for i in temp:
            temp_array_user_2.append(i)
        for i in range(len(temp)):
            if temp[i][0] == filename:
                temp_array_user_2.pop(i)
        clear_file(user_2 + ".csv", "root")
        with open(user_2 + ".csv", mode="a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            tmp = [filename, read, write, execute]
            for i in temp_array_user_2:
                writer.writerow(i)
            writer.writerow(tmp)

    else:
        normal = False
        with open(user_1 + ".csv", mode="r") as r_file:
            filereader = csv.reader(r_file, delimiter=",")
            temp = []
            for row in filereader:
                temp.append(row)
        for i in range(len(temp)):
            if temp[i][0] == filename:
                if temp[i][1] == "1" and temp[i][2] == "1" and temp[i][3] == "1":
                    normal = True
                    temp_array_user_2 = []
                    with open(user_2 + ".csv", mode='r', encoding="utf-8") as r_file:
                        filereader = csv.reader(r_file, delimiter=",")
                        temp = []
                        for row in filereader:
                            temp.append(row)
                    for i in temp:
                        temp_array_user_2.append(i)
                    for i in range(len(temp)):
                        if temp[i][0] == filename:
                            temp_array_user_2.pop(i)
                    clear_file(user_2 + ".csv", "root")
                    with open(user_2 + ".csv", mode="a", newline="") as csv_file:
                        writer = csv.writer(csv_file)
                        tmp = [filename, read, write, execute]
                        for i in temp_array_user_2:
                            writer.writerow(i)
                        writer.writerow(tmp)

        if not normal:
            print("You are not authorized to do this.")
            executor()


def create_object(filename: str, user: str):
    handle = open(filename, "w")
    handle.write("")
    handle.close()
    with open(user + ".csv", "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        tmp = [filename, 1, 1, 1]
        writer.writerow(tmp)


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

print(login_list)
print(password_list)

login = ""
password = ""

check = True


def print_lists():
    global login_list, password_list
    print(login_list)
    print(password_list)


def login_user():
    global login, password
    login = str(input("Write login:"))
    password = str(input("Write password:"))


login_user()

while check:
    if login not in login_list or password not in password_list:
        print("login or password is wrong!")
        login_user()
    else:
        check = False
        break


def create_user():
    global login_list, password_list, login, password
    if login == "root" and password == "1234":
        login_new_user = str(input("login new user: "))
        password_new_user = str(input("password new user: "))
        tmp = [login_new_user, password_new_user]
        with open("login_password.csv", 'a', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(tmp)
        with open(login_new_user + ".csv",
                  'w') as csv_file:  # создание csv для нового пользователя, где будут отображаться его привилегии
            pass
    else:
        print("You are not authorized to do this.")
        executor()


if login == "root" and password == "1234":
    new_user_question = int(input("Create a new user? (1)Yes (2)No"))
    if new_user_question == 1:
        create_user()

if login == "exit":
    sys.exit()


def command_executor(command: str):
    if command == "create_object":
        name_object = str(input("write name object (without .txt ): "))
        create_object(name_object + ".txt", login)
    if command == "create_user":
        create_user()
    if command == "login_user":
        login_user()
    if command == "logout_user":
        logout_user()
    if command == "transfer_rights":
        filename = str(input("Write filename: "))
        user_1 = login
        user_2 = str(input("Write user_2: "))
        read = str(input("read: "))
        write = str(input("write: "))
        execute = str(input("execute: "))
        transfer_rights(filename + ".txt", user_1, user_2, read, write, execute)
    if command == "remove_file":
        filename = str(input("write name file: "))
        remove_file(filename, login)
    if command == "write_file":
        filename = str(input("write name file: "))
        message = str(input("write message: "))
        write_file(filename + ".txt", message, login)
    if command == "read_file":
        filename = str(input("write name file: "))
        read_file(filename + ".txt", login)
    if command == "print_lists":
        print_lists()
    if command == "clear_file":
        filename = str(input("write name file: "))
        clear_file(filename + ".txt", login)
    if command == "check_rights":
        filename = str(input("write filename: "))
        user = str(input("write user: "))
        check_rights(user, filename + ".txt")
    if command == "help":
        help()


flag = True


def executor():
    global flag
    while flag:
        temp_question = int(input("want to quit?(1)Yes(2)No: "))
        if temp_question == 2:
            command = str(input("write command: "))
            command_executor(command)
        if temp_question == 1:
            flag = False
            break
        if temp_question != 2 and temp_question != 1:
            print("Incorrect data")
            break


executor()
