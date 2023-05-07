import uuid
from datetime import datetime, timedelta
import threading

# "items" inputs are a list of following dictionary
# {
#  "data": Item,
#  "amount": Number
# }

# "self.owner" is a User object
# "self.geoloc" is [] of longitude and latitude
# "self.urgency" is a String that can be represented with corresponding enum
# "self.comments" is a String
# "self.items_dict" is a list of following dictionary
# {
#  "item":
#   {"data": Item, "amount": Number},
#  "availibility":
#   {"ma_id": Id,"amount": Number, "supplier": User, "expire": Date, "geoloc": geoloc, "comments": String},
#  "onroute":
#   {"ma_id": Id,"amount": Number, "supplier": User, "expire": Date, "geoloc": geoloc, "comments": String}
# }


class Request:
    collection = []

    def __init__(self, owner, items, geoloc, urgency, comments):
        self.owner = owner
        self.items_dict = []
        for item in items:
            self.items_dict.append(
                {"item": item, "availibility": None, "onroute": None, "delivered": False})
        self.geoloc = geoloc
        self.urgency = urgency
        self.comments = comments
        self.status = 'OPEN'
        self.mutex = threading.Lock()
        Request.collection.append(self)

    def get(self):
        itemstext = ["{\"item\": "+x["item"]["data"].get()+",\"amount\": "+str(
            x["item"]["amount"])+"}" for x in self.items_dict]
        availibilitytext = ["{\"ma_id\": "+str(x["availibility"]["ma_id"])+",\"item\": "+str(x["availibility"]["item"])+",\"amount\": "+str(x["availibility"]["amount"])+",\"supplier\": "+x["availibility"]["supplier"].username +
                            ",\"expire\": "+str(x["availibility"]["expire"])+",\"geoloc\": "+str(x["availibility"]["geoloc"])+",\"comments\": "+x["availibility"]["comments"]+"}" for x in self.items_dict if x["availibility"] is not None]
        onroutetext = ["{\"ma_id\": "+str(x["onroute"]["ma_id"])+",\"item\": "+str(x["onroute"]["item"])+",\"amount\": "+str(x["onroute"]["amount"])+",\"supplier\": "+x["onroute"]["supplier"].username +
                       ",\"expire\": "+str(x["onroute"]["expire"])+",\"geoloc\": "+str(x["onroute"]["geoloc"])+",\"comments\": "+x["onroute"]["comments"]+"}" for x in self.items_dict if x["onroute"] is not None]
        return '{"owner":"' + self.owner + '","items":"' + str(itemstext) + '","geoloc":"' + str(self.geoloc) + '","urgency":"' + self.urgency + '","comments":"' + self.comments + '","status":"' + self.status + '","availibility":"' + str(availibilitytext) + '","onroute":"' + str(onroutetext) + '"}'

    def update(self, owner=None, items=None, geoloc=None, urgency=None, comments=None):
        # Check if the new items are compatible with onroute
        if items is not None:
            for item in self.items_dict:
                if item["onroute"] != None:
                    is_in_new = False
                    for itemi in items:
                        if itemi["data"] == item["item"]["data"]:
                            is_in_new = True
                            if itemi["amount"] < item["onroute"]["amount"]:
                                return False
                    if is_in_new == False:
                        return False
            # If the new items are compatible with onroute
            # If new items exists in old items, use the old availibility and onroute
            # If not, add with availibility and onroute to None
            newlist = []
            for itemi in items:
                added = False
                for itemj in self.items_dict:
                    if itemi["data"] == itemj["item"]["data"]:
                        newlist.append(
                            {"item": itemi, "availibility": itemj["availibility"], "onroute": itemj["onroute"]})
                        added = True
                        break
                if added == False:
                    newlist.append(
                        {"item": itemi, "availibility": None, "onroute": None})
            self.items_dict = newlist

        if geoloc is not None:
            self.geoloc = geoloc
        if urgency is not None:
            self.urgency = urgency
        if comments is not None:
            self.comments = comments
        if owner is not None:
            self.owner = owner
        return True

    def delete(self):
        # Check if there is any delivery on route
        for item in self.items_dict:
            if item["onroute"] != None:
                print("Cannot delete request with items on route")
                return False
        Request.collection.remove(self)
        del self
        return True

    def markavailable(self, user, items, expire, geoloc, comments):
        # If there is no reserved availibility or the reserved availibility is expired, add a new availibility
        # Return unique ma_id
        ma_id = None

        for i, itemi in enumerate(items):
            for j, itemj in enumerate(self.items_dict):
                if itemj["item"]["data"] == itemi["data"]:
                    if itemj["availibility"] is None or itemj["availibility"]["expire"] < datetime.now():
                        ma_id = uuid.uuid4()
                        self.items_dict[j]["availibility"] = {"ma_id": ma_id, "item": itemi["data"].name, "amount": itemi["amount"], "supplier": user, "expire": (
                            datetime.now() + timedelta(hours=int(expire))), "geoloc": geoloc, "comments": comments}
                    break
        return ma_id

    def pick(self, itemid, items):
        # Start delivery for every item in items
        # Create a new onroute for deliveries.
        # If the amount of availibility is less than the amount of request, use the amount of availibility and vice versa
        for i, itemi in enumerate(items):
            for j, itemj in enumerate(self.items_dict):
                if itemj["item"]['data'] == itemi["data"]:
                    if itemj["availibility"] is not None and itemj["availibility"]["ma_id"] == itemid and itemj["availibility"]["expire"] > datetime.now():
                        self.items_dict[j]["onroute"] = {"ma_id": itemid, "item": itemi["data"].name, "amount": min(itemj["item"]["amount"], itemj["availibility"]["amount"], itemi["amount"]), "supplier": itemj[
                            "availibility"]["supplier"], "expire": itemj["availibility"]["expire"], "geoloc": itemj["availibility"]["geoloc"], "comments": itemj["availibility"]["comments"]}
                    break

        # Delete the availibility of given itemid
        for i, item in enumerate(self.items_dict):
            if self.items_dict[i]["availibility"] is not None and self.items_dict[i]["availibility"]["ma_id"] == itemid:
                self.items_dict[i]["availibility"] = None
                continue

    def arrived(self, itemid):
        # Delete the onroute of given itemid
        # If there is no onroute, change the status to CLOSED
        for i, item in enumerate(self.items_dict):
            if self.items_dict[i]["onroute"]["ma_id"] == itemid:
                item["item"]["amount"] -= item["onroute"]["amount"]
                if item["item"]["amount"] == 0:
                    item["delivered"] = True
                self.items_dict[i]["onroute"] = None
                break

        is_onroute = False
        for item in self.items_dict:
            if item["onroute"] != None:
                is_onroute = True
        if is_onroute == False:
            self.status = 'CLOSED'
