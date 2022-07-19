import socket
from constants import *


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)


class MyClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

    def send_recv_data(self, data):
        data = data.encode(FORMAT)
        data_length = len(data)
        send_length = str(data_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(data)
        recv_data = self.client.recv(1024).decode(FORMAT)
        return recv_data

