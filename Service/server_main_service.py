from Class.user import User
from Class.campaign import Campaign
from Class.request import Request
import threading

mutex = threading.Lock()
new_mutex = threading.Lock()
new_cond = threading.Condition(new_mutex)


class ServerParser:
    @staticmethod
    def login(monitor, args):
        username = args.group("username")
        password = args.group("password")
        if len(username) > 0 and len(password) > 0:
            token = User.login(username, password)
            if token:
                monitor.enqueue(f"Login successful. Token: {token}")
                return token
            else:
                monitor.enqueue("Login failed")
        return None

    @staticmethod
    def logout(monitor, token):
        user = User.find_one(token=token)
        if user:
            user.logout()
            monitor.enqueue("Logout successful")
            return True
        else:
            monitor.enqueue("Logout failed")
            return False

    @staticmethod
    def new(monitor, args):
        with new_mutex:
            name = args.group("name")
            descr = args.group("descr")
            if len(name) > 0:
                campaign = Campaign(name=name, description=descr)
                monitor.enqueue("Campaign created")
                return campaign
            else:
                monitor.enqueue("Invalid input")

    @staticmethod
    def open(monitor, args):
        name = args.group("name")
        if len(name) > 0:
            campaign = Campaign.find_one(name)
            if campaign:
                monitor.enqueue("Campaign opened")
                return campaign
            else:
                monitor.enqueue("Campaign not found")
        else:
            monitor.enqueue("Invalid number of arguments")
        return None

    @staticmethod
    def close(monitor, args, campaign, watches):
        try:
            for watch in watches:
                with campaign.mutex:
                    campaign.unwatch(watch)
            return True
        except:
            return False

    @staticmethod
    def list(monitor, args):
        monitor.enqueue("Index\tCampaign Name\t")
        for i, campaign in enumerate(Campaign.collection):
            monitor.enqueue(
                f"{i}\t{campaign.name}\t{campaign.description}")
