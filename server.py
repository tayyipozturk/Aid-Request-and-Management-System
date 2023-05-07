import socket
import argparse
import threading
import uuid
from Class.user import User
from Service.server_main_service import ServerParser
from Service.server_campaign_service import CampaignService
from Service.server_item_service import ItemService
from Service.server_request_service import RequestService
from Class.campaign import Campaign
from Class.request import Request
from Class.item import Item
from Class.watch_monitor import WatchMonitor
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
        self.watch_monitor = WatchMonitor(client_socket)
        self.watch_monitor.run()
        print(f"New connection from {self.address}")

    def run(self):
        while True:
            try:
                input_data = self.client_socket.recv(1024).decode()
                data = input_data.split()
                print(data)
                if self.token != None:
                    if data[0] == "login":
                        self.watch_monitor.enqueue(
                            "You are already logged in")
                        # self.client_socket.sendall("You are already logged in".encode())
                        print(f"{self.address} tried to login again")
                    elif data[0] == "new":
                        input_new = re.search(
                            "new (?P<name>[a-zA-Z0-9]*) (?P<descr>(.*)*)", input_data)
                        ServerParser.new(self.watch_monitor, input_new)
                        print(f"{self.address} tried to create a new campaign")
                    elif data[0] == "list":
                        ServerParser.list(self.watch_monitor, data)
                        print(f"{self.address} tried to list campaigns")
                    elif data[0] == "open":
                        if not self.campaign:
                            input_open = re.search(
                                "open (?P<name>[a-zA-Z0-9]*)", input_data)
                            if input_open:
                                campaign = ServerParser.open(
                                    self.watch_monitor, input_open)
                                if campaign:
                                    self.campaign = campaign
                                else:
                                    self.watch_monitor.enqueue(
                                        "Campaign not found")
                        else:
                            self.watch_monitor.enqueue(
                                "You already have a campaign opened")
                        print(f"{self.address} tried to open a campaign")
                    elif data[0] == "close":
                        if self.campaign:
                            if ServerParser.close(
                                    self.watch_monitor, data, self.campaign, self.watches):
                                self.campaign = None
                                self.watches = []
                                self.watch_monitor.enqueue(
                                    "Campaign closed")
                            else:
                                self.watch_monitor.enqueue(
                                    "Error")
                        else:
                            self.watch_monitor.enqueue(
                                "No campaign opened")
                        print(f"{self.address} tried to close a campaign")
                    elif data[0] == "add_request":
                        if self.campaign:
                            # add_request <items>(<name> <amount>) <latitude> <longtitude> <urgency> <descr>
                            input_addRequest = re.search(
                                "add_request (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+) (?P<latitude>[0-9\.]*) (?P<longtitude>[0-9\.]*) (?P<urgency>[a-zA-Z]*) (?P<descr>(.*)*)", input_data)

                            if input_addRequest:
                                CampaignService.add_request(
                                    self.watch_monitor, input_addRequest, self.campaign, self.token)
                            else:
                                self.watch_monitor.enqueue(
                                    "Error")
                        else:
                            self.watch_monitor.enqueue(
                                "No campaign opened")
                        print(f"{self.address} tried to add a request")
                    elif data[0] == "get_request":
                        input_getRequest = re.search(
                            "get_request (?P<id>[a-zA-Z0-9\-]*)", input_data)
                        if input_getRequest:
                            CampaignService.get_request(
                                self.watch_monitor, input_getRequest, self.campaign)
                        else:
                            self.watch_monitor.enqueue(
                                "Error")
                    elif data[0] == "update_request":
                        input_updateRequest = re.search(
                            "update_request (?P<req_id>[a-zA-Z0-9\-]*) (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+) (?P<latitude>[0-9\.]*) (?P<longtitude>[0-9\.]*) (?P<urgency>[a-zA-Z]*) (?P<descr>(.*)*)", input_data)
                        if input_updateRequest:
                            try:
                                CampaignService.update_request(
                                    self.watch_monitor, input_updateRequest, self.campaign, self.token)
                            except:
                                self.watch_monitor.enqueue(
                                    "Error")
                        else:
                            self.watch_monitor.enqueue(
                                "Error")
                    elif data[0] == "remove_request":
                        input_removeRequest = re.search(
                            "remove_request (?P<id>[a-zA-Z0-9\-]*)", input_data)
                        if input_removeRequest:
                            CampaignService.remove_request(
                                self.watch_monitor, input_removeRequest, self.campaign)
                        else:
                            self.watch_monitor.enqueue(
                                "Error")

                    elif data[0] == "query":
                        # items, rectangular, (latitude, longtitude), (latitude, longtitude), urgency
                        input_queryRect = re.search(
                            "query (?P<items>([a-zA-Z0-9]*)*) 0 (?P<latitude1>[0-9\.]*) (?P<longtitude1>[0-9\.]*) (?P<latitude2>[0-9\.]*) (?P<longtitude2>[0-9\.]*) (?P<urgency>[a-zA-Z]*)", input_data)
                        # items, circular, (latitude, longtitude, radius), urgency
                        input_queryCirc = re.search(
                            "query (?P<items>([a-zA-Z0-9]*)*) 1 (?P<latitude>[0-9\.]*) (?P<longtitude>[0-9\.]*) (?P<radius>[0-9]*) (?P<urgency>[a-zA-Z]*)", input_data)

                        if input_queryRect:
                            CampaignService.query(
                                self.watch_monitor, input_queryRect, self.campaign, "rect")
                        elif input_queryCirc:
                            CampaignService.query(
                                self.watch_monitor, input_queryCirc, self.campaign, "circ")
                        else:
                            self.watch_monitor.enqueue("Error query")
                    elif data[0] == "watch":
                        # items, rectangular, (latitude, longtitude), (latitude, longtitude), urgency
                        input_watchRect = re.search(
                            "watch (?P<items>([a-zA-Z0-9]*)*) 0 (?P<latitude1>[0-9\.]*) (?P<longtitude1>[0-9\.]*) (?P<latitude2>[0-9\.]*) (?P<longtitude2>[0-9\.]*) (?P<urgency>[a-zA-Z]*)", input_data)
                        # items, circular, (latitude, longtitude, radius), urgency
                        input_watchCirc = re.search(
                            "watch (?P<items>([a-zA-Z0-9]*)*) 1 (?P<latitude>[0-9\.]*) (?P<longtitude>[0-9\.]*) (?P<radius>[0-9]*) (?P<urgency>[a-zA-Z]*)", input_data)

                        if input_watchRect:
                            watch_id = CampaignService.watch(
                                self.watch_monitor, input_watchRect, self.campaign, "rect")
                            self.watches.append(watch_id)
                        elif input_watchCirc:
                            watch_id = CampaignService.watch(
                                self.watch_monitor, input_watchCirc, self.campaign, "circ")
                            self.watches.append(watch_id)
                        else:
                            self.watch_monitor.enqueue("Error watch")
                    elif data[0] == "unwatch":
                        input_unwatch = re.search(
                            "unwatch (?P<id>[a-zA-Z0-9\-]*)", input_data)
                        if input_unwatch:
                            id_uuid = uuid.UUID(input_unwatch.group("id"))
                            if id_uuid in self.watches:
                                CampaignService.unwatch(
                                    self.watch_monitor, id_uuid, self.campaign)
                                self.watches.remove(id_uuid)
                        else:
                            self.watch_monitor.enqueue("Error unwatch")
                    elif data[0] == "mark_available":
                        input_markAvailable = re.search(
                            "mark_available (?P<id>[a-zA-Z0-9\-]*) (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+) (?P<expire>[0-9]*) (?P<latitude>[0-9\.]*) (?P<longtitude>[0-9\.]*) (?P<comment>(.*)*)", input_data)
                        if input_markAvailable:
                            RequestService.mark_available(
                                self.watch_monitor, input_markAvailable, self.campaign, self.token)
                        else:
                            self.watch_monitor.enqueue("Error mark_available")
                    elif data[0] == "pick":
                        input_pick = re.search(
                            "pick (?P<req_id>[a-zA-Z0-9\-]*) (?P<ma_id>[a-zA-Z0-9\-]*) (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+)", input_data)
                        if input_pick:
                            RequestService.pick(
                                self.watch_monitor, input_pick, self.campaign, self.token)
                        else:
                            self.watch_monitor.enqueue("Error pick")
                    elif data[0] == "arrived":
                        input_arrived = re.search(
                            "arrived (?P<req_id>[a-zA-Z0-9\-]*) (?P<ma_id>[a-zA-Z0-9\-]*)", input_data)
                        if input_arrived:
                            RequestService.arrived(
                                self.watch_monitor, input_arrived, self.campaign)
                        else:
                            self.watch_monitor.enqueue("Error arrived")
                    elif data[0] == "search_item":
                        input_searchItem = re.search(
                            "search_item (?P<name>[a-zA-Z0-9]*)", input_data)
                        if input_searchItem:
                            ItemService.search_item(
                                self.watch_monitor, input_searchItem)
                        else:
                            self.watch_monitor.enqueue("Error search_item")
                        print(f"{self.address} tried to search an item")
                    elif data[0] == "update_item":
                        input_updateItem = re.search(
                            "update_item (?P<target>[a-zA-Z0-9]*) (?P<name>[a-zA-Z0-9]*)( )?(?P<synonyms>(.*)*)", input_data)
                        print(input_updateItem)
                        if input_updateItem:
                            ItemService.update_item(
                                self.watch_monitor, input_updateItem)
                        else:
                            self.watch_monitor.enqueue("Error update_item")
                    elif data[0] == "remove_item":
                        input_removeItem = re.search(
                            "remove_item (?P<name>[a-zA-Z0-9]*)", input_data)
                        if input_removeItem:
                            ItemService.remove_item(
                                self.watch_monitor, input_removeItem)
                        else:
                            self.watch_monitor.enqueue("Error remove_item")
                    else:
                        self.watch_monitor.enqueue("Invalid command")
                        print(
                            f"{self.address} tried to execute an invalid command")
                else:
                    if data[0] == "login":
                        input_login = re.search(
                            "login (?P<username>[a-zA-Z0-9]*) (?P<password>[a-zA-Z0-9]*)", input_data)
                        self.token = ServerParser.login(
                            self.watch_monitor, input_login)
                    else:
                        self.watch_monitor.enqueue(
                            "You should be logged in to execute a command.")
                    print(f"{self.address} tried to login")
            except Exception as e:
                print(f"Error: {e}")
                break

        self.watch_monitor.enqueue("##EOF##")
        print(f"Connection from {self.address} closed.")
        if self.token:
            ServerParser.logout(self.watch_monitor, self.token)
            self.token = None
        self.client_socket.close()


if __name__ == "__main__":
    # Example users
    user = User("bob", "bob@localhost", "Bob", "123")
    user2 = User("ken", "ken@localhost", "Ken", "123")
    user3 = User("ros", "ros@localhost", "Ros", "123")

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
        new_thread = ClientThread(client_socket, address)
        new_thread.start()
