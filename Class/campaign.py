import uuid
from Enum.urgency import Urgency
import threading

# "self.name" is a String
# "self.description" is a String
# "self.requests" is a list of {"req_id": req_id, "data": request}
# "self.watches" is a list of {"watch_id": watch_id, "callback": callback, "item": item, "loc": loc, "urgency": urgency, "token": token}


class Campaign:
    collection = []

    def __init__(self, name, description):
        # check if name is unique
        for campaign in Campaign.collection:
            if campaign.name == name:
                print("Campaign name already exists.")
                return
        self.name = name
        self.description = description
        self.requests = []
        self.watches = []
        Campaign.collection.append(self)
        self.mutex = threading.Lock()

    def addrequest(self, request, token):
        # request is a Request object
        # return the req_id
        req_id = uuid.uuid4()
        req_dict = {"req_id": req_id, "data": request}
        self.requests.append(req_dict)
        # Check if the request matches any watch
        # If it does, call the callback
        # For algorithm, see query function
        for watch in self.watches:
            if watch["item"] is None and watch["loc"] is None and watch['urgency'] is None:
                watch["callback"]()
            else:
                is_okay = True
                if watch["item"] is not None:
                    item_exists = 0
                    for itemi in watch["item"]:
                        for itemj in request.items_dict:
                            if itemj["item"]["data"] == itemi:
                                item_exists += 1
                                break
                    if item_exists != len(watch["item"]):
                        is_okay = False
                if is_okay and watch["loc"] is not None:
                    # two geoloc and a rectangle
                    if watch["loc"]["type"] == 0:
                        geoloc0 = request.geoloc
                        target_geoloc0 = watch["loc"]['values'][0]
                        target_geoloc1 = watch["loc"]['values'][1]
                        # find if geloloc0 is in the rectangle
                        max_longtitude = max(
                            float(target_geoloc0[0]), float(target_geoloc1[0]))
                        max_latitude = max(
                            float(target_geoloc0[1]), float(target_geoloc1[1]))
                        min_longtitude = min(
                            float(target_geoloc0[0]), float(target_geoloc1[0]))
                        min_latitude = min(
                            float(target_geoloc0[1]), float(target_geoloc1[1]))
                        if float(geoloc0[0]) > max_longtitude or float(geoloc0[0]) < min_longtitude or float(geoloc0[1]) > max_latitude or float(geoloc0[1]) < min_latitude:
                            is_okay = False
                    elif watch["loc"]["type"] == 1:
                        if (request.geoloc[0] - watch["loc"]["values"][0][0])**2 + (request.geoloc[1] - watch["loc"]["values"][0][1])**2 > watch["loc"]["values"][1]**2:
                            is_okay = False
                if is_okay and watch['urgency'] is not None:
                    if Urgency[request.urgency].value > Urgency[watch['urgency']].value:
                        is_okay = False
                if is_okay:
                    if watch["callback"] is not None:
                        #'{"owner":"' + self.owner + '","items":' + str(itemstext) + ',"geoloc":' + str(self.geoloc) + ',"urgency":"' + self.urgency + '","comments":"' + self.comments + '","status":"' + self.status + '","availibility":' + str(availibilitytext) + ',"onroute":' + str(onroutetext) + '}'
                        watch_text = '{"token":"' + str(watch["token"]) + '","request":"' + str(req_id) + '","watchcalled": true}'
                        watch["callback"](watch_text)
                        #watch["callback"](f"WATCH MATCHED:\n{watch}\nTOKEN: {token}\n")

        return req_id

    def removerequest(self, requestid):
        # Try to delete request
        # Remove request from list if successful
        for i, request in enumerate(self.requests):
            if request["req_id"] == requestid:
                if request["data"].delete():
                    print("Request deleted.")
                    self.requests.pop(i)
                    return True
                else:
                    print("Request not deleted.")
                    return False
        print("Request not found.")
        return False

    def updaterequest(self, requestid, request):
        # Try to update request
        for req in self.requests:
            check_val = req["req_id"]
            if isinstance(requestid, str):
                check_val = str(check_val)
            if check_val == requestid:
                if req["data"].update(owner=request.owner, items=[x["item"] for x in request.items_dict], geoloc=request.geoloc, urgency=request.urgency, comments=request.comments):
                    print("Request updated.")
                    return True
                else:
                    print("Request not updated.")
                    return False
        print("Request not found.")
        return False

    def getrequest(self, requestid):
        # Try to get request and return it
        for request in self.requests:
            check_val = request["req_id"]
            if isinstance(requestid, str):
                check_val = str(check_val)
            if check_val == requestid:
                return request["data"].get()
        return None

    def query(self, item=None, loc=None, urgency=None):
        # item is a list of Item object
        # geoloc is [] of longitude and latitude
        # loc is {"type": Number, "values": []}. If type is 0, values consists two geoloc. If type is 1, values consists a geoloc and a radius.
        # urgency is a String

        # If all arguments are None, return all requests
        if item is None and loc is None and urgency is None:
            return [request["data"] for request in self.requests]
        else:
            returnList = []
            # Look for requests that match the query
            for request in self.requests:
                # Accept if all conditions are met
                # Check for if items don't match
                # Check for if geoloc don't match
                # If loc type is 0, check if requests geoloc is not in the rectangle
                # If loc type is 1, check if requests geoloc is not in the circle
                # Check for if urgency level is above
                # If we don't match any of these negative conditions, add to return list
                is_okay = True
                if item is not None:
                    item_exists = 0
                    for itemi in item:
                        for itemj in request["data"].items_dict:
                            if itemj["item"]["data"] == itemi:
                                item_exists += 1
                                break
                    if item_exists != len(item):
                        is_okay = False
                if is_okay and loc is not None:
                    if loc["type"] == 0:
                        geoloc0 = request['data'].geoloc
                        target_geoloc0 = loc['values'][0]
                        target_geoloc1 = loc['values'][1]
                        max_longtitude = max(
                            float(target_geoloc0[0]), float(target_geoloc1[0]))
                        max_latitude = max(
                            float(target_geoloc0[1]), float(target_geoloc1[1]))
                        min_longtitude = min(
                            float(target_geoloc0[0]), float(target_geoloc1[0]))
                        min_latitude = min(
                            float(target_geoloc0[1]), float(target_geoloc1[1]))
                        if float(geoloc0[0]) > max_longtitude or float(geoloc0[0]) < min_longtitude or float(geoloc0[1]) > max_latitude or float(geoloc0[1]) < min_latitude:
                            is_okay = False
                    elif loc["type"] == 1:
                        if (request["data"].geoloc[0] - loc["values"][0][0])**2 + (request["data"].geoloc[1] - loc["values"][0][1])**2 > loc["values"][1]**2:
                            is_okay = False
                if is_okay and urgency is not None:
                    if Urgency[request["data"].urgency].value > Urgency[urgency].value:
                        is_okay = False
                if is_okay:
                    returnList.append(request)
        return returnList

    def watch(self, callback=None, item=None, loc=None, urgency=None, token=None):
        # Add a watcher with callback function to the list
        # item is a list of Item object
        # Return the watch_id
        watch_id = uuid.uuid4()
        self.watches.append({"watch_id": watch_id, "callback": callback,
                            "item": item, "loc": loc, "urgency": urgency, "token": token})
        return watch_id

    def unwatch(self, watchid):
        # Remove given watcher from the list
        for i, watch in enumerate(self.watches):
            if watch["watch_id"] == watchid:
                self.watches.pop(i)
                return True
        return False

    def findrequest(self, req_id):
        # Return the request if it is in the list
        for req in self.requests:
            check_val = req["req_id"]
            if isinstance(req_id, str):
                check_val = str(check_val)
            if check_val == req_id:
                return req
        return None

    @staticmethod
    def find_one(name):
        for campaign in Campaign.collection:
            if campaign.name == name:
                return campaign
        return None

    def get_all_requests(self):
        requests = [request['req_id'] for request in self.requests]
        return "\n".join([str(request) for request in requests])
