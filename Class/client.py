import socket
import uuid
import argparse
import os


class Client:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.id = uuid.uuid4()

    def __str__(self):
        return f"Client: {self.name} - {self.phone} - {self.email}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.id == other.id


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int)
    HOST = "localhost"
    PORT = p.parse_args().port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    while True:
        message = input("Enter your message: ")
        client_socket.sendall(message.encode())
        while True:
            response = client_socket.recv(1024).decode()
            print(f"Received response: {response}\n")
            if response == "##EOF##":
                break
    client_socket.close()
