import socket
import threading
import tkinter
from tkinter import *


host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

window = tkinter.Tk()
window.geometry('1920x1080')
window.title('Tkinter Chat Server')




def universal():


    # hostip = '[ip of your choice]'
    hostip = '127.0.0.1'
    # port = [port of your choice]
    port = 80

    messages = Listbox(window, width=200, height=40, fg='black', background='light grey')
    messages.pack()
    host.bind((hostip, port))
    messages.insert(END, f"Server online, host address [{hostip}], port [{port}]")
    host.listen()
    def main():





        usernames = []
        addresses = []


        def broadcast(msg):
            for address in addresses:
                address.sendall(msg)

        def handle(address, username):
            while True:
                try:
                    msg = address.recv(1024).decode()
                    messages.insert(END, msg)
                    message_send = username+' : '+msg
                    broadcast(message_send.encode())
                except:
                    addresses.remove(address)
                    address.close()
                    broadcast(f'<<{username} has left>>'.encode())
                    usernames.remove(username)
                    break

        def recieve():
            while True:
                address, addr = host.accept()
                messages.insert(END, f'{str(address)} has connected')
                address.send('name'.encode())
                messages.insert(END, 'code sent')
                username = address.recv(1024).decode()
                usernames.append(username)

                addresses.append(address)

                messages.insert(END, f"{username} has connected")
                broadcast(f'\n{username} has joined'.encode())
                address.send('Connected'.encode())

                thread = threading.Thread(target=handle, args=(address, username))
                thread.start()







        recieve()

    main()


threading.Thread(target=universal, daemon=True).start()
window.mainloop()

