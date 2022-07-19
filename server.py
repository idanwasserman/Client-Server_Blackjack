import socket
import threading
import tkinter as tk
import os
from constants import *
from model import Model
import json


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
output_lock = threading.Semaphore(value=1)


def _my_print(text):
    output_lock.acquire()
    print(text)
    output_lock.release()


def on_ct_button_clicked():
    """
    on create table button clicked.
    starting a new thread for the client.
    main thread is server's GUI.
    second thread is the server itself.
    """
    if _get_number_of_active_connections() < MAX_CLIENTS:
        num_of_players = int(nop_variable.get())
        num_of_decks = int(nod_variable.get())
        thread = threading.Thread(target=start_new_client, args=[num_of_players, num_of_decks])
        thread.start()
    else:
        _my_print(f'[ERROR] Cannot create more than {MAX_CLIENTS} tables')
        return


def start_new_client(num_of_players, num_of_decks):
    path = r'C:\seminar_client_server\Client-Server_Blackjack\controller.py'
    os.system(f'python {path} {num_of_players} {num_of_decks}')
    pass


def _get_numbers(conn):
    """
    first thing receiving from client is numbers dictionary
    input: conn- connection to the client
    output: numbers_dict- dictionary containing number of players and number of decks
    for the model of the client's table
    """
    numbers_dict = None
    while True:
        # receive length of upcoming data
        data_length = conn.recv(HEADER).decode(FORMAT)
        if not data_length:
            continue

        # receive data
        data_length = int(data_length)
        data = conn.recv(data_length).decode(FORMAT)

        if data == DISCONNECT_MSG:
            answer = {"disconnecting": True}
        elif data:
            numbers_dict = json.loads(data)
            answer = {"disconnecting": False}
        else:
            continue

        answer_to_send = json.dumps(answer).encode(FORMAT)
        answer_length = str(len(answer_to_send)).encode(FORMAT)
        answer_length += b' ' * (HEADER - len(answer_length))

        conn.send(answer_length)
        conn.send(answer_to_send)

        if numbers_dict:
            return numbers_dict


def handle_client(conn, addr):
    _my_print(f'[NEW CONNECTION] {addr} connected')

    numbers_dict = _get_numbers(conn)
    model = Model(num_of_players=numbers_dict[NUM_PLAYERS], num_of_decks=numbers_dict[NUM_DECKS])

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
            answer = {"disconnecting": True}
        else:
            answer = model.process_data(data)

        # encode answer
        answer_to_send = json.dumps(answer).encode(FORMAT)

        # compute answer length
        answer_length = str(len(answer_to_send)).encode(FORMAT)
        answer_length += b' ' * (HEADER - len(answer_length))

        # send the length of answer and answer itself
        conn.send(answer_length)
        conn.send(answer_to_send)

    conn.close()
    _my_print(f'[ACTIVE CONNECTIONS] {_get_number_of_active_connections() - 1}')


def start_server():
    _my_print(f'[LISTENING] server is listening on {HOST}')

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
        _my_print(f'[ACTIVE CONNECTIONS] {_get_number_of_active_connections()}')

    _my_print('[STOPPED] server has stopped')


def shut_down_server():
    # main thread is server's GUI
    # second thread is the server itself
    if _get_number_of_active_connections() > 0:
        _my_print(f'[ERROR] cannot shut down server ; there are still {_get_number_of_active_connections()} active clients')
        return

    global root, server

    _my_print('[SHUT DOWN] server is shutting down')

    server.close()

    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
    root.destroy()


def _get_number_of_active_connections():
    return int((threading.activeCount() - 2) / 2)


_my_print('[START] server is starting')

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
