import os
import socket
import tkinter
import threading
from tkinter import *
import urllib
from urllib.request import Request, urlopen
from PIL import ImageTk
#from PIL import Image
from customtkinter import *


window = CTk()
window.geometry('600x300')
window.title('Tkinter Chat Server')

req = Request(
    url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Solid_white_bordered.svg/2048px-Solid_white_bordered.svg.png',
    headers={'User-Agent': 'Mozilla/5.0'}
)
url=urlopen(req)
data_r = url.read()
url.close()
photo = ImageTk.PhotoImage(data=data_r)


#img = Image.open('wra.png')
#photo = PhotoImage(file=photo)
#window.iconphoto(False, photo)
#window.configure()



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def server():

    s.connect(('127.0.0.1', 80))
    #connected = Label(window, text='connected to server', fg='green')
    #connected.pack()
    # connected = Label(window, text='connected to server', fg='green')
    # connected.pack()
    # users()

    # notConnected = Label(window, text='server offline', fg='red')
    # os.close(1)

    def main():
        window.geometry('1920x1080')

        messages = CTkTextbox(window, width=1000, height=800)
        messages.place(relx=0.5, rely=0.375, anchor=CENTER)

        message = CTkEntry(window, width=200, height=10)
        message.place(relx=0.5, rely=0.9, anchor=CENTER)

        def recieve():
            # username = input('Enter username : ')

            while True:
                try:
                    msg = s.recv(1024).decode()

                    if msg == 'name':
                        s.send(user.encode())
                    # elif msg == 'endex':
                    #    print('\nServer is now offline we are sorry for any inconvenience, this could be due to updates or server upgrade \nnethertheless we asure it will be up any time soon')
                    # elif msg == 'NMORE':
                    #    print("We are very sorry but all servers are permanently being shutdown, we are very sorry and we hope you have a good day ")

                    # username = input('Enter username : ')

                    else:
                        messages.insert(END, '\n'+msg)


                except:
                    error = Label(window,
                                  text='error with connection, this could be a problem with the servers or with your internet connection',
                                  fg='red')
                    error.pack()
                    s.close()
                    break

        def sends():

            def destroy_b():
                send_message.destroy()
                leave.destroy()
                sends()

            def __send__():
                msg = message.get()
                s.send(msg.encode())
                destroy_b()

            def leave_chat():
                s.close()
                os.close(1)

            send_message = CTkButton(window, text='Send', command=__send__, width=50)
            send_message.place(relx=0.4, rely=0.9, anchor=CENTER)

            leave = CTkButton(window, text='Leave', command=leave_chat, width=50)
            leave.place(relx=0.6, rely=0.9, anchor=CENTER)

        send_thread = threading.Thread(target=sends, )
        send_thread.start()

        recieve_thread = threading.Thread(target=recieve)
        recieve_thread.start()

    def users():

        yes_name = s.recv(1024).decode()
        username = CTkEntry(window, width=300)
        username.place(relx=0.5, rely=0.1, anchor=CENTER)

        def get_username():
            global user
            user = username.get()
            if yes_name == 'name':
                s.send(user.encode())

            else:
                s.close()
                os.close(1)

            username.destroy()
            send_username.destroy()
            main()

        send_username = CTkButton(window, text='Join', command=get_username)
        send_username.place(relx=0.5, rely=0.2, anchor=CENTER)

    users()
    #window.mainloop()

server()
window.mainloop()
