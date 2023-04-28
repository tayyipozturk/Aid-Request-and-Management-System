import socket
import argparse
import threading
from Class.user import User
from Class.server_parser import ServerParser
from Class.campaign import Campaign
from Class.request import Request
from Class.item import Item
import os


class ClientThread(threading.Thread):
    def __init__(self, client_socket, address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        print(f"New connection from {self.address}")

    def run(self):
        token = None
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                data = data.split()
                self.client_socket.sendall("##EOF##".encode())
                if token != None:
                    if data[0] == "login":
                        self.client_socket.sendall(
                            "You are already logged in".encode())
                    elif data[0] == "new":
                        campaign = ServerParser.new(self.client_socket, data)
                    elif data[0] == "list":
                        ServerParser.list(self.client_socket, data)
                    elif data[0] == "open":
                        pass
                    elif data[0] == "close":
                        pass
                    else:
                        self.client_socket.sendall("Invalid command".encode())
                else:
                    if data[0] == "login":
                        token = ServerParser.login(self.client_socket, data)
                        # response = handle_request(data)
                        # self.client_socket.sendall(response.encode())
                    else:
                        self.client_socket.sendall(
                            "You should be logged in to execute a command.".encode())
            except Exception as e:
                print(f"Error: {e}")
                break
        print(f"Connection from {self.address} closed.")
        self.client_socket.close()


def handle_request(request):
    # process the request and return a response
    return "Hello, World!"


if __name__ == "__main__":
    requester = User("bob", "bob@localhost", "Bob", "123")
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int)

    HOST = "127.0.0.1"
    PORT = p.parse_args().port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on port {PORT}...")
    while True:
        client_socket, address = server_socket.accept()
        # data = client_socket.recv(1024).decode()
        # if data:
        #     # handle the received data
        #     response = handle_request(data)
        #     self.client_socket.sendall(response.encode())
        new_thread = ClientThread(client_socket, address)
        new_thread.start()
