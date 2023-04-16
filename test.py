from Class.user import User
from Class.item import Item
from Class.request import Request
from Class.campaign import Campaign
from datetime import datetime

def testPrint():
    print("TEST PRINT FOR CALLBACK")

def UserTest():
    requester = User("bob", "bob@localhost", "Bob", "123")
    provider = User("alice", "alice@localhost", "Alice", "123")
    user = User("eve", "eve@localhost", "Eve", "123")
    user.update("name", "email", "fullname", "password")
    userToBeLoggedOut = User("evilcorp", "evilcorp@localhost", "Evil Corp", "123456")
    
    # Get all users one by one
    for client in User.collection:
        print(client.get())
    
    # Update user
    user.update(email="eve@protonmail.com", passwd="123456")
    print(user.get())

    # Authenticate users
    for client in User.collection:
        if client.auth("123"):
            print("User authenticated")
        else:
            print("User password for user {} is incorrect".format(client.username))
    
    # Login users
    print("Logging in user test")
    for client in User.collection:
        if client.login():
            print("User logged in")
        else:
            print("User has already logged in")
    
    # Logout user
    print("Logging out user test")
    if userToBeLoggedOut.logout():
        print("User logged out")
    else:
        print("User has already logged out")

    # Logout user
    print("Logging out user test")
    if user.logout():
        print("User logged out")
    else:
        print("User has already logged out")

    # Print session
    print("Session")
    for client in User.sessions:
        print(client)

    # Delete user
    print("Deleting user test")
    user.delete()

    # Print all users
    print("All users test")
    for client in User.collection:
        print(client.get())

    # Print session
    print("Session test")
    for client in User.sessions:
        print("User token is ", client)

def ItemTest():
    user = User("eve", "eve@localhost", "Eve", "123")
    userToBeLoggedOut = User("evilcorp", "evilcorp@localhost", "Evil Corp", "123456")
    
    item = Item("camasir suyu", ["klorak"])
    item2 = Item("simit", ["gevrek"])
    item3 = Item("pil", ["batarya", "duracell"])
    item4 = Item("cekirdek", ["karasimsek"])
    item5 = Item("araba", ["otomobil"])
    
    # Get all items one by one
    print("All items test")
    for item in Item.collection:
        print(item.get())

    # Update item
    print("Updating items test")
    item3.update(synonyms=["batarya", "duracell", "energizer"])
    item5.update(name="arac")
    # Print updated items
    print("Updated items")
    print(item3.get())
    print(item5.get())

    # Delete item
    print("Deleting item test")
    item.delete()

    # Search item
    print("Searching item for 'duracell test'")
    searchedItem = Item.search("duracell")
    if searchedItem != None:
        print("Item found")
        print(searchedItem.get())
    else:
        print("Item not found")

    # Search item
    print("Searching item for 'elma' test")
    searchedItem2 = Item.search("elma")
    if searchedItem2 != None:
        print("Item found")
        print(searchedItem2.get())
    else:
        print("Item not found")
        
    print("All items test")
    for item in Item.collection:
        print(item.get())

def RequestTest():
    user = User("eve", "eve@localhost", "Eve", "123")
    user.update("name", "email", "fullname", "password")
    userToBeLoggedOut = User("evilcorp", "evilcorp@localhost", "Evil Corp", "123456")

    item = Item("camasir suyu", ["klorak"])
    item2 = Item("simit", ["gevrek"])
    item3 = Item("pil", ["batarya", "duracell"])
    item4 = Item("cekirdek", ["karasimsek"])
    item5 = Item("araba", ["otomobil"])
    item6 = Item("elma", ["armut"])
    requester = User("tom", "tom@localhost", "Tom", "123")
    requester2 = User("spike", "spike@localhost", "Spike", "123")
    provider = User("jerry", "jerry@localhost", "Jerry", "123")
    
    # Multiple inputs
    request = Request(requester, [{"data": Item.search("camasir suyu"), "amount": 5}, {"data": Item.search("simit"), "amount": 3}], [41.015137,28.979530], "URGENT", "1st request")
    request2 = Request(requester2, [{"data": Item.search("pil"), "amount": 1}, {"data": Item.search("cekirdek"), "amount": 7}], [41.015137,28.979530], "OPTIONAL", "2nd request")
    request3 = Request(provider, [{"data": Item.search("camasir suyu"), "amount": 5}, {"data": Item.search("simit"), "amount": 3}], [41.015137,28.979530], "DAYS", "3rd request")

    # Get all requests one by one
    print("All requests test")
    for request in Request.collection:
        print(request.get())

    # Update request
    print("Updating request test")
    request.update(owner=requester, items=[{"data": Item.search("camasir suyu"), "amount": 3}, {"data": Item.search("simit"), "amount": 3}], geoloc=[41.015137,28.979530], urgency="SOON", comments="Pls help")
    print(request.get())
    request2.update(geoloc=[41.0123,28.456], urgency="SOON", comments="Need help")
    print(request2.get())
    
    # Mark available request
    print("Marking request available test")
    ma_id = request3.markavailable(user=provider, items=[{"data": Item.search("camasir suyu"), "amount": 3}, {"data": Item.search("simit"), "amount": 3}], expire=datetime.now(), geoloc=[41.015137,28.979530], comments="3rd request")
    print(request3.get())

    # Pick request
    print("Picking request test")
    request3.pick(itemid=ma_id, items=[{"data": Item.search("camasir suyu"), "amount": 3}])
    print(request3.get())

    # Arrive request
    print("Arriving request test")
    request3.arrived(itemid=ma_id)
    print(request3.get())

    # Delete request
    print("Deleting request test")
    request3.delete()

def CampaignTest():
    user = User("abc", "abc@localhost", "abc", "123")
    user2 = User("efg", "efg@localhost", "efg", "123456")
    
    item = Item("camasir suyu", ["klorak"])
    item2 = Item("simit", ["gevrek"])
    item3 = Item("pil", ["batarya", "duracell"])
    item4 = Item("cekirdek", ["karasimsek"])
    item5 = Item("araba", ["otomobil"])
    item6 = Item("elma", ["armut"])
    requester = User("tom", "tom@localhost", "Tom", "123")
    requester2 = User("spike", "spike@localhost", "Spike", "123")
    provider = User("jerry", "jerry@localhost", "Jerry", "123")
    
    # Multiple inputs
    request = Request(requester, [{"data": Item.search("camasir suyu"), "amount": 5}, {"data": Item.search("simit"), "amount": 3}], [41.015137,28.979530], "URGENT", "1st request")
    request2 = Request(requester2, [{"data": Item.search("pil"), "amount": 1}, {"data": Item.search("cekirdek"), "amount": 7}], [41.015137,28.979530], "OPTIONAL", "2nd request")
    request3 = Request(provider, [{"data": Item.search("camasir suyu"), "amount": 5}, {"data": Item.search("simit"), "amount": 3}], [41.015137,28.979530], "DAYS", "3rd request")
    # Create campaign
    campaign = Campaign("campaign1", "Here is the description")
    campaign2 = Campaign("campaign2", "Here is the description 2")

    requester = User("tom", "tom@localhost", "Tom", "123")
    requester2 = User("spike", "spike@localhost", "Spike", "123")
    provider = User("jerry", "jerry@localhost", "Jerry", "123")
    
    # Multiple inputs
    request = Request(requester, [{"data": Item.search("camasir suyu"), "amount": 5}, {"data": Item.search("simit"), "amount": 3}], [41.015137,28.979530], "URGENT", "1st request")
    request2 = Request(requester2, [{"data": Item.search("pil"), "amount": 1}, {"data": Item.search("cekirdek"), "amount": 7}], [41.015137,28.979530], "SOON", "2nd request")
    request3 = Request(provider, [{"data": Item.search("camasir suyu"), "amount": 5}, {"data": Item.search("simit"), "amount": 3}], [41.015137,28.979530], "DAYS", "3rd request")


    # Add request to campaign
    print("Add requests to campaign test")
    req_1_id = campaign.addrequest(request)
    req_2_id = campaign.addrequest(request2)

    # Update request attributes with request2
    print("Update request test")
    campaign.updaterequest(req_1_id, request2)

    # Get request by id
    print("Get request by id test")
    campaign.getrequest(req_1_id)

    # Query rectangular area by two points' coordinate references
    print("Query rectangular area test")
    campaign.query(item=Item.search("camasir suyu"), urgency="URGENT", loc={"type": 0, "values": [[41.015137,28.979530], [41.0123,28.456]]})
    # Query circular area by center point's coordinate reference and radius
    print("Query circular area test")
    campaign.query(item=Item.search("camasir suyu"), urgency="URGENT", loc={"type": 1, "values": [41.015137,28.979530, 1000]})

    # Watch campaign
    print("Watch campaign test")
    watch_id = campaign.watch(callback=testPrint, item=Item.search("camasir suyu"), urgency="DAYS", loc={"type": 0, "values": [[41.015137,28.979530], [41.0123,28.456]]})
    
    # Callback should be called after adding the target request
    print("Add request to campaign to check callback test")
    req_3_id = campaign.addrequest(request3)

    # Unwatch campaign
    print("Unwatch campaign test")
    campaign.unwatch(watch_id)

    # Remove request from campaign
    print("Remove request from campaign test")
    campaign.removerequest(req_1_id)
    print("Remove request from campaign test")
    campaign.removerequest(req_2_id)
    print("Remove request from campaign test")
    campaign.removerequest(req_3_id)

def runAllTests():
    UserTest()
    ItemTest()
    RequestTest()
    CampaignTest()


def main():
    run = input("Press 0 to exit, any other key to continue: ")
    while run != "0":
        choice = input("Do you want to run tests? (y/n): ")
        if choice == "n":
            return
        choose_test = input("Choose test to run (1-4): \n 1. User Test \n 2. Item Test \n 3. Request Test \n 4. Campaign Test \n 5. Run All Tests \n")
        if choose_test == "1":
            print("-----User Test Started-----")
            UserTest()
            print("-----User Test Finished-----\n")
        elif choose_test == "2":
            print("-----Item Test Started-----")
            ItemTest()
            print("-----Item Test Finished-----\n")
        elif choose_test == "3":
            print("-----Request Test Started-----")
            RequestTest()
            print("-----Request Test Finished-----\n")
        elif choose_test == "4":
            print("-----Campaign Test Started-----")
            CampaignTest()
            print("-----Campaign Test Finished-----\n")
        elif choose_test == "5":
            print("-----All Tests Started-----")
            runAllTests()
            print("-----All Tests Finished-----\n")
        else:
            print("Invalid input")
        run = input("Press 0 to exit, any other key to continue... ")

main()