import random


class User:

    sessions = []

    def __init__(self, username, email, fullname, passwd):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = passwd
        self.logged = False
        self.token = None
    
    def get(self):
        return '{"username":"' + self.username + '","email":"' + self.email + '","fullname":"' + self.fullname + '","passwd":"' + self.passwd + '","logged":"' + str(self.logged) + '"}'
    
    def update(self, username, email, fullname, passwd):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = passwd

    def delete(self):
        self.username = None
        self.email = None
        self.fullname = None
        self.passwd = None
        self.logged = False

    def auth(self, plainpass):
        if plainpass == self.passwd:
            return True
        else:
            return False

    def login(self):
        if self.checksession(self.token):
            print(self.username + ' is already logged in.')
        else:
            self.logged = True
            self.token = self.username + str(random.randint(100000, 999999))
            User.sessions.append(self.token)
            print(self.username + ' is logged in.')

    def checksession(self, token):
        if self.token in User.sessions:
            return True
        else:
            return False

    def logout(self):
        self.logged = False
        print(self.username + ' is not logged in.')