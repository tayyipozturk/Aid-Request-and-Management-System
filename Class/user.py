import random
import werkzeug.security as ws

class User:
    collection = []
    sessions = []

    def __init__(self, username, email, fullname, passwd):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = ws.generate_password_hash(passwd, method='pbkdf2:sha256', salt_length=8)
        self.token = None
        User.collection.append(self)
    
    def get(self):
        return '{"username":"' + self.username + '","email":"' + self.email + '","fullname":"' + self.fullname + '","passwd":"' + self.passwd + '"}'
    
    def update(self, username, email, fullname, passwd):
        self.username = username
        self.email = email
        self.fullname = fullname
        self.passwd = passwd

    def delete(self):
        User.collection.remove(self)
        del self

    def auth(self, plainpass):
        if ws.check_password_hash(plainpass, self.passwd):
            return True
        else:
            print('Wrong password.')
            return False

    def login(self):
        if User.checksession(self.token):
            print(self.username + ' is already logged in.')
            return None
        else:
            self.token = self.username + str(random.randint(100000, 999999))
            User.sessions.append(self.token)
            print(self.username + ' is logged in.')
            return self.token

    @staticmethod
    def checksession(token):
        if token in User.sessions:
            return True
        else:
            return False

    def logout(self):
        if User.checksession(self.token):
            User.sessions.remove(self.token)
            print(self.username + ' is logged out.')
            return True