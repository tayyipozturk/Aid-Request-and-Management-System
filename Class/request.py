from item import Item

class Request:
    collection = []

    def __init__(self, owner, items, geoloc, urgency, comments):
        self.owner = owner
        self.items = items
        self.geoloc = geoloc
        self.urgency = urgency
        self.comments = comments
        self.status = 'pending'
        Request.collection.append(self)
    
    def get(self):
        return '{"owner":"' + self.owner + '","items":"' + self.items + '","geoloc":"' + self.geoloc + '","urgency":"' + self.urgency + '","comments":"' + self.comments + '"}'
    
    def update(self, owner, items, geoloc, urgency, comments):
        self.owner = owner
        self.items = items
        self.geoloc = geoloc
        self.urgency = urgency
        self.comments = comments

    def delete(self):
        Request.collection.remove(self)
        del self

    def markavailable(self, user, items, expire, geloc, comments):
        for item in items:
            collection = Item.collection
            for i in collection:
                if item.name == i.name or item.name in i.synonyms and i.name == user:
                    i.status = 'reserved'
    
    def pick(self):
        self.status = 'picked'

    def arrived(self):
        self.status = 'arrived'
