from Class.user import User
from Class.item import Item
from Class.request import Request
from Class.campaign import Campaign
from datetime import datetime

User("admin", "admin@localhost", "Admin", "admin")
Campaign("Campaign 0", "desc")

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
            print("Create User")
            print("--------------------")
            fullname = input("Fullname:")
            username = input("username:")
            email = input("Email:")
            password = input("Password:")
            user = User(username, email, fullname, password)
            print("User Created Successfully")
            print("--------------------")
        elif operation_choice == 2:
            print("Get All Users")
            print("--------------------")
            users = User.collection
            for user in users:
                print(user.get())
        elif operation_choice == 3:
            print("Update User")
            print("--------------------")
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
            print("--------------------")
        elif operation_choice == 4:
            print("Delete User")
            print("--------------------")
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Delete:"))
            user = users[choose_user]
            user.delete()
            print("User Deleted Successfully")
            print("--------------------")
        elif operation_choice == 5:
            print("Authentication")
            print("--------------------")
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
            print("--------------------")
        elif operation_choice == 6:
            print("Login")
            print("--------------------")
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Login:"))
            user = users[choose_user]
            if user.login() != None:
                print("User Logged In Successfully")
            else:
                print("User Already Logged In")
            print("--------------------")
        elif operation_choice == 7:
            print("Check Session")
            print("--------------------")
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Check Session:"))
            user = users[choose_user]
            if user.checksession(user.token):
                print("User Session is Valid")
            else:
                print("User Session is Invalid")
            print("--------------------")
        elif operation_choice == 8:
            print("Logout")
            print("--------------------")
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Logout:"))
            user = users[choose_user]
            if user.logout():
                print("User Logged Out Successfully")
            else:
                print("User Already Logged Out")
            print("--------------------")
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
            print("--------------------")
        elif operation_choice == 2:
            items = Item.collection
            for item in items:
                print(item.get())
            print("--------------------")
        elif operation_choice == 3:
            print("Update Item")
            print("--------------------")
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
            print("--------------------")
        elif operation_choice == 4:
            print("Delete Item")
            print("--------------------")
            name = input("Name of item to delete:")
            item = Item.search(name)
            if item is not None:
                item.delete()
                print("Item deleted successfully")
            else:
                print("Item not found")
            print("--------------------")
    elif choice == 3:
        print("Campaign Menu")
        print("--------------------")
        operation_choice = int(input("0-Back To Menu\n1-Create Campaign\n2-Add Request\n3-Get Request\n4-Update Request\n5-Remove Request\n6-Query\n7-Watch\n8-Unwatch\nChoice:"))
        print("--------------------")
        if operation_choice == 0:
            continue
        elif operation_choice == 1:
            name = input("Name:")
            description = input("Description:")
            campaign = Campaign(name, description)
            print("Campaign Created Successfully")
            print("--------------------")
        elif operation_choice == 2:
            print("Add Request")
            print("--------------------")
            campaigns = Campaign.collection
            for i, campaign in enumerate(campaigns):
                print(i, campaign.name)
            choose_campaign = int(input("Choose Campaign To Add Request:"))
            campaign = campaigns[choose_campaign]
            
            # choose user to create request
            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Choose User To Create Request:"))
            user = users[choose_user]

            owner = user.username
            items = []
            print("Press enter to skip")
            item_name = input("Item Name:")
            amount = input("Requested Amount:")
            while True:
                if item_name == "":
                    break
                item_test = Item.search(item_name)
                if item_test is None:
                    item_test = Item.search(item_name)
                items.append({"data": item_test, "amount": int(amount)})
                print("Press enter to skip")
                item_name = input("Item Name:")
                amount = input("Requested Amount:")
            
            latitude = float(input("Latitude:"))
            longtitude = float(input("Longtitude:"))
            geoloc = [longtitude, latitude]
            
            urgency = int(input("Urgency Choice:\n1-URGENT\n2-SOON\n3-DAYS\n4-WEEKS\n5-OPTIONAL\n:"))
            if urgency == 1:
                urgency = "URGENT"
            elif urgency == 2:
                urgency = "SOON"
            elif urgency == 3:
                urgency = "DAYS"
            elif urgency == 4:
                urgency = "WEEKS"
            elif urgency == 5:
                urgency = "OPTIONAL"

            comments = input("Enter Comment:")

            request = Request(owner, items, geoloc, urgency, comments)
            campaign.addrequest(request)
            print("Request Added Successfully")
            print("--------------------")
        elif operation_choice == 3:
            print("Get Request")
            print("--------------------")
            campaigns = Campaign.collection
            for i, campaign in enumerate(campaigns):
                print(i, campaign.name)
            choose_campaign = int(input("Choose Campaign To Get Request:"))
            campaign = campaigns[choose_campaign]

            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
                continue
            for i, request in enumerate(requests):
                print(i, request['data'].get())
            choose_request = int(input("Choose Request To Get:"))
            request = requests[choose_request]['data']
            req_id = requests[choose_request]['req_id']

            print(campaign.getrequest(req_id))
            print("Request Retrieved Successfully")
            print("--------------------")
        elif operation_choice == 4:
            print("Update Request")
            print("--------------------")
            campaigns = Campaign.collection
            for i, campaign in enumerate(campaigns):
                print(i, campaign.name)
            choose_campaign = int(input("Choose Campaign To Update Request:"))
            campaign = campaigns[choose_campaign]

            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
                continue
            for i, request in enumerate(requests):
                print(i, request['data'].get())
            choose_request = int(input("Choose Request To Update:"))
            request = requests[choose_request]['data']
            req_id = requests[choose_request]['req_id']

            users = User.collection
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = int(input("Update Owner of Request:"))
            cancel = input("Enter to skip")
            if cancel == "":
                user = request.owner
            else:
                user = users[choose_user]

            print("Update Items of Request")
            print("Enter Item Name and Amount to update, press enter to skip")
            items = []
            print("Press enter to skip")
            item_name = input("Item Name:")
            amount = input("Requested Amount:")
            while True:
                if item_name == "":
                    break
                item_test = Item.search(item_name)
                if item_test is None:
                    item_test = Item.search(item_name)
                items.append({"data": item_test, "amount": int(amount)})
                print("Press enter to skip")
                item_name = input("Item Name:")
                amount = input("Requested Amount:")
            
            latitude = float(input("Latitude:"))
            longtitude = float(input("Longtitude:"))
            geoloc = [longtitude, latitude]
            
            urgency = int(input("Urgency Choice:\n1-URGENT\n2-SOON\n3-DAYS\n4-WEEKS\n5-OPTIONAL\n:"))
            if urgency == 1:
                urgency = "URGENT"
            elif urgency == 2:
                urgency = "SOON"
            elif urgency == 3:
                urgency = "DAYS"
            elif urgency == 4:
                urgency = "WEEKS"
            elif urgency == 5:
                urgency = "OPTIONAL"

            comments = input("Enter Comment:")
            campaign.updaterequest(req_id, request)
            print("Request Updated Successfully")
            print("--------------------")
        elif operation_choice == 5:
            print("Remove Request")
            print("--------------------")
            campaigns = Campaign.collection
            for i, campaign in enumerate(campaigns):
                print(i, campaign.name)
            choose_campaign = int(input("Choose Campaign To Remove Request:"))
            campaign = campaigns[choose_campaign]
            
            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
                continue
            for i, request in enumerate(requests):
                print(i, request["data"].get())
            choose_request = int(input("Choose Request To Remove:"))
            request = requests[choose_request]

            campaign.removerequest(request['req_id'])
            print("Request Removed Successfully")
        elif operation_choice == 6:
            print("Query")
            campaigns = Campaign.collection
            for i, campaign in enumerate(campaigns):
                print(i, campaign.name)
            choose_campaign = int(input("Choose Campaign To Query Request:"))
            campaign = campaigns[choose_campaign]

            items = []
            print("Press enter to skip")
            item_name = input("Item Name:")
            amount = input("Requested Amount:")
            while True:
                if item_name == "":
                    break
                items.append({"name": item_name, "amount": int(amount)})
                print("Press enter to skip")
                item_name = input("Item Name:")
                amount = input("Requested Amount:")
            
            print("Press enter to skip")
            location_type = input("Location Type:\n1-Rectangular\n2-Circular\n:")
            if(location_type == ""):
                location_type = None
            elif int(location_type) == 1:
                location_type = "RECTANGULAR"
            elif int(location_type) == 2:
                location_type = "CIRCULAR"

            if location_type == "RECTANGULAR":
                print("Enter Coordinates of First Corner")
                latitude = float(input("Latitude:"))
                longtitude = float(input("Longtitude:"))
                corner1 = [longtitude, latitude]
                print("Enter Coordinates of Second Corner")
                latitude = float(input("Latitude:"))
                longtitude = float(input("Longtitude:"))
                corner2 = [longtitude, latitude]
                geoloc = {'type': 0, 'values': [corner1, corner2]}
            elif location_type == "CIRCULAR":
                print("Enter Coordinates of Center")
                latitude = float(input("Latitude:"))
                longtitude = float(input("Longtitude:"))
                center = [longtitude, latitude]
                radius = float(input("Radius:"))
                geoloc = {'type': 1, 'values': [center, radius]}

            print("Press enter to skip")
            urgency = input("Urgency Choice:\n1-URGENT\n2-SOON\n3-DAYS\n4-WEEKS\n5-OPTIONAL\n:")
            if urgency == "":
                urgency = None
            elif int(urgency) == 1:
                urgency = "URGENT"
            elif int(urgency) == 2:
                urgency = "SOON"
            elif int(urgency) == 3:
                urgency = "DAYS"
            elif int(urgency) == 4:
                urgency = "WEEKS"
            elif int(urgency) == 5:
                urgency = "OPTIONAL"
            
            if len(items) == 0:
                items = None
            returnList = campaign.query(items, geoloc, urgency)
            for request in returnList:
                print(request.get())
            print("Query Successful")
            print("--------------------")
        elif operation_choice == 7:
            print("Watch")
            print("--------------------")
            campaigns = Campaign.collection
            for i, campaign in enumerate(campaigns):
                print(i, campaign.name)
            choose_campaign = int(input("Choose Campaign To Get Offers:"))
            campaign = campaigns[choose_campaign]

            items = Item.collection
            for i, item in enumerate(items):
                print(i, item.get())
            choose_item = int(input("Choose Item To Get Offers:"))
            item = items[choose_item]

            location_type = int(input("Location Type:\n1-Rectangular\n2-Circular\n:"))
            if location_type == 1:
                location_type = "RECTANGULAR"
            elif location_type == 2:
                location_type = "CIRCULAR"

            if location_type == "RECTANGULAR":
                print("Enter Coordinates of First Corner")
                latitude = float(input("Latitude:"))
                longtitude = float(input("Longtitude:"))
                corner1 = [longtitude, latitude]
                print("Enter Coordinates of Second Corner")
                latitude = float(input("Latitude:"))
                longtitude = float(input("Longtitude:"))
                corner2 = [longtitude, latitude]
                geoloc = {'type': 0, 'values': [corner1, corner2]}
            elif location_type == "CIRCULAR":
                print("Enter Coordinates of Center")
                latitude = float(input("Latitude:"))
                longtitude = float(input("Longtitude:"))
                center = [longtitude, latitude]
                radius = float(input("Radius:"))
                geoloc = {'type': 1, 'values': [center, radius]}
            
            urgency = int(input("Urgency Choice:\n1-URGENT\n2-SOON\n3-DAYS\n4-WEEKS\n5-OPTIONAL\n:"))
            if urgency == 1:
                urgency = "URGENT"
            elif urgency == 2:
                urgency = "SOON"
            elif urgency == 3:
                urgency = "DAYS"
            elif urgency == 4:
                urgency = "WEEKS"
            elif urgency == 5:
                urgency = "OPTIONAL"

            campaign.watch(item=item, geoloc=geoloc, urgency=urgency)
            print("Watch Successful")
            print("--------------------")
        elif operation_choice == 8:
            print("Unwatch")
            print("--------------------")
            campaigns = Campaign.collection
            for i, campaign in enumerate(campaigns):
                print(i, campaign.name)
            choose_campaign = int(input("Choose Campaign To Get Offers:"))
            campaign = campaigns[choose_campaign]
            
            watches = campaign.watches
            for i, watch in enumerate(watches):
                print(i, watch.get())
            choose_watch = int(input("Choose Watch To Remove:"))
            watch = watches[choose_watch]
            watch_id = watch['watch_id']

            campaign.unwatch(watch_id)
            print("Unwatch Successful")
            print("--------------------")
    elif choice == 4:
        break
    print("--------------------")
    input("Press Enter To Continue...")