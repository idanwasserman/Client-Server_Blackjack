import socket
import threading
import tkinter as tk
import os
from constants import *


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)


def on_ct_button_clicked():
    # main thread is server's GUI
    # second thread is the server itself
    if threading.activeCount() - 2 < MAX_CLIENTS:
        num_of_players = int(nop_variable.get())
        num_of_decks = int(nod_variable.get())
        thread = threading.Thread(target=start_new_client, args=[num_of_players, num_of_decks])
        thread.start()
    else:
        print(f"Cannot create more than {MAX_CLIENTS} tables")
        return


def start_new_client(num_of_players, num_of_decks):
    path = r'C:\seminar_client_server\Client-Server_Blackjack\controller.py'
    os.system(f'python {path} {num_of_players} {num_of_decks}')
    pass


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected')

    connected = True
    while connected:
        # receive length of upcoming data
        data_length = conn.recv(HEADER).decode(FORMAT)
        if not data_length:
            continue

        # receive data
        data_length = int(data_length)
        data = conn.recv(data_length).decode(FORMAT)

        if data == DISCONNECT_MSG:
            connected = False
        else:
            # TODO: do something with data received from client
            answer = f"server answer for client's data: {data}"
            conn.send(answer.encode(FORMAT))
            pass

        print(f'[{addr}] server got this data from client: {data}')
        # conn.send("from server: data received".encode(FORMAT))

    conn.close()
    print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 2}')


def start_server():
    print(f'[LISTENING] server is listening on {HOST}')
    server.listen()
    server_on = True
    while True:
        try:
            conn, addr = server.accept()
        except OSError:
            server_on = False

        if not server_on:
            break

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.daemon = True
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 2}')

    print(f'[STOPPED] server has stopped')


def shut_down_server():
    # main thread is server's GUI
    # second thread is the server itself
    if threading.activeCount() - 2 > 0:
        print(f'[ERROR] cannot shut down server ; there are still {threading.activeCount() - 2} active clients')
        return

    global root, server

    print(f'[SHUT DOWN] server is shutting down')
    server.close()

    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
    root.destroy()


print('[START] server is starting')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()


if __name__ == '__main__':
    root = tk.Tk()
    root.title(SERVER_TITLE)
    root.geometry("400x250")
    root.configure()

    first_frame = tk.Frame(root)
    first_frame.pack(padx=10, pady=10)

    nop_label_text = 'Select how many players in the table:'
    nop_label = tk.Label(first_frame, text=nop_label_text, font=('Helvetica', 12))
    nop_label.pack(side=tk.LEFT, padx=10, pady=10)

    # number of players variable
    nop_variable = tk.StringVar(first_frame)
    nop_variable.set(str(MIN_PLAYERS))
    nop_om = tk.OptionMenu(first_frame, nop_variable, *[str(i) for i in range(MIN_PLAYERS, MAX_PLAYERS + 1)])
    nop_om.pack(side=tk.LEFT, padx=10, pady=10)

    second_frame = tk.Frame(root)
    second_frame.pack(padx=10, pady=10)

    nod_label_text = 'Select how many decks in a game:'
    nod_label = tk.Label(second_frame, text=nod_label_text, font=('Helvetica', 12))
    nod_label.pack(side=tk.LEFT, padx=10, pady=10)

    # number of decks variable
    nod_variable = tk.StringVar(second_frame)
    nod_variable.set('1')
    nod_om = tk.OptionMenu(second_frame, nod_variable, *[str(i) for i in range(1, 7)])
    nod_om.pack(side=tk.LEFT, padx=10, pady=10)

    third_frame = tk.Frame(root)
    third_frame.pack(padx=10, pady=10)

    ct_button = tk.Button(third_frame, text=CREATE_TABLE, font=('Helvetica', 14), command=on_ct_button_clicked)
    ct_button.pack(padx=10, pady=10, side=tk.LEFT)

    quit_button = tk.Button(third_frame, text=QUIT, font=('Helvetica', 14), command=shut_down_server)
    quit_button.pack(padx=10, pady=10, side=tk.LEFT)

    root.mainloop()
