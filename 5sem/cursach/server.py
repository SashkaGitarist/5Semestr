import socket
import random
from threading import Thread
import sqlite3
import hashlib
import uuid
import sys
from time import sleep
import time


def login(client):
    connection = sqlite3.connect("DataBasik.db")
    cursor = connection.cursor()
    while 1:
        nickname = client.recv(buff).decode("utf8")
        password = client.recv(buff).decode("utf8")
        zapros = ("""SELECT Nickname, Password FROM Login WHERE  
                                Nickname = '{}' AND Password = '{}'""").format(nickname, password)
        cursor.execute(zapros)
        results = cursor.fetchall()
        try:
            if nickname == results[0][0]:
                client.send(bytes("1", "utf8"))
                connection.close()
                return nickname
        except IndexError:
            client.send(bytes("0", "utf8"))


def process_conn():
    while 1:
        client, client_address = SERVER.accept()
        name = login(client)
        print("Подключен ", name, " с адресом %s:%s " % client_address)
        addresses[client] = client_address
        test1[name] = client_address
        test2[name] = ADDR
        Thread(target=processing_client, args=(client, name)).start()


def processing_client(client, name):
    clients[client] = name
    sendall(bytes("%s присоединился" % name, "utf8"))
    rassilka(client)

    while 1:
        msg = client.recv(buff)

        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")
        timesend = hour + ":" + minute + ":" + second

        print("Сообщение в " + timesend + " от пользователя " + name + ": " + msg.decode('utf8'))

        if msg == bytes("/exit", "utf8"):
            print("Отключился пользователь с именем: %s" % name)
            client.send(bytes("%s покинул чат" % name, "utf8"))
            sleep(0.5)
            client.close()
            sleep(0.5)
            del clients[client]
            break

        elif msg == bytes("/register", "utf8"):
            if name != "Admin":
                client.send(bytes("У тебя нет доступа!", "utf8"))
            else:
                connection = sqlite3.connect("DataBasik.db")
                cursor = connection.cursor()
                client.send(bytes("Логин", "utf8"))
                nickname = client.recv(buff).decode("utf8")
                client.send(bytes("Пароль", "utf8"))
                password = client.recv(buff).decode("utf8")
                h = hashlib.md5(password.encode())
                ht = h.hexdigest()
                zapros = ("""INSERT INTO Login(Nickname, Password) VALUES('{}','{}')""").format(nickname, ht)
                cursor.execute(zapros)
                connection.commit()
                connection.close()
                client.send(bytes("Пользователь зарегистрирован", "utf8"))

        elif msg == bytes("/66", "utf8"):
            if name != "Admin":
                client.send(bytes("У тебя нет доступа!"), "utf8")
            else:
                connection = sqlite3.connect("DataBasik.db")
                cursor = connection.cursor()
                client.send(bytes("\"Коммандер Коди... Вот время и настало. Выполнить приказ 66\"", "utf8"))
                zapros = ("""DELETE FROM Login WHERE key > 1 """)
                cursor.execute(zapros)
                connection.commit()
                connection.close()
                client.send(bytes("Приказ 66 исполнен", "utf8"))
                sleep(0.5)
                client.send(bytes(" ", "utf8"))

        elif msg == bytes("/help", "utf8"):
            client.send(bytes("Помощь пришла!", "utf8"))
            client.send(bytes("А чтобы она не только пришла, но и помогла - обратись к админу сервера :)", "utf8"))
            sleep(0.5)
            client.send(bytes(" ", "utf8"))

        elif msg == bytes("/adr", "utf8"):

            client.send(bytes("Чекай консоль", "utf8"))

            print(test1)

        elif msg == bytes("/clients", "utf8"):
            client.send(bytes("Список пользователей в чате: ", "utf8"))
            strings = []
            for key, value in clients.items():
                strings.append("{}".format(value))
            result = "; ".join(strings)
            client.send(bytes(result, "utf8"))
            sleep(0.5)
            client.send(bytes(" ", "utf8"))
            # Модуль веселья
        elif msg == bytes("/cat", "utf8"):
            client.send(bytes("\t\t人____人", "utf8"))
            client.send(bytes("≧(◕ ‿‿ ◕)≦", "utf8"))
            sleep(0.5)
            client.send(bytes(" ", "utf8"))

        elif msg == bytes("/emoji", "utf8"):
            client.send(bytes("Вам выберется рандомное эмоджи :)", "utf8"))
            emoji = ["( ͡° ͜ʖ ͡°)", "(*^ω^)", "(^人^)", "(✯◡✯)", "(◕‿◕)", "＼(≧▽≦)／", "(－‸ლ)", "(>ω^)", "(•ิ_•ิ)?",
                     "(／。＼)", "(＃＞＜)", "ヽ(♡‿♡)ノ", "(ﾉ´з｀)ノ", "(＞ｍ＜)", "(◣_◢)", " ╮(￣_￣)╭",
                     "┐( ˘ ､ ˘ )┌", "(◎ ◎)", "(O.O)", "Σ(ﾟロﾟ)", "(＾• ω •＾)", "︻デ═一", "(╮°-°)╮┳━━┳", "(╯°益°)╯彡┻━┻",
                     "┬─┬ノ( º _ ºノ)", "( ˘▽˘)っ♨", "(*￣ii￣)", "٩(ˊ〇ˋ*)و", "(￣^￣)ゞ", "✞", "❤", "👽"]

            randomEmo = random.choice(emoji)
            client.send(bytes(f"{randomEmo}", "utf8"))
            sleep(0.5)
            client.send(bytes(" ", "utf8"))

        else:
            sendall(msg, timesend + " " + name + ": ")
            MsgConnection = sqlite3.connect("DataBasik.db")
            cursor = MsgConnection.cursor()
            savemsg = ("""INSERT INTO MessageDataBase(Name, Timesend , Message) VALUES('{}','{}','{}')""").format(name,
                                                                                                                  timesend,
                                                                                                                  msg.decode(
                                                                                                                      'utf8'))
            cursor.execute(savemsg)
            MsgConnection.commit()
            MsgConnection.close()


def rassilka(client):
    sleep(1)
    client.send(bytes("-------------------------------", "utf8"))
    sleep(1)
    client.send(bytes("\nПриветствую в самом ламповом чате!", "utf8"))
    sleep(1)
    client.send(bytes("(*・ω・)ﾉ", "utf8"))
    sleep(1)
    client.send(bytes("Тут ты сможешь найти себе друга, подругу, жену, тещу или кирюху", "utf8"))
    sleep(1)
    client.send(bytes("Список команд, действующих в чате: ", "utf8"))
    sleep(0.5)
    client.send(bytes("/help - неотложная помощь", "utf8"))
    sleep(0.5)
    client.send(bytes("/w - Личное сообщение", "utf8"))
    sleep(0.5)
    client.send(bytes("/clients - список пользователей", "utf8"))
    sleep(0.5)
    client.send(bytes("/emoji - смайлики для общения", "utf8"))
    sleep(0.5)
    client.send(bytes("/cat - кошечка для развлечения", "utf8"))
    sleep(0.5)
    client.send(bytes("Приятного общения!", "utf8"))
    sleep(0.5)
    client.send(bytes("-------------------------------", "utf8"))
    sleep(0.4)


def sendall(msg, prefix=""):
    for client in clients:
        client.send(bytes(prefix, "utf8") + msg)


def check():
    if uuid.getnode() != 168202120781163:
        print("*Биб-Биб* Сервер не хочет запускаться! *Биб-бам...*")
        sys.exit(0)
    else:
        print("Сервер можно запустить")


check()

clients = {}
addresses = {}
test1 = {}
test2 = {}

HOST = socket.gethostbyname(socket.gethostname())
print("Хост: " + HOST)
PORT = 9090
print("Порт: " + str(PORT))
buff = 4096
ADDR = (HOST, PORT)

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind(ADDR)

SERVER.listen(10)
print("Сервер запущен")

ACCEPT_THREAD = Thread(target=process_conn)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()

SERVER.close()
