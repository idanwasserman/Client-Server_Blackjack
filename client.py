import socket
from constants import *
import json


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)


class MyClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

    def send_recv_data(self, data):
        # encode data
        data = data.encode(FORMAT)

        # compute data length
        data_length = len(data)
        send_length = str(data_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))

        # send the length of data and data itself
        self.client.send(send_length)
        self.client.send(data)

        # receive length of upcoming data
        recv_data_length = self.client.recv(HEADER).decode(FORMAT)
        if not recv_data_length:
            print(f'client.py - send_recv_data: recv_data_length is None')
        recv_data_length = int(recv_data_length)

        # receive data
        recv_data = self.client.recv(recv_data_length)

        if recv_data is None:
            return

        recv_data = json.loads(recv_data)
        return recv_data

