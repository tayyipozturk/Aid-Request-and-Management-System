from Service.server_main_service import mutex, new_cond
from Class.user import User
from Class.request import Request
from Class.item import Item


class ItemService:
    @staticmethod
    def search_item(client, args):
        name = args.group("name")
        with mutex:
            item = Item.search(name)
            if item is None:
                client.sendall("Item does not exist".encode())
                return
            client.sendall(item.get().encode())

    @staticmethod
    def update_item(client, args):
        with mutex:
            print(args.groupdict())
            target = args.group("target")
            name = args.group("name")
            synonyms = args.group("synonyms").split(" ")
            item = Item.search(target)
            if target is None:
                client.sendall("Item does not exist".encode())
                return
            if synonyms is None or len(synonyms) == 0:
                item.update(name=name)
            else:
                item.update(name=name, synonyms=synonyms)

    @ staticmethod
    def remove_item(client, args):
        name = args.group("name")
        with mutex:
            item = Item.find_one(name)
            if item is None:
                client.sendall("Item does not exist".encode())
                return
            item.delete()
