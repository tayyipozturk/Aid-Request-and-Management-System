import threading


class Item:
    collection = []
    mutex = threading.Lock()

    def __init__(self, name, synonyms=[]):
        self.name = name
        self.synonyms = synonyms        # List of synonyms
        self.mutex = threading.Lock()
        Item.collection.append(self)

    def get(self):
        # Return item as json
        with self.mutex:
            return '{"name":"' + self.name + '","synonyms":"' + str(self.synonyms) + '"}'

    def update(self, name=None, synonyms=None):
        # Update item with new values
        with self.mutex:
            if name is not None:
                self.name = name
            if synonyms is not None:
                self.synonyms = synonyms

    def delete(self):
        # Remove item from collection
        # Delete item
        with Item.mutex:
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

    @staticmethod
    def find_one(name=None):
        # Return item object
        # If item not found, return None
        for item in Item.collection:
            if name == item.name or name in item.synonyms:
                return item
        return None

    @staticmethod
    def find_all():
        return Item.collection
