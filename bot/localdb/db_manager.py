from tinydb import TinyDB, Query
from datetime import datetime

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DBmanager(metaclass=Singleton):
    db = None
    def __init__(self):
        self.db = TinyDB('db.json')

    def addUser(self,user):
        #return inserted id
        today = datetime.now()
        return self.db.insert({'username': user["username"], 'id': str(user["pk"]),"date_following":today.strftime("%d/%m/%Y %H:%M:%S")})

    def removeUser(self,username):
        User = Query()
        return self.db.remove(User.username == username)
    def getAllUsers(self):
        return self.db.all()

    def getFollowingNumber(self):
        return len(self.db.all())