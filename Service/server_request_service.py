import re
from Class.item import Item
from Class.user import User
from Class.request import Request
import uuid


class RequestService:
    def mark_available(monitor, args, campaign, token):
        item_list = re.findall("([a-zA-Z0-9]+) ([0-9]+)", args.group("items"))
        expire = int(args.group("expire"))
        latitude = float(args.group("latitude"))
        longtitude = float(args.group("longtitude"))
        comments = args.group("comment")
        id = args.group("id")
        ma_id = None

        user = User.find_one(token=token)
        items = []
        geoloc = [latitude,longtitude]

        for it in item_list:
            item = it
            item_test = Item.search(item[0])
            if item_test is None:
                item_test = Item.search(item[0])
            items.append({"data": item_test, "amount": int(item[1])})

        request = campaign.findrequest(id)
        if request is None:
            monitor.enqueue("Request not found")
            return None
        with request["data"].mutex:
            ma_id = request["data"].markavailable(
                user, items, expire, geoloc, comments)
        if ma_id is not None:
            monitor.enqueue(f"Marked available successfully: {ma_id}")
        else:
            monitor.enqueue("Marked available failed")
        return ma_id

    def pick(monitor, args, campaign, token):
        item_list = re.findall("([a-zA-Z0-9]+) ([0-9]+)", args.group("items"))
        req_id = args.group("req_id")
        ma_id = args.group("ma_id")
        ma_id = uuid.UUID(ma_id)
        items = []

        request = campaign.findrequest(req_id)
        if request is None:
            monitor.enqueue("Request not found")
            return None

        for it in item_list:
            item = it
            item_test = Item.search(item[0])
            if item_test is None:
                item_test = Item.search(item[0])
            items.append({"data": item_test, "amount": int(item[1])})

        try:
            with request["data"].mutex:
                request["data"].pick(ma_id, items)
        except:
            monitor.enqueue("Picked failed")
            return

        monitor.enqueue("Picked successfully")
        return

    def arrived(monitor, args, campaign):
        req_id = args.group("req_id")
        ma_id = args.group("ma_id")
        ma_id = uuid.UUID(ma_id)
        request = campaign.findrequest(req_id)
        if request is None:
            monitor.enqueue("Request not found")
            return None
        try:
            with request["data"].mutex:
                request["data"].arrived(ma_id)
        except:
            monitor.enqueue("Arrived failed")
            return
        monitor.enqueue("Arrived successfully")
        return
