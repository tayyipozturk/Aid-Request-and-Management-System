import socket
import argparse
import threading
from Class.user import User
from Service.server_main_service import ServerParser
from Service.server_campaign_service import CampaignService
from Service.server_item_service import ItemService
from Class.campaign import Campaign
from Class.request import Request
from Class.item import Item
import os
import re


class ClientThread(threading.Thread):
    def __init__(self, client_socket, address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        self.user = None
        self.campaign = None
        self.watches = []
        self.token = None
        print(f"New connection from {self.address}")

    def run(self):
        while True:
            try:
                input_data = self.client_socket.recv(1024).decode()
                data = input_data.split()
                print(data)
                if self.token != None:
                    if data[0] == "login":
                        self.client_socket.sendall(
                            "You are already logged in".encode())
                        print(f"{self.address} tried to login again")
                    elif data[0] == "new":
                        input_new = re.search(
                            "new (?P<name>[a-zA-Z0-9]*) (?P<descr>(.*)*)", input_data)
                        ServerParser.new(self.client_socket, input_new)
                        print(f"{self.address} tried to create a new campaign")
                    elif data[0] == "list":
                        ServerParser.list(self.client_socket, data)
                        print(f"{self.address} tried to list campaigns")
                    elif data[0] == "open":
                        if not self.campaign:
                            input_open = re.search(
                                "open (?P<name>[a-zA-Z0-9]*)", input_data)
                            if input_open:
                                campaign = ServerParser.open(
                                    self.client_socket, input_open)
                                if campaign:
                                    self.campaign = campaign
                                else:
                                    self.client_socket.sendall(
                                        "Error".encode())
                        else:
                            self.client_socket.sendall(
                                "You already have a campaign opened".encode())
                        print(f"{self.address} tried to open a campaign")
                    elif data[0] == "close":
                        if self.campaign:
                            if ServerParser.close(
                                    self.client_socket, data, self.campaign, self.watches):
                                self.campaign = None
                                self.watches = []
                                self.client_socket.sendall(
                                    "Campaign closed".encode())
                            else:
                                self.client_socket.sendall(
                                    "Error".encode())
                        else:
                            self.client_socket.sendall(
                                "No campaign opened".encode())
                        print(f"{self.address} tried to close a campaign")
                    elif data[0] == "add_request":
                        if self.campaign:
                            # add_request <n_items> <items>(<name> <amount>) <latitude> <longtitude> <urgency> <descr>
                            input_addRequest = re.search(
                                "add_request (?P<n_items>[0-9]*) (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+) (?P<latitude>[0-9]*) (?P<longtitude>[0-9]*) (?P<urgency>[a-zA-Z]*) (?P<descr>(.*)*)", input_data)

                            if input_addRequest:
                                CampaignService.add_request(
                                    self.client_socket, input_addRequest, self.campaign, self.token)
                            else:
                                self.client_socket.sendall(
                                    "Error".encode())
                        else:
                            self.client_socket.sendall(
                                "No campaign opened".encode())
                        print(f"{self.address} tried to add a request")
                    elif data[0] == "get_request":
                        input_getRequest = re.search(
                            "get_request (?P<id>[a-zA-Z0-9\-]*)", input_data)
                        if input_getRequest:
                            CampaignService.get_request(
                                self.client_socket, input_getRequest, self.campaign)
                        else:
                            self.client_socket.sendall(
                                "Error".encode())
                    elif data[0] == "update_requests":
                        input_updateRequest = re.search(
                            "update_request (?P<n_items>[0-9]*) (?P<req_id>[a-zA-Z0-9\-]*) (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+) (?P<latitude>[0-9]*) (?P<longtitude>[0-9]*) (?P<urgency>[a-zA-Z]*) (?P<descr>(.*)*)", input_data)
                        if input_updateRequest:
                            CampaignService.update_request(
                                self.client_socket, input_updateRequest, self.campaign, self.token)
                        else:
                            self.client_socket.sendall(
                                "Error".encode())
                    elif data[0] == "remove_request":
                        input_removeRequest = re.search(
                            "remove_request (?P<id>[a-zA-Z0-9\-]*)", input_data)
                        if input_removeRequest:
                            CampaignService.remove_request(
                                self.client_socket, input_removeRequest, self.campaign)
                        else:
                            self.client_socket.sendall(
                                "Error".encode())

                    elif data[0] == "query":
                        # n_items, items, rectangular, (latitude, longtitude), (latitude, longtitude), urgency
                        input_queryRect = re.search(
                            "query (?P<n_items>[0-9]*) (?P<items>([a-zA-Z0-9]*)*) 0 (?P<latitude1>[0-9]*) (?P<longtitude1>[0-9]*) (?P<latitude2>[0-9]*) (?P<longtitude2>[0-9]*) (?P<urgency>[a-zA-Z]*)", input_data)
                        # n_items, items, circular, (latitude, longtitude, radius), urgency
                        input_queryCirc = re.search(
                            "query (?P<n_items>[0-9]*) (?P<items>([a-zA-Z0-9]*)*) 1 (?P<latitude>[0-9]*) (?P<longtitude>[0-9]*) (?P<radius>[0-9]*) (?P<urgency>[a-zA-Z]*)", input_data)

                        if input_queryRect:
                            CampaignService.query(
                                self.client_socket, input_queryRect, self.campaign, "rect")
                        elif input_queryCirc:
                            CampaignService.query(
                                self.client_socket, input_queryCirc, self.campaign, "circ")
                        else:
                            self.client_socket.sendall(
                                "Error".encode())
                    elif data[0] == "watch":
                        # n_items, items, rectangular, (latitude, longtitude), (latitude, longtitude), urgency
                        input_watchRect = re.search(
                            "watch (?P<n_items>[0-9]*) (?P<items>([a-zA-Z0-9]*)*) 0 (?P<latitude1>[0-9]*) (?P<longtitude1>[0-9]*) (?P<latitude2>[0-9]*) (?P<longtitude2>[0-9]*) (?P<urgency>[a-zA-Z]*)", input_data)
                        # n_items, items, circular, (latitude, longtitude, radius), urgency
                        input_watchCirc = re.search(
                            "watch (?P<n_items>[0-9]*) (?P<items>([a-zA-Z0-9]*)*) 1 (?P<latitude>[0-9]*) (?P<longtitude>[0-9]*) (?P<radius>[0-9]*) (?P<urgency>[a-zA-Z]*)", input_data)

                        if input_watchRect:
                            watch_id = CampaignService.watch(
                                self.client_socket, input_watchRect, self.campaign, "rect")
                            self.watches.append(watch_id)
                        elif input_watchCirc:
                            watch_id = CampaignService.watch(
                                self.client_socket, input_watchCirc, self.campaign, "circ")
                            self.watches.append(watch_id)
                        else:
                            self.client_socket.sendall(
                                "Error".encode())
                    elif data[0] == "unwatch":
                        pass
                    elif data[0] == "search_item":
                        input_searchItem = re.search(
                            "search_item (?P<name>[a-zA-Z0-9]*)", input_data)
                        if input_searchItem:
                            ItemService.search_item(
                                self.client_socket, input_searchItem)
                        else:
                            self.client_socket.sendall(
                                "Error".encode())
                        print(f"{self.address} tried to search an item")
                    elif data[0] == "update_item":
                        input_updateItem = re.search(
                            "update_item (?P<target>[a-zA-Z0-9]*) (?P<name>[a-zA-Z0-9]*)( )?(?P<synonyms>(.*)*)", input_data)
                        print(input_updateItem)
                        if input_updateItem:
                            ItemService.update_item(
                                self.client_socket, input_updateItem)
                    elif data[0] == "remove_item":
                        input_removeItem = re.search(
                            "remove_item (?P<name>[a-zA-Z0-9]*)", input_data)
                        if input_removeItem:
                            ItemService.remove_item(
                                self.client_socket, input_removeItem)
                    else:
                        self.client_socket.sendall("Invalid command".encode())
                        print(
                            f"{self.address} tried to execute an invalid command")
                else:
                    if data[0] == "login":
                        input_login = re.search(
                            "login (?P<username>[a-zA-Z0-9]*) (?P<password>[a-zA-Z0-9]*)", input_data)
                        self.token = ServerParser.login(
                            self.client_socket, input_login)
                    else:
                        self.client_socket.sendall(
                            "You should be logged in to execute a command.".encode())
                    print(f"{self.address} tried to login")
            except Exception as e:
                print(f"Error: {e}")
                break

        self.client_socket.sendall("##EOF##".encode())
        print(f"Connection from {self.address} closed.")
        if self.token:
            ServerParser.logout(self.client_socket, self.token)
            self.token = None
        self.client_socket.close()


def handle_request(request):
    # process the request and return a response
    return "Hello, World!"


if __name__ == "__main__":
    requester = User("bob", "bob@localhost", "Bob", "123")
    requester = User("mmm", "bob@localhost", "Bob", "123")
    campaign = Campaign("camp", "Here is the description")
    campaign2 = Campaign("campaign2", "Here is the description 2")
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
