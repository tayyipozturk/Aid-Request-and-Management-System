from Class.user import User
from Class.campaign import Campaign
from Class.request import Request
import threading

mutex = threading.Lock()
new_mutex = threading.Lock()
new_cond = threading.Condition(new_mutex)


class ServerParser:
    @staticmethod
    def login(client, args):
        username = args.group("username")
        password = args.group("password")
        if len(username) > 0 and len(password) > 0:
            token = User.login(username, password)
            if token:
                client.sendall(f"Login successful. Token: {token}".encode())
                return token
            else:
                client.sendall("Login failed".encode())
        return None
        '''
        if len(args) > 0:
            if args[0] == "login":
                if len(args) == 3:
                    print(args)
                    token = User.login(args[1], args[2])
                    print(token)
                    if token:
                        client.sendall(
                            f"Login successful. Token: {token}".encode())
                        return token
                    else:
                        client.sendall("Login failed".encode())
                else:
                    client.sendall("Invalid number of arguments".encode())
            else:
                client.sendall("Invalid command".encode())
        else:
            client.sendall("No arguments provided".encode())
        return None
    '''

    @staticmethod
    def logout(client, token):
        user = User.find_one(token=token)
        if user:
            user.logout()
            client.sendall("Logout successful".encode())
            return True
        else:
            client.sendall("Logout failed".encode())
            return False

    @staticmethod
    def new(client, args):
        with new_mutex:
            name = args.group("name")
            descr = args.group("descr")
            if len(name) > 0:
                campaign = Campaign(name=name, description=descr)
                client.sendall("Campaign created".encode())
                return campaign
            else:
                client.sendall("Invalid input".encode())

    @staticmethod
    def open(client, args):
        name = args.group("name")
        if len(name) > 0:
            campaign = Campaign.find_one(name)
            if campaign:
                client.sendall("Campaign opened".encode())
                return campaign
            else:
                client.sendall("Campaign not found".encode())
        else:
            client.sendall("Invalid number of arguments".encode())
        return None

    @staticmethod
    def close(client, args, campaign, watches):
        try:
            for watch in watches:
                with campaign.mutex:
                    campaign.unwatch(watch)
            return True
        except:
            return False

    @staticmethod
    def list(client, args):
        client.sendall("Index\tCampaign Name\t".encode())
        for i, campaign in enumerate(Campaign.collection):
            client.sendall(
                f"{i}\t{campaign.name}\t{campaign.description}\n".encode())
