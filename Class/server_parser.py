from Class.user import User
from Class.campaign import Campaign


class ServerParser:
    @staticmethod
    def login(client, args):
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

    @staticmethod
    def new(client, args):
        if len(args) == 2:
            client.sendall("Campaign created".encode())
            return Campaign(name=args[1], description="")
        elif len(args) == 3:
            client.sendall("Campaign created".encode())
            return Campaign(name=args[1], description=args[2])
        else:
            client.sendall("Invalid number of arguments".encode())
            return None

    @staticmethod
    def list_test(client, campaign):
        result = []
        for request in campaign.requests:
            data = campaign.getrequest(request['req_id'])
            if data != None:
                result.append(data)

        if len(result) > 0:
            client.sendall(result.encode())
        else:
            client.sendall("No requests".encode())

    @staticmethod
    def list(client, args):
        if len(args) == 1:
            client.sendall(("Campaigns:").encode())
            for campaign in Campaign.collection():
                client.sendall(
                    ("Campaign name: " + campaign.name + "\n").encode())
                client.sendall(("Campaign description: " +
                               campaign.description + "\n").encode())
                # for i, request in enumerate(campaign.requests):
                #    client.sendall(f"Request {i+1}: [{request['data'].get()}]\n".encode())
                # for i, watches in enumerate(campaign.watches):
                #    client.sendall(f"Watch {i+1}: [Watched item: {watches['item']}, Location: {watches['location']}, Urgency: {watches['urgency']}]\n".encode())

    # LISTTE YOLLADIĞIMIZ SENDALLAR CLIENTA GİTMİYOR.
    # SERVERDA EOF EKLEDİM AMA CLIENTTAKİ DÖNGÜ ÇALIŞMADI
    # BUNUN ÇÖZÜMÜNÜ BUL VE CAMPAGINLERI LIST OLARAK BASTIR
    # TEK SEFERDE SEND YAPMIYORUZ ÇÜNKÜ 1024 SINIRI VAR UNUTMA
