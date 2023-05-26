from Service.server_main_service import mutex, new_cond
from Class.user import User
from Class.request import Request
from Class.item import Item
import re
import uuid


class CampaignService:
    @staticmethod
    def add_request(monitor, args, campaign, token):
        item_list = re.findall("([a-zA-Z0-9]+) ([0-9]+)", args.group("items"))
        latitude = float(args.group("latitude"))
        longtitude = float(args.group("longtitude"))
        urgency = args.group("urgency")
        comments = args.group("descr")
        items = []
        geoloc = [longtitude, latitude]

        for it in item_list:
            item = it
            item_test = Item.search(item[0])
            if item_test is None:
                item_test = Item.search(item[0])
            items.append({"data": item_test, "amount": int(item[1])})
        username = User.find_one(token=token).username
        request = Request(username, items, geoloc, urgency, comments)
        with campaign.mutex:
            req_id = campaign.addrequest(request, token)
            monitor.enqueue(f"Request added successfully: {req_id}")

    @staticmethod
    def get_all_requests(monitor, campaign):
        with campaign.mutex:
            requests = campaign.get_all_requests()
            if requests != "":
                monitor.enqueue(requests)
            else:
                monitor.enqueue("No requests found")

    @staticmethod
    def get_request(monitor, args, campaign):
        id = args.group("id")
        with campaign.mutex:
            request = campaign.getrequest(id)
            if request != None:
                monitor.enqueue(request)
            else:
                monitor.enqueue("Request not found")

    @staticmethod
    def update_request(monitor, args, campaign, token):
        items_list = re.findall("([a-zA-Z0-9]+) ([0-9]+)", args.group("items"))
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
        with campaign.mutex:
            campaign.updaterequest(req_id, request)
            monitor.enqueue(f"Request updated successfully: {req_id}")

    def remove_request(monitor, args, campaign):
        id = args.group("id")
        id = uuid.UUID(id)
        with campaign.mutex:
            campaign.removerequest(id)
            monitor.enqueue(f"Request removed successfully: {id}")

    def query(monitor, args, campaign, type):
        item_list = re.findall("([a-zA-Z0-9]+)", args.group("items"))
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

        returnList = None
        with campaign.mutex:
            returnList = campaign.query(items, geoloc, urgency)

        result = ""
        if returnList is not None:
            for request in returnList:
                result += str(request.get()) + "\n"
        else:
            monitor.enqueue("No requests found")
        return

    def watch(monitor, args, campaign, type):
        item_list = re.findall("([a-zA-Z0-9]+)", args.group("items"))
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

        with campaign.mutex:
            watchid = campaign.watch(monitor.enqueue, items, geoloc, urgency)
        if watchid is None:
            monitor.enqueue("Error: Watch not added")
        else:
            monitor.enqueue(f"Watch added successfully: {watchid}")
        return watchid

    def unwatch(monitor, watchid, campaign):
        result = None
        with campaign.mutex:
            result = campaign.unwatch(watchid)
        if result:
            monitor.enqueue(f"Watch removed successfully: {watchid}")
        else:
            monitor.enqueue("Error: Watch not removed")
        return
