from tinydb import TinyDB, Query
from datetime import datetime
from utils.Singleton import Singleton


class DBmanager(metaclass=Singleton):
    db = None
    def __init__(self):
        self.db = TinyDB('db.json')

    def addUser(self,user):
        #return inserted id
        today = datetime.now()
        return self.db.insert({'username': user["username"],"removed": False, 'id': str(user["pk"]),"date_following":today.strftime("%d/%m/%Y %H:%M:%S")})

    def removeUser(self,id):
        User = Query()
        return self.db.remove(User.id == str(id))

    def existsUser(self,id):
        User = Query()
        user=None
        user = self.db.search(User.id ==str(id))
        if(user):
            return True
        else:
            return False

    def updateRemovedFlag(self,id,removedValue):
        User = Query()
        return self.db.update({"removed":removedValue},User.id == str(id))

    def getAllUsers(self):
        return self.db.all()

    #get all users added at least 24h ago
    def getAllUsersAdded24h(self):
        User = Query()
        users = self.db.search(User.removed == False)
        print(users)
        now = datetime.now()
        users_selected= []
        for user in users:
            added = datetime.strptime(user["date_following"],"%d/%m/%Y %H:%M:%S")
            difference =  int((now - added).total_seconds()/3600)
            if(difference >=24):
                users_selected.append(user)

        return users_selected

    def getFollowingNumber(self):
        return len(self.db.all())
