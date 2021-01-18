from instagram_private_api import Client, ClientCompatPatch
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")
api = Client(username, password)


def __userFollowsBack(userid):
    response = api.friendships_show(userid)
    followedBack = response["followed_by"]
    print(response)
    return followedBack

def __removeFollow(userid):
    response = api.friendships_destroy(userid)
    print(response)

def __userInf(username):
    response = api.username_info(username)
    print(response)


#__userInf("andrews.00")
#__removeFollow(469589300)
#__userFollowsBack(469589300)
#test

