from Service.server_main_service import mutex, new_cond
from Class.user import User
from Class.request import Request
from Class.item import Item
import re
import uuid


class CampaignService:
    @staticmethod
    def add_request(client, args, campaign, token):
        item_list = re.findall("([a-zA-Z0-9]+) ([0-9]+)", args.group("items"))
        num_items = args.group("n_items")
        latitude = float(args.group("latitude"))
        longtitude = float(args.group("longtitude"))
        urgency = args.group("urgency")
        comments = args.group("descr")
        items = []
        geoloc = [longtitude, latitude]

        with campaign.mutex:
            for it in item_list:
                item = it
                item_test = Item.search(item[0])
                if item_test is None:
                    item_test = Item.search(item[0])
                items.append({"data": item_test, "amount": int(item[1])})
        username = User.find_one(token=token).username
        request = Request(username, items, geoloc, urgency, comments)
        with campaign.mutex:
            req_id = campaign.addrequest(request)
            client.sendall(f"Request added successfully: {req_id}".encode())

    @staticmethod
    def get_request(client, args, campaign):
        print(args.groupdict())
        id = args.group("id")
        with campaign.mutex:
            request = campaign.getrequest(id)
            if request != None:
                client.sendall(request.encode())
            else:
                client.sendall("Request not found".encode())

    @staticmethod
    def update_request(client, args, campaign, token):
        items_list = re.findall("([a-zA-Z0-9]+) ([0-9]+)", args.group("items"))
        num_items = args.group("n_items")
        latitude = float(args.group("latitude"))
        longtitude = float(args.group("longtitude"))
        urgency = args.group("urgency")
        comments = args.group("descr")
        req_id = args.group("req_id")
        items = []
        geoloc = [longtitude, latitude]
        with campaign.mutex:
            for item in items_list:
                item_test = Item.search(item[0])
                if item_test is None:
                    item_test = Item.search(item[0])
                items.append({"data": item_test, "amount": int(item[1])})
        username = User.find_one(token=token).username
        request = Request(username, items, geoloc, urgency, comments)
        print(request.items_dict)
        print(request)
        with campaign.mutex:
            campaign.updaterequest(req_id, request)
            client.sendall(f"Request updated successfully: {req_id}".encode())

    def remove_request(client, args, campaign):
        id = args.group("id")
        with campaign.mutex:
            campaign.removerequest(id)
            client.sendall(f"Request removed successfully: {id}".encode())

    def query(client, args, campaign, type):
        item_list = re.findall("([a-zA-Z0-9]+)", args.group("items"))
        num_items = args.group("n_items")
        urgency = args.group("urgency")

        items = []
        for it in item_list:
            found_item = Item.search(it)
            if found_item is None:
                found_item = Item.search(it)
            items.append(found_item)

        if type == "rect":
            latitude1 = float(args.group("latitude1"))
            longtitude1 = float(args.group("longtitude1"))
            latitude2 = float(args.group("latitude2"))
            longtitude2 = float(args.group("longtitude2"))
            corner1 = [longtitude1, latitude1]
            corner2 = [longtitude2, latitude2]
            geoloc = {'type': 0, 'values': [corner1, corner2]}
        elif type == "circ":
            latitude = float(args.group("latitude"))
            longtitude = float(args.group("longtitude"))
            radius = float(args.group("radius"))
            center = [longtitude, latitude]
            geoloc = {'type': 1, 'values': [center, radius]}

        returnList = campaign.query(items, geoloc, urgency)

        for request in returnList:
            client.sendall(request.get().encode())
        return

    def watch(client, args, campaign, type):
        item_list = re.findall("([a-zA-Z0-9]+)", args.group("items"))
        num_items = args.group("n_items")
        urgency = args.group("urgency")
        watchid = None

        items = []
        for it in item_list:
            found_item = Item.search(it)
            if found_item is None:
                found_item = Item.search(it)
            items.append(found_item)

        if type == "rect":
            latitude1 = float(args.group("latitude1"))
            longtitude1 = float(args.group("longtitude1"))
            latitude2 = float(args.group("latitude2"))
            longtitude2 = float(args.group("longtitude2"))
            corner1 = [longtitude1, latitude1]
            corner2 = [longtitude2, latitude2]
            geoloc = {'type': 0, 'values': [corner1, corner2]}
        elif type == "circ":
            latitude = float(args.group("latitude"))
            longtitude = float(args.group("longtitude"))
            radius = float(args.group("radius"))
            center = [longtitude, latitude]
            geoloc = {'type': 1, 'values': [center, radius]}

        watchid = campaign.watch(client.sendall, items, geoloc, urgency)
        if watchid is None:
            client.sendall("Error: Watch not added".encode())
        else:
            client.sendall(f"Watch added successfully: {watchid}".encode())
        return watchid

    def unwatch(client, args, campaign):
        watchid = args.group("watchid")
        if campaign.unwatch(watchid):
            client.sendall(f"Watch removed successfully: {watchid}".encode())
        else:
            client.sendall("Error: Watch not removed".encode())
        return
