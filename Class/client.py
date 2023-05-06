import socket
import uuid
import argparse
import os
import re
import threading

mutex = threading.Lock()
cond = threading.Condition()


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


def get_input(client_socket):
    while True:
        message = input()
        client_socket.sendall(message.encode())


def get_response(client_socket):
    while True:
        response = client_socket.recv(1024).decode()
        eof_check = True if response.find("##EOF##") != -1 else False
        if eof_check:
            response = response.replace("##EOF##", "")
        resp = re.search("##EOF##", response)
        if response:
            print(response)
        if eof_check:
            break


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int)
    HOST = "localhost"
    PORT = p.parse_args().port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    in_thread = threading.Thread(target=get_input, args=(client_socket,))
    out_thread = threading.Thread(target=get_response, args=(client_socket,))

    in_thread.start()
    out_thread.start()

    in_thread.join()
    out_thread.join()
    client_socket.close()
    '''
    while True:
        message = input("Enter your message: ")
        client_socket.sendall(message.encode())
        while True:
            response = client_socket.recv(1024).decode()
            eof_check = True if response.find("##EOF##") != -1 else False
            if eof_check:
                response = response.replace("##EOF##", "")
            resp = re.search("##EOF##", response)
            if response:
                print(response)
            if eof_check:
                break



def receive_message(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print(data.decode('utf-8'))
            else:
                sock.close()
                break
        except:
            sock.close()
            break


def send_message(sock):
    while True:
        msg = input()
        try:
            sock.send(msg.encode('utf-8'))
        except:
            sock.close()
            break


if __name__ == '__main__':
    host = 'localhost'
    port = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    recv_thread = threading.Thread(target=receive_message, args=(sock,))
    recv_thread.start()

    send_thread = threading.Thread(target=send_message, args=(sock,))
    send_thread.start()
'''
