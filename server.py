import socket
import threading
import tkinter as tk
import os
from constants import *
from model import Model
import json
import file_utils


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)
output_lock = threading.Semaphore(value=1)

users_playing = []


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
    username = username_entry.get()
    if len(username) < MIN_USERNAME_LEN:
        _my_print(f'[ERROR] Username must be at least {MIN_USERNAME_LEN} characters')
        return

    if username in users_playing:
        _my_print(f'[ERROR] User {username} is already playing')
        return

    if _get_number_of_active_connections() < MAX_CLIENTS:
        users_playing.append(username)
        num_of_players = int(nop_variable.get())
        num_of_decks = int(nod_variable.get())
        user_money = _load_user_money(username)
        thread = threading.Thread(target=start_new_client, args=[num_of_players, num_of_decks, username, user_money])
        thread.start()
    else:
        _my_print(f'[ERROR] Cannot create more than {MAX_CLIENTS} tables')
        return


def _load_user_money(username):
    users = file_utils.load_users_from_file()
    if username in users:
        return users[username]
    else:
        return STARTER_MONEY_AMOUNT


def start_new_client(num_of_players, num_of_decks, username, user_money):
    path = r'C:\seminar_client_server\Client-Server_Blackjack\controller.py'
    os.system(f'python {path} {num_of_players} {num_of_decks} {username} {user_money}')
    pass


def _get_model_info(conn):
    """
    first thing receiving from client is model information dictionary
    input: conn- connection to the client
    output: model_info_dict- dictionary containing number of players, number of decks and user info
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

    model_info_dict = _get_model_info(conn)
    model = Model(
        num_of_players=model_info_dict[NUM_PLAYERS],
        num_of_decks=model_info_dict[NUM_DECKS],
        username=model_info_dict[USERNAME],
        user_money=model_info_dict[USER_MONEY]
    )

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
            answer = {DISCONNECTING: True}
        else:
            answer = model.process_data(data)
            if SWITCHER in answer:
                if answer[SWITCHER] == QUIT:
                    users_playing.remove(model_info_dict[USERNAME])

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
        msg = '[ERROR] cannot shut down server ; '
        msg += f'there are still {_get_number_of_active_connections()} active clients'
        _my_print(msg)
        return

    global root, server

    _my_print('[SHUT DOWN] server is shutting down')

    server.close()

    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()
    root.destroy()


def _get_number_of_active_connections():
    return int(threading.activeCount() / 2 - 1)


_my_print('[START] server is starting')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()


if __name__ == '__main__':
    root = tk.Tk()
    root.title(SERVER_TITLE)
    root.geometry("450x350")
    root.configure()

    # username frame
    user_frame = tk.Frame(root)
    user_frame.pack(padx=10, pady=10)
    username_label_text = 'Enter username:'
    username_label = tk.Label(user_frame, text=username_label_text, font=('Helvetica', 12))
    username_label.pack(side=tk.LEFT, padx=10, pady=10)
    username_entry = tk.Entry(user_frame)
    username_entry.pack(side=tk.LEFT, padx=10, pady=10)

    # nop = number of players
    nop_frame = tk.Frame(root)
    nop_frame.pack(padx=10, pady=10)
    nop_label_text = 'Select how many players in the table:'
    nop_label = tk.Label(nop_frame, text=nop_label_text, font=('Helvetica', 12))
    nop_label.pack(side=tk.LEFT, padx=10, pady=10)
    # number of players variable
    nop_variable = tk.StringVar(nop_frame)
    nop_variable.set(str(MIN_PLAYERS))
    nop_om = tk.OptionMenu(nop_frame, nop_variable, *[str(i) for i in range(MIN_PLAYERS, MAX_PLAYERS + 1)])
    nop_om.pack(side=tk.LEFT, padx=10, pady=10)

    # nod = number of decks
    nod_frame = tk.Frame(root)
    nod_frame.pack(padx=10, pady=10)
    nod_label_text = 'Select how many decks:'
    nod_label = tk.Label(nod_frame, text=nod_label_text, font=('Helvetica', 12))
    nod_label.pack(side=tk.LEFT, padx=10, pady=10)
    # number of decks variable
    nod_variable = tk.StringVar(nod_frame)
    nod_variable.set('1')
    nod_om = tk.OptionMenu(nod_frame, nod_variable, *[str(i) for i in range(1, 7)])
    nod_om.pack(side=tk.LEFT, padx=10, pady=10)

    # buttons frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(padx=10, pady=10)
    # create table button
    ct_button = tk.Button(buttons_frame, text=CREATE_TABLE, font=('Helvetica', 14), command=on_ct_button_clicked)
    ct_button.pack(padx=10, pady=10, side=tk.LEFT)
    # quit button
    quit_button = tk.Button(buttons_frame, text=QUIT, font=('Helvetica', 14), command=shut_down_server)
    quit_button.pack(padx=10, pady=10, side=tk.LEFT)

    root.mainloop()
