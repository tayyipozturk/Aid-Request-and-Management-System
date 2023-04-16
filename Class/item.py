class Item:
    collection = []

    def __init__(self, name, synonyms=[]):
        self.name = name
        self.synonyms = synonyms        # List of synonyms
        Item.collection.append(self)

    def get(self):
        # Return item as json
        synonymtxt = ",".join(self.synonyms)
        return '{"name":"' + self.name + '","synonyms":"' + synonymtxt + '"}'
    
    def update(self, name=None, synonyms=None):
        # Update item with new values
        if name is not None:
            self.name = name
        if synonyms is not None:
            self.synonyms = synonyms

    def delete(self):
        # Remove item from collection
        # Delete item
        Item.collection.remove(self)
        del self

    @staticmethod
    def search(name):
        # Search item in collection and return item object
        # If item not found, create new item and return None
        for item in Item.collection:
            if name == item.name or name in item.synonyms:
                return item
        newItem = Item(name)
        return None