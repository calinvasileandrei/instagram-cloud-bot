from bot.localdb.db_manager import DBmanager

dbmanager = DBmanager()

def __users24hago():
    print(dbmanager.getAllUsersAdded24h())



#__users24hago()

#print( dbmanager.existsUser("498298"))

#dbmanager.addUser({"username":"andrew","pk":1})
#print(dbmanager.removeUser("andrew"))
#print(dbmanager.getFollowingNumber())