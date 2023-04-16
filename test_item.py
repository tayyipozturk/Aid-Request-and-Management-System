from Class.user import User
from Class.item import Item
from Class.request import Request
from Class.campaign import Campaign
from datetime import datetime
choice = 0
while True:
    if choice == 0:
        print("--------------------")
        choice = int(input("1-User\n2-Item\n3-Campaign\n4-Exit\nChoice:"))
    print("--------------------")
    if choice == 1:
        print("User Menu")
        operation_choice = int(input("0-Back To Menu\n1-Create User\n2-Get All Users\n3-Update User\n4-Delete User\n5-Authentication\n6-Login\n7-Check Session\n8-Logout\n> Choice:"))
        print("--------------------")
        if operation_choice == 0:
            choice = 0
            continue
        elif operation_choice == 1:
            print("Create")
            fullname = input("Fullname:")
            username = input("username:")
            email = input("Email:")
            password = input("Password:")
            user = User(username, email, fullname, password)
            print("User Created Successfully")
        elif operation_choice == 2:
            print("Get All Users")
            users = User.collection
            for user in users:
                print(user.get())
        elif operation_choice == 3:
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Update:"))
            user = users[choose_user]
            # update user
            print("Update User's Info")
            print("Leave blank if you don't want to update")
            fullname = input("Fullname:")
            username = input("username:")
            email = input("Email:")
            password = input("Password:")
            if fullname == "":
                fullname = None
            if username == "":
                username = None
            if email == "":
                email = None
            if password == "":
                password = None
            
            user.update(username, email, fullname, password)
            print("User Updated Successfully")
        elif operation_choice == 4:
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Delete:"))
            user = users[choose_user]
            user.delete()
            print("User Deleted Successfully")
        elif operation_choice == 5:
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Authenticate:"))
            get_pass = input("Enter password:")
            user = users[choose_user]
            if user.auth(get_pass):
                print("User Authenticated Successfully")
            else:
                print("User Authentication Failed")
        elif operation_choice == 6:
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Login:"))
            user = users[choose_user]
            if user.login() != None:
                print("User Logged In Successfully")
            else:
                print("User Already Logged In")
        elif operation_choice == 7:
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Check Session:"))
            user = users[choose_user]
            if user.checksession(user.token):
                print("User Session is Valid")
            else:
                print("User Session is Invalid")
        elif operation_choice == 8:
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Logout:"))
            user = users[choose_user]
            if user.logout():
                print("User Logged Out Successfully")
            else:
                print("User Already Logged Out")
                
    elif choice == 2:
        print("Item Menu")
        operation_choice = int(input("0-Back To Menu\n1-Search Item\n2-Get All Items\n3-Update Item\n4-Delete Item\n> Choice:"))
        print("--------------------")
        if operation_choice == 0:
            choice = 0
            continue
        elif operation_choice == 1:
            name = input("Name:")
            item = Item.search(name)
            if item is not None:
                print(item.get())
            else:
                print("Item not found")
        elif operation_choice == 2:
            items = Item.collection
            for item in items:
                print(item.get())
        elif operation_choice == 3:
            name = input("Name of item to update:")
            item = Item.search(name)

            if item is not None:
                print("Enter name and synonyms to update, press enter to skip")
                name = input("Name:")
                synonyms = []
                while True:
                    synonym = input("Synonym:")
                    if synonym == "":
                        break
                    synonyms.append(synonym)
                if name != "" and len(synonyms) > 0:
                    item.update(name, synonyms)
                elif name != "" and len(synonyms) == 0:
                    item.update(name=name)
                elif name == "" and len(synonyms) > 0: 
                    item.update(synonyms=synonyms)
                print("Item Updated Successfully")
            else:
                print("Item not found")
        elif operation_choice == 4:
            name = input("Name of item to delete:")
            item = Item.search(name)
            if item is not None:
                item.delete()
                print("Item deleted successfully")
            else:
                print("Item not found")
    input("Press Enter To Continue...")