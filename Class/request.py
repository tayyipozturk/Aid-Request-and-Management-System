import uuid
from datetime import datetime

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
            self.items_dict.append({"item": item, "availibility": None, "onroute": None})
        self.geoloc = geoloc
        self.urgency = urgency
        self.comments = comments
        self.status = 'OPEN'
        Request.collection.append(self)
    
    def get(self):
        itemstext = ["{\"item\": "+x["item"]["data"].get()+",\"amount\": "+str(x["item"]["amount"])+"}" for x in self.items_dict]
        geoloctext = "["+str(self.geoloc[0])+","+str(self.geoloc[1])+"]"
        return '{"owner":"' + self.owner + '","items":"' + ",".join(itemstext) + '","geoloc":"' + geoloctext + '","urgency":"' + self.urgency + '","comments":"' + self.comments + '"}'

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
                        newlist.append({"item": itemi, "availibility": itemj["availibility"], "onroute": itemj["onroute"]})
                        added = True
                        break
                if added == False:
                    newlist.append({"item": itemi, "availibility": None, "onroute": None})
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
        ma_id = uuid.uuid4()

        for i, itemi in enumerate(items):
            for j, itemj in enumerate(self.items_dict):
                if itemj["item"]["data"] == itemi["data"]:
                    if itemj["availibility"] is None or itemj["availibility"]["expire"] < datetime.now():
                        self.items_dict[j]["availibility"] = {"ma_id": ma_id,"amount": itemi["amount"], "supplier": user, "expire": expire, "geoloc": geoloc, "comments": comments}
                    break

        return ma_id
    
    def pick(self,itemid,items):
        # Start delivery for every item in items
        # Create a new onroute for deliveries. 
        # If the amount of availibility is less than the amount of request, use the amount of availibility and vice versa
        for i, itemi in enumerate(items):
            for j, itemj in enumerate(self.items_dict):
                if itemj["item"]['data'] == itemi["data"]:
                    if itemj["availibility"] is not None and itemj["availibility"]["ma_id"] == itemid:
                        if itemj["availibility"]["amount"] >= itemi["amount"]:
                            self.items_dict[j]["onroute"] = {"ma_id": itemid,"amount": itemi["amount"], "supplier": itemj["availibility"]["supplier"], "expire": itemj["availibility"]["expire"], "geoloc": itemj["availibility"]["geoloc"], "comments": itemj["availibility"]["comments"]}
                        elif itemj["availibility"]["amount"] < itemi["amount"]:
                            self.items_dict[j]["onroute"] = {"ma_id": itemid,"amount": itemj["availibility"]["amount"], "supplier": itemj["availibility"]["supplier"], "expire": itemj["availibility"]["expire"], "geoloc": itemj["availibility"]["geoloc"], "comments": itemj["availibility"]["comments"]}
                        self.items_dict[j]["availibility"] = None
                    break

        # Delete the availibility of given itemid
        for i, item in enumerate(self.items_dict):
            if self.items_dict[i]["availibility"] is not None and self.items_dict[i]["availibility"]["ma_id"] == itemid:
                self.items_dict[i]["availibility"] = None
                break

    def arrived(self, itemid):
        # Delete the onroute of given itemid
        # If there is no onroute, change the status to CLOSED
        for i, item in enumerate(self.items_dict):
            if self.items_dict[i]["onroute"]["ma_id"] == itemid:
                self.items_dict[i]["onroute"] = None
                break

        is_onroute = False
        for item in self.items_dict:
            if item["onroute"] != None:
                is_onroute = True
        if is_onroute == False:
            self.status = 'CLOSED'