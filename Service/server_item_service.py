from Service.server_main_service import mutex, new_cond
from Class.user import User
from Class.request import Request
from Class.item import Item


class ItemService:
    @staticmethod
    def search_item(monitor, args):
        name = args.group("name")
        item = Item.search(name)
        if item is None:
            monitor.enqueue("Item does not exist")
            return
        monitor.enqueue(item.get())

    @staticmethod
    def update_item(monitor, args):
        target = args.group("target")
        name = args.group("name")
        synonyms = args.group("synonyms").split(" ")
        item = Item.search(target)
        if target is None:
            monitor.enqueue("Item does not exist")
            return
        if synonyms is None or len(synonyms) == 0:
            item.update(name=name)
        else:
            item.update(name=name, synonyms=synonyms)
        monitor.enqueue("Item updated")

    @ staticmethod
    def remove_item(monitor, args):
        name = args.group("name")
        item = Item.find_one(name)
        if item is None:
            monitor.enqueue("Item does not exist")
            return
        item.delete()
