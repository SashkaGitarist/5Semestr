import hashlib
import sys
from time import *
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox


def quit(event=None):
    soket.send(bytes("/exit", "utf8"))
    chat.destroy()
    sleep(1)
    chat.quit()


def quitbutt(event=None):
    soket.send(bytes("/exit", "utf8"))
    chat.destroy()
    sleep(1)
    chat.quit()


def log(event=None):
    nickname = nic.get()
    password = pas.get()
    h = hashlib.md5(password.encode())
    ht = h.hexdigest()
    soket.send(bytes(nickname, "utf8"))
    soket.send(bytes(ht, "utf8"))
    msg = soket.recv(buff).decode("utf8")
    if msg == "1":
        login.destroy()
    else:
        messagebox.showerror(title="Error", message="Вы ввели неверные данные")


def conn(event=None):
    global HOST
    global PORT
    HOST = host.get()
    PORT = port.get()
    connect.destroy()


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    soket.send(bytes(msg, "utf8"))


def read_sock(event=None):
    while 1:
        msg = soket.recv(buff).decode("utf8")
        msg_list.insert(END, msg)


def rainbow(tk):
    MAX_ROW = 7
    FONT_SIZE = 5
    rainbow = ["red", "orange", "yellow", "green", "blue", "purple", "brown"]
    row = 0
    col = 0
    for i in range(70):
        for color in rainbow:
            e = Label(tk, background=color)
            e.grid(row=row, column=col, sticky=E + W)
            row += 1
            if (row > 6):
                row = 0
                col += 1


connect = Tk()
connect.title("Подключение")
connect.geometry('380x130')
connect.resizable(width=False, height=False)
host, port = StringVar(), StringVar()
label1 = Label(connect, text="Хост:")
label2 = Label(connect, text="Порт:")
entry1 = Entry(connect, textvariable=host)
entry2 = Entry(connect, textvariable=port)
button = Button(connect, relief=GROOVE, text="Отправить")

button.bind("<Button-1>", conn)
label1.place(x=20, y=20)
label2.place(x=20, y=50)
entry1.place(x=60, y=20, width=270)
entry2.place(x=60, y=50, width=270)
button.place(x=160, y=80)

# Стиль
bgr = "snow3"
connect.configure(bg=bgr)
label1.configure(bg=bgr)
label2.configure(bg=bgr)
connect.mainloop()

buff = 4096
address = (HOST, int(PORT))

soket = socket(AF_INET, SOCK_STREAM)
soket.connect(address)

login = Tk()
name = StringVar()
pas = StringVar()

login.title("Авторизация")
login.geometry('380x130')
login.resizable(width=False, height=False)

lbl = Label(login, text="Логин:")
lbl.place(x=20, y=20)

lbp = Label(login, text="Пароль:")
lbp.place(x=20, y=50)

nic = Entry(login, textvariable=name, width=40)
nic.place(x=80, y=20)

pas = Entry(login, textvariable=pas, show="*", width=40)
pas.place(x=80, y=50)

btn = Button(login, text="Отправить", command=log)
btn.place(x=155, y=90)

login.protocol("WM_DELETE_WINDOW", login.quit)

login.configure(bg=bgr)
lbl.configure(bg=bgr)
lbp.configure(bg=bgr)

login.mainloop()

chat = Tk()

chat.title("Чат")
chat.geometry('650x320')
chat.resizable(width=False, height=False)
my_msg = StringVar()
my_msg.set("")

frame = Frame(chat)
scrollbar = Scrollbar(frame, takefocus=True)
msg_list = Listbox(frame, height=45, width=100, yscrollcommand=scrollbar.set)
entry_field = Entry(chat, textvariable=my_msg)
entry_field.bind("<Return>", send)
send = Button(chat, text="Отправить", command=send)
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
frame.place(x=15, y=35, width=620, height=240)
entry_field.place(x=15, y=280, width=440)
send.place(x=460, y=280, width=85)
chat.protocol("WM_DELETE_WINDOW", quit)
scrollbar.configure(command=msg_list.yview)

chat.configure(bg=bgr)

Exitik = msg_list.selection_clear(0, END)
ExitikBtn = Button(chat, text="Выход", command=quitbutt)

ExitikBtn.place(x=550, y=280, width=85)

fontStyle = tkFont.Font(size=19)
labelchatnick = Label(chat, text="Ваш ник: %s" % name.get(), font=fontStyle)
labelchatnick.place(x=15, y=0)
labelchatnick.configure(bg=bgr)


def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    My_label.config(text="Время: " + hour + ":" + minute + ":" + second)
    My_label.after(1000, clock)


My_label = Label(chat, text="", font=("Helvetica", 19), fg="black", bg=bgr)
My_label.place(x=445, y=0)
clock()

receive_thread = Thread(target=read_sock)
receive_thread.start()

chat.mainloop()
