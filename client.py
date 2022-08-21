import socket
from constants import *
import json


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (HOST, PORT)


class MyClient:
    """
    A class used to represent a client in the system

    Methods
    -------
    send_recv_data(data)
        Sends data to the server (first data's length, then the data itself).
        Receives data from server (first data's length, then the data itself).
        The function returns the received data.
    """

    def __init__(self):
        # opens a socket and connects it to address
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(ADDR)

    def send_recv_data(self, data):
        """
        Sends and receives data from the server

        Parameters
        ----------
        data : str
            data to send to the server

        Returns
        -------
        str
            data received from the server or None if received nothing
        """
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
