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


# login username password
# <token> new campaign_name campaign_descr
# <token> list
# <token> open campaign_name
# <token> close
# <token> add_request <items>(<name> <amount>) <latitude> <longtitude> <urgency> <descr>
# <token> get_all_requests
# <token> get_request <id>
# <token> update_request <id> <items>(<name> <amount>) <latitude> <longtitude> <urgency> <descr>
# <token> delete_request <id>
# <token> add_item <name> <descr>
# <token> get_all_items
# <token> get_item <name>
# <token> update_item <name> <descr>
# <token> delete_item <name>

userList = []
class ClientThread(threading.Thread):
    def __init__(self, client_socket, address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.address = address
        print(f"New connection from {self.address}")

    def run(self):
        while True:
            try:
                input_data = self.client_socket.recv(2048).decode()
                data = input_data.split()
                
                if data == []:
                    continue
                if data[0] == "login":
                    username = data[1]
                    password = data[2]
                    token = None
                    watch_monitor = WatchMonitor(client_socket)
                    watch_monitor.run()
                    if len(username) > 0 and len(password) > 0:
                        token = User.login(username, password)
                        if token:
                            watch_monitor.enqueue(f"Login successful. Token: {token}")
                        else:
                            watch_monitor.enqueue("Login failed")
                            continue

                    logged = {"username": username, "token": token, "campaign": None,
                              "watches": [], "watch_monitor": watch_monitor}
                    userList.append(logged)
                    print(f"{username} logged in")
                else:
                    token = data[0]
                    index = self.find_user(token)
                    targetUser = userList[index]
                    if data[1] == "new":
                        input_new = re.search(
                            "(?P<token>[a-zA-Z0-9]*) new (?P<name>[a-zA-Z0-9]*) (?P<descr>(.*)*)", input_data)
                        ServerParser.new(targetUser['watch_monitor'], input_new)
                        print(f"{targetUser['username']} tried to create a new campaign")
                    elif data[1] == "list":
                        ServerParser.list(targetUser['watch_monitor'], data)
                        print(f"{targetUser['username']} tried to list campaigns")
                    elif data[1] == "open":
                        if not targetUser['campaign']:
                            input_open = re.search(
                                "(?P<token>[a-zA-Z0-9]*) open (?P<name>[a-zA-Z0-9]*)", input_data)
                            if input_open:
                                campaign = ServerParser.open(
                                    targetUser['watch_monitor'], input_open)
                                if campaign:
                                    targetUser['campaign'] = campaign
                                    targetUser['watch_monitor'].enqueue(
                                        "Campaign opened")
                                else:
                                    targetUser['watch_monitor'].enqueue(
                                        "Campaign not found")
                        else:
                            targetUser['watch_monitor'].enqueue(
                                "You already have a campaign opened")
                        print(f"{targetUser['username']} tried to open a campaign")
                    elif data[1] == "close":
                        if targetUser['campaign']:
                            if ServerParser.close(
                                    targetUser['watch_monitor'], data, targetUser['campaign'], targetUser['watches']):
                                targetUser['campaign'] = None
                                targetUser['watches'] = []
                                targetUser['watch_monitor'].enqueue(
                                    "Campaign closed")
                            else:
                                targetUser['watch_monitor'].enqueue(
                                    "Error closing campaign")
                        else:
                            targetUser['watch_monitor'].enqueue(
                                "No campaign opened")
                        print(f"{targetUser['username']} tried to close a campaign")
                    elif data[1] == "add_request":
                        if targetUser['campaign']:
                            # add_request <items>(<name> <amount>) <latitude> <longtitude> <urgency> <descr>
                            input_addRequest = re.search(
                                "(?P<token>[a-zA-Z0-9]*) add_request (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+) (?P<latitude>[0-9\.]*) (?P<longtitude>[0-9\.]*) (?P<urgency>[a-zA-Z]*) (?P<descr>(.*)*)",
                                input_data)

                            if input_addRequest:
                                CampaignService.add_request(
                                    targetUser['watch_monitor'], input_addRequest, targetUser['campaign'], targetUser['token'])
                            else:
                                targetUser['watch_monitor'].enqueue(
                                    "Error")
                        else:
                            targetUser['watch_monitor'].enqueue(
                                "No campaign opened")
                        print(f"{targetUser['username']} tried to add a request")

                    elif data[1] == "get_all_requests":
                        if targetUser['campaign']:
                            CampaignService.get_all_requests(
                                targetUser['watch_monitor'], targetUser['campaign'])
                        else:
                            targetUser['watch_monitor'].enqueue(
                                "No campaign opened")
                        print(f"{targetUser['username']} tried to get all requests")
                    elif data[1] == "get_request":
                        input_getRequest = re.search(
                            "(?P<token>[a-zA-Z0-9]*) get_request (?P<id>[a-zA-Z0-9\-]*)", input_data)
                        if input_getRequest:
                            CampaignService.get_request(
                                targetUser['watch_monitor'], input_getRequest, targetUser['campaign'])
                        else:
                            targetUser['watch_monitor'].enqueue(
                                "Error")
                    elif data[1] == "update_request":
                        input_updateRequest = re.search(
                            "(?P<token>[a-zA-Z0-9]*) update_request (?P<req_id>[a-zA-Z0-9\-]*) (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+) (?P<latitude>[0-9\.]*) (?P<longtitude>[0-9\.]*) (?P<urgency>[a-zA-Z]*) (?P<descr>(.*)*)",
                            input_data)
                        if input_updateRequest:
                            try:
                                CampaignService.update_request(
                                    targetUser['watch_monitor'], input_updateRequest, targetUser['campaign'], targetUser['token'])
                            except:
                                targetUser['watch_monitor'].enqueue(
                                    "Error updating request")
                        else:
                            targetUser['watch_monitor'].enqueue(
                                "Error updating request")
                    elif data[1] == "remove_request":
                        input_removeRequest = re.search(
                            "(?P<token>[a-zA-Z0-9]*) remove_request (?P<id>[a-zA-Z0-9\-]*)", input_data)
                        if input_removeRequest:
                            CampaignService.remove_request(
                                targetUser['watch_monitor'], input_removeRequest, targetUser['campaign'])
                        else:
                            targetUser['watch_monitor'].enqueue(
                                "Error")

                    elif data[1] == "query":
                        # items, rectangular, (latitude, longtitude), (latitude, longtitude), urgency
                        arg = {}
                        item_count = data[2]
                        items = []
                        for t in range(int(item_count)):
                            items.append(data[3 + t])
                        queryType = int(data[3 + int(item_count)])

                        if queryType == 0:
                            latitude1 = data[4 + int(item_count)]
                            longitude1 = data[5 + int(item_count)]
                            latitude2 = data[6 + int(item_count)]
                            longitude2 = data[7 + int(item_count)]
                            urgency = data[8 + int(item_count)]
                            arg = {'items': items, 'latitude1': latitude1, 'longitude1': longitude1,
                                      'latitude2': latitude2, 'longitude2': longitude2, 'urgency': urgency}
                            CampaignService.query(
                                targetUser['watch_monitor'], arg, targetUser['campaign'], "rect")
                        elif queryType == 1:
                            latitude = data[4 + int(item_count)]
                            longitude = data[5 + int(item_count)]
                            radius = data[6 + int(item_count)]
                            urgency = data[7 + int(item_count)]
                            arg = {'items': items, 'latitude': latitude, 'longitude': longitude,
                                        'radius': radius, 'urgency': urgency}
                            CampaignService.query(
                                targetUser['watch_monitor'], arg, targetUser['campaign'], "circ")
                        else:
                            targetUser['watch_monitor'].enqueue("Error query")
                    elif data[1] == "watch":
                        # items, rectangular, (latitude, longtitude), (latitude, longtitude), urgency
                        arg = {}
                        item_count = data[2]
                        items = []
                        for t in range(int(item_count)):
                            items.append(data[3 + t])
                        watchType = int(data[3 + int(item_count)])

                        if watchType == 0:
                            latitude1 = data[4 + int(item_count)]
                            longitude1 = data[5 + int(item_count)]
                            latitude2 = data[6 + int(item_count)]
                            longitude2 = data[7 + int(item_count)]
                            urgency = data[8 + int(item_count)]
                            arg = {'items': items, 'latitude1': latitude1, 'longitude1': longitude1,
                                   'latitude2': latitude2, 'longitude2': longitude2, 'urgency': urgency}
                            watch_id = CampaignService.watch(
                                targetUser['watch_monitor'], arg, targetUser['campaign'], "rect")
                            targetUser['watches'].append(watch_id)
                        elif watchType == 1:
                            latitude = data[4 + int(item_count)]
                            longitude = data[5 + int(item_count)]
                            radius = data[6 + int(item_count)]
                            urgency = data[7 + int(item_count)]
                            arg = {'items': items, 'latitude': latitude, 'longitude': longitude,
                                   'radius': radius, 'urgency': urgency}
                            watch_id = CampaignService.watch(
                                targetUser['watch_monitor'], arg, targetUser['campaign'], "circ")
                            targetUser['watches'].append(watch_id)
                        else:
                            targetUser['watch_monitor'].enqueue("Error watch")
                    elif data[1] == "unwatch":
                        input_unwatch = re.search(
                            "(?P<token>[a-zA-Z0-9]*) unwatch (?P<id>[a-zA-Z0-9\-]*)", input_data)
                        if input_unwatch:
                            id_uuid = uuid.UUID(input_unwatch.group("id"))
                            if id_uuid in targetUser['watches']:
                                CampaignService.unwatch(
                                    targetUser['watch_monitor'], id_uuid, targetUser['campaign'])
                                targetUser['watches'].remove(id_uuid)
                        else:
                            targetUser['watch_monitor'].enqueue("Error unwatch")
                    elif data[1] == "mark_available":
                        input_markAvailable = re.search(
                            "(?P<token>[a-zA-Z0-9]*) mark_available (?P<id>[a-zA-Z0-9\-]*) (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+) (?P<expire>[0-9]*) (?P<latitude>[0-9\.]*) (?P<longtitude>[0-9\.]*) (?P<comment>(.*)*)",
                            input_data)
                        if input_markAvailable:
                            RequestService.mark_available(
                                targetUser['watch_monitor'], input_markAvailable, targetUser['campaign'], targetUser['token'])
                        else:
                            targetUser['watch_monitor'].enqueue("Error mark_available")
                    elif data[1] == "pick":
                        input_pick = re.search(
                            "(?P<token>[a-zA-Z0-9]*) pick (?P<req_id>[a-zA-Z0-9\-]*) (?P<ma_id>[a-zA-Z0-9\-]*) (?P<items>(([a-zA-Z0-9]*) ([0-9]*))+)",
                            input_data)
                        if input_pick:
                            RequestService.pick(
                                targetUser['watch_monitor'], input_pick, targetUser['campaign'], targetUser['token'])
                        else:
                            targetUser['watch_monitor'].enqueue("Error pick")
                    elif data[1] == "arrived":
                        input_arrived = re.search(
                            "(?P<token>[a-zA-Z0-9]*) arrived (?P<req_id>[a-zA-Z0-9\-]*) (?P<ma_id>[a-zA-Z0-9\-]*)", input_data)
                        if input_arrived:
                            RequestService.arrived(
                                targetUser['watch_monitor'], input_arrived, targetUser['campaign'])
                        else:
                            targetUser['watch_monitor'].enqueue("Error arrived")
                    elif data[1] == "search_item":
                        input_searchItem = re.search(
                            "(?P<token>[a-zA-Z0-9]*) search_item (?P<name>[a-zA-Z0-9]*)", input_data)
                        if input_searchItem:
                            ItemService.search_item(
                                targetUser['watch_monitor'], input_searchItem)
                        else:
                            targetUser['watch_monitor'].enqueue("Error search_item")
                        print(f"{targetUser['username']} tried to search an item")
                    elif data[1] == "update_item":
                        input_updateItem = re.search(
                            "(?P<token>[a-zA-Z0-9]*) update_item (?P<target>[a-zA-Z0-9]*) (?P<name>[a-zA-Z0-9]*) (?P<synonyms>(.*)*)",
                            input_data)
                        print(input_updateItem)
                        if input_updateItem:
                            ItemService.update_item(
                                targetUser['watch_monitor'], input_updateItem)
                        else:
                            targetUser['watch_monitor'].enqueue("Error update_item")
                    elif data[1] == "remove_item":
                        input_removeItem = re.search(
                            "(?P<token>[a-zA-Z0-9]*) remove_item (?P<name>[a-zA-Z0-9]*)", input_data)
                        if input_removeItem:
                            ItemService.remove_item(
                                targetUser['watch_monitor'], input_removeItem)
                        else:
                            targetUser['watch_monitor'].enqueue("Error remove_item")
                    elif data[1] == "logout":
                        target = User.find_one(token=token)
                        target.logout()
                        targetUser['watch_monitor'].enqueue("Logout successful")
                        userList.pop(index)
                    else:
                        targetUser['watch_monitor'].enqueue("Invalid command")
                        print(
                            f"{targetUser['username']} tried to execute an invalid command")
            except Exception as e:
                print(f"Error: {e}")
                # break

        # self.watch_monitor.enqueue("##EOF##")
        # print(f"Connection from {self.address} closed.")
        # if self.token:
        #     ServerParser.logout(self.watch_monitor, self.token)
        #     self.token = None
        # self.client_socket.close()

    def find_user(self, token):
        index = 0
        for element in userList:
            if element["token"] == token:
                return index
            index += 1
        return None


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
