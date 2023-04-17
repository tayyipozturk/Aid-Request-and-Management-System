from Class.user import User
from Class.item import Item
from Class.request import Request
from Class.campaign import Campaign
from datetime import datetime
import os

# usertest = User("admin", "admin@localhost", "Admin", "admin")
# camptest = Campaign("Campaign 0", "desc")

# item_limon = Item.search("limon")
# if item_limon is None:
#     item_limon = Item.search("limon")

# item_simit = Item.search("simit")
# if item_simit is None:
#     item_simit = Item.search("simit")
# request_test1 = Request(usertest.username, [{"data": item_limon, "amount": 5}, {"data": item_simit, "amount": 3}], [41.015137,28.979530], "URGENT", "1st request")
# camptest.addrequest(request_test1)


choice = 0
while True:
    if choice == 0:
        print("--------------------")
        choice = input("1-User\n2-Item\n3-Campaign\n4-Request\n5-Exit\n> Choice:")
        if choice != "":
            choice = int(choice)
        else:
            continue
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------------")
    if choice == 1:
        print("User Menu")
        operation_choice = input("0-Back To Menu\n1-Create User\n2-Get All Users\n3-Update User\n4-Delete User\n5-Authorization\n6-Login\n7-Check Session\n8-Logout\n> Choice:")
        if operation_choice != "":
            operation_choice = int(operation_choice)
        else:
            continue
        print("--------------------")
        os.system('cls' if os.name == 'nt' else 'clear')
        if operation_choice == 0:
            choice = 0
            continue
        elif operation_choice == 1:
            print("Create User")
            print("--------------------")
            fullname = input("> Fullname:")
            username = input("> username:")
            email = input("> Email:")
            password = input("> Password:")
            user = User(username, email, fullname, password)
            print("User Created Successfully")
            print("--------------------")
        elif operation_choice == 2:
            print("Get All Users")
            print("--------------------")
            users = User.collection
            print("Users:")
            for user in users:
                print(user.get())
        elif operation_choice == 3:
            print("Update User")
            print("--------------------")
            users = User.collection
            if (len(users) == 0):
                input("> No users available. Press enter to continue...")
                continue
            print("Users:")
            print("Index\tUser Data")
            for i, user in enumerate(users):
                print(i,"\t", user.get())
            choose_user = input("> Choose User To Update:")
            if choose_user != "":
                choose_user = int(choose_user)
                if choose_user >= len(users):
                    continue
            user = users[choose_user]
            # update user
            print("Update User's Info")
            print("Leave blank if you don't want to update")
            fullname = input("> Fullname:")
            username = input("> username:")
            email = input("> Email:")
            password = input("> Password:")
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
            if (len(users) == 0):
                input("> No users available. Press enter to continue...")
                continue
            print("Users:")
            print("Index\tUser Data")
            for i, user in enumerate(users):
                print(i,"\t", user.get())
            choose_user = input("> Choose User To Delete:")
            if choose_user != "":
                choose_user = int(choose_user)
                if choose_user >= len(users):
                    continue
            user = users[choose_user]
            user.delete()
            print("User Deleted Successfully")
            print("--------------------")
        elif operation_choice == 5:
            print("Authorization")
            print("--------------------")
            users = User.collection
            print("Users:")
            print("Index\tUser Data")
            for i, user in enumerate(users):
                print(i,"\t", user.get())
            choose_user = input("> Choose User To Authorize:")
            get_pass = input("> Enter password:")
            if choose_user != "":
                choose_user = int(choose_user)
                if choose_user >= len(users):
                    continue
            user = users[choose_user]
            if user.auth(get_pass):
                print("User Authorized Successfully")
            else:
                print("User Authorization Failed")
            print("--------------------")
        elif operation_choice == 6:
            print("Login")
            print("--------------------")
            username = input("> Enter username:")
            password = input("> Enter password:")
            if User.login(username, password) != None:
                print("User Logged In Successfully")
            else:
                print("User Already Logged In")
            print("--------------------")
        elif operation_choice == 7:
            print("Check Session")
            print("--------------------")
            users = User.collection
            if (len(users) == 0):
                input("> No users available. Press enter to continue...")
                continue
            print("Users:")
            print("Index\tUser Data")
            for i, user in enumerate(users):
                print(i,"\t", user.get())
            choose_user = input("> Choose User To Check Session:")
            if choose_user != "":
                choose_user = int(choose_user)
                if choose_user >= len(users):
                    continue
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
            if (len(users) == 0):
                input("> No users available. Press enter to continue...")
                continue
            print("Users:")
            print("Index\tUser Data")
            for i, user in enumerate(users):
                print(i,"\t", user.get())
            choose_user = input("> Choose User To Logout:")
            if choose_user != "":
                choose_user = int(choose_user)
                if choose_user >= len(users):
                    continue
            user = users[choose_user]
            if user.logout():
                print("User Logged Out Successfully")
            else:
                print("User Already Logged Out")
            print("--------------------")
    elif choice == 2:
        print("Item Menu")
        operation_choice = input("0-Back To Menu\n1-Search Item\n2-Get All Items\n3-Update Item\n4-Delete Item\n> Choice:")
        if operation_choice != "":
            operation_choice = int(operation_choice)
        else:
            continue
        print("--------------------")
        os.system('cls' if os.name == 'nt' else 'clear')
        if operation_choice == 0:
            choice = 0
            continue
        elif operation_choice == 1:
            name = input("> Name:")
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
            items = Item.collection
            if len(items) == 0:
                print("No Items Found")
                
            else:
                print("Items:")
                print("Index\tItem Name")
                for i, item in enumerate(items):
                    print(i,"\t", item.name)
                choose_item = input("> Choose Item To Update:")
                if choose_item != "":
                    item = items[int(choose_item)]
                    print("Enter name and synonyms to update, press enter to skip")
                    name = input("> Name:")
                    synonyms = []
                    while True:
                        synonym = input("> Synonym:")
                        if synonym == "":
                            break
                        synonyms.append(synonym)
                    if name != "" and len(synonyms) > 0:
                        item.update(name, synonyms)
                    elif name != "" and len(synonyms) == 0:
                        item.update(name=name)
                    elif name == "" and len(synonyms) > 0: 
                        item.update(synonyms=synonyms)
                    print("Item updated successfully")
                else:
                    print("Item not found")
            print("--------------------")
        elif operation_choice == 4:
            print("Delete Item")
            print("--------------------")
            items = Item.collection
            if len(items) == 0:
                print("No Items Found")
                
            else:
                print("Items:")
                print("Index\tItem Name")
                for i, item in enumerate(items):
                    print(i,"\t", item.name)
                choose_item = input("> Choose Item To Delete:")
                if choose_item != "":
                    item = items[int(choose_item)]
                    item.delete()
                    print("Item deleted successfully")
                else:
                    print("Item not found")
            print("--------------------")
    elif choice == 3:
        print("Campaign Menu")
        print("--------------------")
        operation_choice = input("0-Back To Menu\n1-Create Campaign\n2-Add Request\n3-Get Request\n4-Update Request\n5-Remove Request\n6-Query\n7-Watch\n8-Unwatch\n> Choice:")
        if operation_choice != "":
            operation_choice = int(operation_choice)
        else:
            continue
        print("--------------------")
        os.system('cls' if os.name == 'nt' else 'clear')
        if operation_choice == 0:
            choice = 0
            continue
        elif operation_choice == 1:
            name = input("> Name:")
            description = input("> Description:")
            campaign = Campaign(name, description)
            print("Campaign Created Successfully")
            print("--------------------")
        elif operation_choice == 2:
            print("Add Request")
            print("--------------------")
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Add Request:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]
            
            # choose user to create request
            users = User.collection
            if (len(users) == 0):
                input("> No users available. Press enter to continue...")
                continue
            print("Users:")
            print("Index\tUser Data")
            for i, user in enumerate(users):
                print(i,"\t", user.get())
            choose_user = input("> Choose User To Create Request:")
            if choose_user != "":
                choose_user = int(choose_user)
                if choose_user >= len(users):
                    continue
            user = users[choose_user]

            owner = user.username
            items = []
            print("Press enter to skip")
            item_name = input("> Item Name:")
            amount = input("> Requested Amount:")
            while True:
                if item_name == "":
                    break
                item_test = Item.search(item_name)
                if item_test is None:
                    item_test = Item.search(item_name)
                items.append({"data": item_test, "amount": int(amount)})
                print("Press enter to skip")
                item_name = input("> Item Name:")
                amount = input("> Requested Amount:")
            
            print("Geoloc data of request")
            latitude = float(input("> Latitude:"))
            longtitude = float(input("> Longtitude:"))
            geoloc = [longtitude, latitude]
            
            urgency = input("Urgency Choice:\n1-URGENT\n2-SOON\n3-DAYS\n4-WEEKS\n5-OPTIONAL\n> Choose:")
            if urgency == "":
                urgency = None
            else:
                urgency = int(urgency)

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
            else:
                input("Wrong Input...")
                continue

            comments = input("> Enter Comment:")

            request = Request(owner, items, geoloc, urgency, comments)
            campaign.addrequest(request)
            print("Request Added Successfully")
            print("--------------------")
        elif operation_choice == 3:
            print("Get Request")
            print("--------------------")
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Get Request:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]

            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
            else:
                for i, request in enumerate(requests):
                    print(i,"\t", request['req_id'])
                choose_request = input("> Choose Request To Get:")
                if choose_request != "":
                    choose_request = int(choose_request)
                    if choose_request >= len(requests):
                        continue
                request = requests[choose_request]['data']
                req_id = requests[choose_request]['req_id']

                print(campaign.getrequest(req_id))
                print("Request Retrieved Successfully")
                
            print("--------------------")
        elif operation_choice == 4:
            print("Update Request")
            print("--------------------")
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Update Request:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]

            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
                continue
            for i, request in enumerate(requests):
                print(i, request['data'].get())
            choose_request = input("> Choose Request To Update:")
            if choose_request != "":
                choose_request = int(choose_request)
                if choose_request >= len(requests):
                    continue
            request = requests[choose_request]['data']
            req_id = requests[choose_request]['req_id']

            users = User.collection
            if (len(users) == 0):
                input("> No users available. Press enter to continue...")
                continue
            for i, user in enumerate(users):
                print(i, user.get())
            choose_user = input("> Update Owner of Request:")
            if choose_user != "":
                choose_user = int(choose_user)
                if choose_user >= len(users):
                    continue
            cancel = input("> Enter to skip")
            if cancel == "":
                user = request.owner
            else:
                user = users[choose_user]

            print("Update Items of Request")
            print("Enter Item Name and Amount to update, press enter to skip")
            items = []
            print("Press enter to skip")
            item_name = input("> Item Name:")
            amount = input("> Requested Amount:")
            while True:
                if item_name == "":
                    break
                item_test = Item.search(item_name)
                if item_test is None:
                    item_test = Item.search(item_name)
                items.append({"data": item_test, "amount": int(amount)})
                print("Press enter to skip")
                item_name = input("> Item Name:")
                amount = input("> Requested Amount:")
            
            latitude = float(input("> Latitude:"))
            longtitude = float(input("> Longtitude:"))
            geoloc = [longtitude, latitude]
            
            urgency = input("Urgency Choice:\n1-URGENT\n2-SOON\n3-DAYS\n4-WEEKS\n5-OPTIONAL\n> Choose:")
            if urgency == "":
                urgency = None
            else:
                urgency = int(urgency)

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
            else:
                input("Wrong Input...")
                continue

            comments = input("> Enter Comment:")
            campaign.updaterequest(req_id, request)
            print("Request Updated Successfully")
            print("--------------------")
        elif operation_choice == 5:
            print("Remove Request")
            print("--------------------")
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Remove Request:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]
            
            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
                continue
            print("Requests:")
            print("Index\tRequest Data")
            for i, request in enumerate(requests):
                print(i,"\t", request["data"].get())
            choose_request = input("> Choose Request To Remove:")
            if choose_request != "":
                choose_request = int(choose_request)
                if choose_request >= len(requests):
                    continue
            request = requests[choose_request]

            campaign.removerequest(request['req_id'])
            print("Request Removed Successfully")
        elif operation_choice == 6:
            print("Query")
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Query Request:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]

            items = []
            print("Press enter to skip")
            item_name = input("> Item Name:")
            while True:
                if item_name == "":
                    break
                found_item = Item.search(item_name)
                if found_item is None:
                    found_item = Item.search(item_name)
                items.append(found_item)           
                print("Press enter to skip")
                item_name = input("> Item Name:")
            
            print("Press enter to skip")
            location_type = input("Location Type:\n1-Rectangular\n2-Circular\n> Choose:")
            if(location_type == ""):
                location_type = None
                geoloc = None
            elif int(location_type) == 1:
                location_type = "RECTANGULAR"
            elif int(location_type) == 2:
                location_type = "CIRCULAR"

            if location_type == "RECTANGULAR":
                print("Enter Coordinates of First Corner")
                latitude = float(input("> Latitude:"))
                longtitude = float(input("> Longtitude:"))
                corner1 = [longtitude, latitude]
                print("Enter Coordinates of Second Corner")
                latitude = float(input("> Latitude:"))
                longtitude = float(input("> Longtitude:"))
                corner2 = [longtitude, latitude]
                geoloc = {'type': 0, 'values': [corner1, corner2]}
            elif location_type == "CIRCULAR":
                print("Enter Coordinates of Center")
                latitude = float(input("> Latitude:"))
                longtitude = float(input("> Longtitude:"))
                center = [longtitude, latitude]
                radius = float(input("> Radius:"))
                geoloc = {'type': 1, 'values': [center, radius]}

            print("Press enter to skip")
            urgency = input("Urgency Choice:\n1-URGENT\n2-SOON\n3-DAYS\n4-WEEKS\n5-OPTIONAL\n> Choose:")
            if urgency == "":
                urgency = None
            else:
                if int(urgency) == 1:
                    urgency = "URGENT"
                elif int(urgency) == 2:
                    urgency = "SOON"
                elif int(urgency) == 3:
                    urgency = "DAYS"
                elif int(urgency) == 4:
                    urgency = "WEEKS"
                elif int(urgency) == 5:
                    urgency = "OPTIONAL"
                else:
                    input("Wrong Input...")
                    continue
            
            if len(items) == 0:
                items = None
            returnList = campaign.query(items, geoloc, urgency)
            print("Query Successful")
            print("Returned Requests:")
            for request in returnList:
                print(request.get())
            print("--------------------")
        elif operation_choice == 7:
            print("Watch")
            print("--------------------")
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Get Offers:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]

            items = []
            print("Press enter to skip")
            item_name = input("> Item Name:")
            while True:
                if item_name == "":
                    break
                found_item = Item.search(item_name)
                if found_item is None:
                    found_item = Item.search(item_name)
                items.append(found_item)               
                print("Press enter to skip")
                item_name = input("> Item Name:")

            location_type = input("Location Type:\n1-Rectangular\n2-Circular\n> Choose:")
            if location_type == "":
                location_type = None
                geoloc = None
            elif int(location_type) == 1:
                location_type = "RECTANGULAR"
            elif int(location_type) == 2:
                location_type = "CIRCULAR"

            if location_type == "RECTANGULAR":
                print("Enter Coordinates of First Corner")
                latitude = float(input("> Latitude:"))
                longtitude = float(input("> Longtitude:"))
                corner1 = [longtitude, latitude]
                print("Enter Coordinates of Second Corner")
                latitude = float(input("> Latitude:"))
                longtitude = float(input("> Longtitude:"))
                corner2 = [longtitude, latitude]
                geoloc = {'type': 0, 'values': [corner1, corner2]}
            elif location_type == "CIRCULAR":
                print("Enter Coordinates of Center")
                latitude = float(input("> Latitude:"))
                longtitude = float(input("> Longtitude:"))
                center = [longtitude, latitude]
                radius = float(input("> Radius:"))
                geoloc = {'type': 1, 'values': [center, radius]}
            
            urgency = input("Urgency Choice:\n1-URGENT\n2-SOON\n3-DAYS\n4-WEEKS\n5-OPTIONAL\n> Choose:")
            if urgency == "":
                urgency = None
            else:
                if int(urgency) == 1:
                    urgency = "URGENT"
                elif int(urgency) == 2:
                    urgency = "SOON"
                elif int(urgency) == 3:
                    urgency = "DAYS"
                elif int(urgency) == 4:
                    urgency = "WEEKS"
                elif int(urgency) == 5:
                    urgency = "OPTIONAL"
                else:
                    input("Wrong Input...")
                    continue

            if len(items) == 0:
                items = []
            def callback():
                print("-CALLBACK CALLED-")
            watchid = campaign.watch(callback, items, geoloc, urgency)
            print("Watch Successful")
            print("WATCH ID: ", watchid)
            print("--------------------")
        elif operation_choice == 8:
            print("Unwatch")
            print("--------------------")
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Get Offers:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]
            
            watches = campaign.watches
            if len(watches) == 0:
                print("No Watches")
            else:
                print("Watches:")
                print("Index\tWatch Info")
                for i, watch in enumerate(watches):
                    ret_str = ""
                    if watch["item"] != None and len(watch["item"]) != 0:
                        ret_str += "items: ["
                        for item in watch["item"]:
                            ret_str += item.name + ", "
                        ret_str += "], "
                    if watch["loc"] is not None:
                        ret_str += "loc: " + str(watch["loc"]) + ", "
                    if watch["urgency"] is not None:
                        ret_str += "urgency: " + watch["urgency"] + ", "
                    print(i,"\t", ret_str)
                choose_watch = input("> Choose Watch To Remove:")
                if (choose_watch != ""):
                    watch = watches[int(choose_watch)]
                    watch_id = watch['watch_id']

                    campaign.unwatch(watch_id)
                    print("Unwatch Successful")
                    print("--------------------")
    elif choice == 4:
        print("Request Menu")
        print("--------------------")
        operation_choice = input("0-Back To Menu\n1-Mark Available\n2-Pick\n3-Arrived\n> Choice:")
        if operation_choice != "":
            operation_choice = int(operation_choice)
        else:
            continue
        print("--------------------")
        os.system('cls' if os.name == 'nt' else 'clear')
        if operation_choice == 0:
            choice = 0
            continue
        elif operation_choice == 1:
            print("Mark Available")
            print("--------------------")
            # SELECT CAMPAIGN
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Continue To Mark Available:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]
            # SELECT REQUEST
            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
                continue
            print("Requests:")
            print("Index\tRequest Data")
            for i, request in enumerate(requests):
                print(i,"\t", request["data"].get())
            choose_request = input("> Choose Request To Continue To Mark Available:")
            if choose_request != "":
                choose_request = int(choose_request)
                if choose_request >= len(requests):
                    continue
            request = requests[choose_request]
            # SELECT USER
            users = User.collection
            if (len(users) == 0):
                input("> No users available. Press enter to continue...")
                continue
            print("Users:")
            print("Index\tUser Data")
            for i, user in enumerate(users):
                print(i,"\t", user.get())
            choose_user = input("> Choose User To Continue To Mark Available:")
            if choose_user != "":
                choose_user = int(choose_user)
                if choose_user >= len(users):
                    continue
            user = users[choose_user]
            # GET ITEMS WITH AMOUNT
            items = []
            print("Press enter to skip")
            item_name = input("> Item Name:")
            amount = input("> Requested Amount:")
            while True:
                if item_name == "":
                    break
                item_test = Item.search(item_name)
                if item_test is None:
                    item_test = Item.search(item_name)
                items.append({"data": item_test, "amount": int(amount)})
                print("Press enter to skip")
                item_name = input("> Item Name:")
                amount = input("> Requested Amount:")
            # GET EXPIRE
            expire = input("> Expire(Hour):")
            if expire == "":
                expire = 0
            else:
                expire = int(expire)
            # GET GEOLOC
            latitude = input("> Latitude:")
            if latitude != "":
                latitude = float(latitude)
            longtitude = input("> Longtitude:")
            if longtitude != "":
                longtitude = float(longtitude)
            geoloc = [longtitude, latitude]
            # GET COMMENT
            comments = input("> Enter Comment:")
            # MARK AVAILABLE
            ma_id = request["data"].markavailable(user, items, expire, geoloc, comments)
            print("Mark Available Successful")
            print("Mark Available ID:", ma_id)
            print("--------------------")
        elif operation_choice == 2:
            print("Pick")
            print("--------------------")
            # SELECT CAMPAIGN
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Continue To Pick:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]
            # SELECT REQUEST
            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
                continue
            print("Requests:")
            print("Index\tRequest Data")
            for i, request in enumerate(requests):
                print(i,"\t", request["data"].get())
            choose_request = input("> Choose Request To Continue To Pick:")
            if choose_request != "":
                choose_request = int(choose_request)
                if choose_request >= len(requests):
                    continue
            request = requests[choose_request]
            # SELECT MARKAVAILABLE
            print("Mark Available:")
            print("Index\tMark Available Data")
            unique_ma_id = []
            for i, dict in enumerate(request["data"].items_dict):
                if dict["availibility"] == None:
                    continue
                else:
                    if dict["availibility"]["ma_id"] not in unique_ma_id:
                        unique_ma_id.append(dict["availibility"]["ma_id"])
                        print(i,"\t", dict["availibility"]["ma_id"])
            choose_markavailable = input("> Choose Available ID To Continue To Pick:")
            selected_maid = request["data"].items_dict[int(choose_markavailable)]["availibility"]["ma_id"]
            # GET ITEMS
            items = []
            print("Press enter to skip")
            item_name = input("> Item Name:")
            amount = input("> Requested Amount:")
            while True:
                if item_name == "":
                    break
                item_test = Item.search(item_name)
                if item_test is None:
                    item_test = Item.search(item_name)
                items.append({"data": item_test, "amount": int(amount)})
                print("Press enter to skip")
                item_name = input("> Item Name:")
                amount = input("> Requested Amount:")
            # PICK
            request["data"].pick(selected_maid,items)
            print("Pick Successful")
            print("--------------------")
        elif operation_choice == 3:
            print("Arrived")
            print("--------------------")
            # SELECT CAMPAIGN
            campaigns = Campaign.collection
            if (len(campaigns) == 0):
                input("> No campaigns available. Press enter to continue...")
                continue
            print("Campaigns:")
            print("Index\tCampaign Name")
            for i, campaign in enumerate(campaigns):
                print(i,"\t", campaign.name)
            choose_campaign = input("> Choose Campaign To Continue To Done Arrival:")
            if choose_campaign != "":
                choose_campaign = int(choose_campaign)
                if choose_campaign >= len(campaigns):
                    continue
            campaign = campaigns[choose_campaign]
            # SELECT REQUEST
            requests = campaign.requests
            if len(requests) == 0:
                print("No Requests")
                print("--------------------")
                continue
            print("Requests:")
            print("Index\tRequest Data")
            for i, request in enumerate(requests):
                print(i,"\t", request["data"].get())
            choose_request = input("> Choose Request To Continue To Done Arrival:")
            if choose_request != "":
                choose_request = int(choose_request)
                if choose_request >= len(requests):
                    continue
            request = requests[choose_request]
            
            unique_ma_id = []
            for i, dict in enumerate(request["data"].items_dict):
                if dict["onroute"] == None:
                    continue
                else:
                    if dict["onroute"]["ma_id"] not in unique_ma_id:
                        unique_ma_id.append(dict["onroute"]["ma_id"])
                        print(i,"\t", dict["onroute"]["ma_id"])
            choose_markavailable = input("> Choose Available ID To Continue To Done Arrival:")
            selected_maid = request["data"].items_dict[int(choose_markavailable)]["onroute"]["ma_id"]
            # ARRIVED
            request["data"].arrived(selected_maid)
            print("Arrived Successful")
            print("--------------------")
    elif choice == 5:
        pass
    print("--------------------")
    input("> Press Enter To Continue...")

