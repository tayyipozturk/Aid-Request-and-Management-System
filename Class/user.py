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
    
    def update(self, username=None, email=None, fullname=None, passwd=None):
        # Update user with new values
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if fullname is not None:
            self.fullname = fullname
        if passwd is not None:
            self.passwd = ws.generate_password_hash(passwd, method='pbkdf2:sha256', salt_length=8)

    def delete(self):
        # Remove user from collection and sessions 
        # Delete user object
        User.collection.remove(self)
        if self.token is not None and self.token in User.sessions:
            User.sessions.remove(self.token)
        del self
        print('User deleted.')

    def auth(self, plainpass):
        # Authenticate user if password is correct
        if ws.check_password_hash(self.passwd, plainpass):
            return True
        else:
            return False

    def login(self):
        # Login user if not already logged in
        if User.checksession(self.token):
            return None
        else:
            self.token = self.username + str(random.randint(100000, 999999))
            User.sessions.append(self.token)
            return self.token

    @staticmethod
    def checksession(token):
        # Check if user is logged in
        if token in User.sessions:
            return True
        else:
            return False

    def logout(self):
        # Logout user if logged in
        if User.checksession(self.token):
            User.sessions.remove(self.token)
            return True
        else:
            return False