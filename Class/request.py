class Request:
    def __init__(self, owner, items, geoloc, urgency, comments):
        self.owner = owner
        self.items = items
        self.geoloc = geoloc
        self.urgency = urgency
        self.comments = comments
        self.status = 'pending'
    
    def get(self):
        return '{"owner":"' + self.owner + '","items":"' + self.items + '","geoloc":"' + self.geoloc + '","urgency":"' + self.urgency + '","comments":"' + self.comments + '","status":"' + self.status + '"}'
    
    def update(self, owner, items, geoloc, urgency, comments):
        self.owner = owner
        self.items = items
        self.geoloc = geoloc
        self.urgency = urgency
        self.comments = comments

    def delete(self):
        self.owner = None
        self.items = None
        self.geoloc = None
        self.urgency = None
        self.comments = None
        self.status = None

    def markavailable(self):
        self.status = 'available'
    
    def pick(self):
        self.status = 'picked'

    def arrived(self):
        self.status = 'arrived'
