import socket
import threading
import tkinter as tk
import os


HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MSG = '!DISCONNECT!'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)

MIN_NUM_PLAYERS = 1
MAX_NUM_PLAYERS = 3
MAX_NUM_TABLES = 3

tables_counter = 0


def on_ct_button_clicked():
    global tables_counter
    if tables_counter < MAX_NUM_TABLES:
        tables_counter += 1
        num_of_players = int(nop_variable.get())
        num_of_decks = int(nod_variable.get())
        thread = threading.Thread(target=start_new_client, args=[num_of_players, num_of_decks])
        thread.start()
    else:
        print("Cannot create more tables")
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

        print(f'[{addr}] {data}')
        conn.send("from server: data received".encode(FORMAT))

    conn.close()
    print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


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
        print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')

    server.close()
    print(f'[STOPPED] server has stopped')


def shut_down_server():

    print(f'[SHUT DOWN] server is shutting down')
    global server, root
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
    global root
    root = tk.Tk()
    root.title('Server')
    root.geometry("400x250")
    root.configure()

    first_frame = tk.Frame(root)
    first_frame.pack(padx=10, pady=10)

    nop_label_text = f'Select how many players in the table:'
    nop_label = tk.Label(first_frame, text=nop_label_text, font=('Helvetica', 12))
    nop_label.pack(side=tk.LEFT, padx=10, pady=10)

    # number of players variable
    nop_variable = tk.StringVar(first_frame)
    nop_variable.set(str(MIN_NUM_PLAYERS))
    nop_om = tk.OptionMenu(first_frame, nop_variable, *[str(i) for i in range(MIN_NUM_PLAYERS, MAX_NUM_PLAYERS + 1)])
    nop_om.pack(side=tk.LEFT, padx=10, pady=10)

    second_frame = tk.Frame(root)
    second_frame.pack(padx=10, pady=10)

    nod_label_text = f'Select how many decks in a game:'
    nod_label = tk.Label(second_frame, text=nod_label_text, font=('Helvetica', 12))
    nod_label.pack(side=tk.LEFT, padx=10, pady=10)

    # number of decks variable
    nod_variable = tk.StringVar(second_frame)
    nod_variable.set('1')
    nod_om = tk.OptionMenu(second_frame, nod_variable, *[str(i) for i in range(1, 7)])
    nod_om.pack(side=tk.LEFT, padx=10, pady=10)

    third_frame = tk.Frame(root)
    third_frame.pack(padx=10, pady=10)

    ct_button = tk.Button(third_frame, text='Create table', font=('Helvetica', 14), command=on_ct_button_clicked)
    ct_button.pack(padx=10, pady=10, side=tk.LEFT)

    quit_button = tk.Button(third_frame, text='Quit', font=('Helvetica', 14), command=shut_down_server)
    quit_button.pack(padx=10, pady=10, side=tk.LEFT)

    root.mainloop()


