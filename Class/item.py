class Item:
    collection = []

    def __init__(self, name, seller, synonyms=[]):
        self.name = name
        self.seller = seller
        self.synonyms = synonyms
        self.status = "available"
        Item.collection.append(self)

    def get(self):
        return '{"name":"' + self.name + '","synonyms":"' + self.synonyms + '" ,"seller":"' + self.seller + '" ,"status":"' + self.status + '"}'
    
    def update(self, name, synonyms, seller):
        self.name = name
        self.synonyms = synonyms
        self.seller = seller

    def delete(self):
        Item.collection.remove(self)
        del self

    @staticmethod
    def search(name):
        for item in Item.collection:
            if name == item.name or name in item.synonyms:
                return item.name
        Item.collection.append(Item(name))