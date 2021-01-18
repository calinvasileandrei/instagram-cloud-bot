from instagram_private_api import Client, ClientCompatPatch
import json
import os
from random import randint
import time
import logging
from threading import Thread
from bot.localdb.db_manager import DBmanager

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(
    "debug.log"), logging.StreamHandler()])
from bot.status import Status,Operation

class InstagramCloudBot(Thread):

    __api=None
    __status=Status.offline
    __dbmanager=None
    __operation = None

    def __init__(self, _username, _password,_operation):
        super().__init__()
        self.__api = Client(_username, _password)
        self.__dbmanager = DBmanager()
        self.__operation = _operation

    def run(self):
        if(self.__operation == Operation.work):
            self.__work()
        elif (self.__operation == Operation.unfollow):
            self.__removeNotFollowingBack()

    def getBotFollowedUsers(self):
        return self.__dbmanager.getAllUsers()

    def getBotFollowingNumber(self):
        return self.__dbmanager.getFollowingNumber()

    def stop(self):
        self.__updateStatus(Status.offline)

    def status(self):
        return self.__status

    #private
    def __createFollowingFile(self):
        results = self.__api.user_following(self.__api.authenticated_user_id, self.__api.generate_uuid())
        with open('following.json', 'w', encoding='utf-8') as f:
            json.dump(results["users"], f, ensure_ascii=False, indent=4)
            return results["users"]


    def __readFollowingFile(self):
        with open('following.json', encoding='utf-8') as fh:
            data = json.load(fh)
            return data


    def __findRandomUser(self, following):
        maxFollowing = len(following)
        userChoosen = randint(0, maxFollowing)
        return following[userChoosen]


    def __findLastUserPost(self, user):
        feed = self.__api.username_feed(user["username"])
        if (len(feed["items"]) > 0):
            lastPost = feed["items"][0]
            return lastPost


    def __findMediaLikers(self, post):
        mediaLikers = self.__api.media_likers(post["id"])
        return mediaLikers["users"]


    def __followUser(self, userId):
        result = self.__api.friendships_create(userId)
        return result["status"]

    def __updateStatus(self,newStatus):
        self.__status = newStatus

    def __userFollowsBack(self,userid):
        response = self.__api.friendships_show(userid)
        followedBack = response["followed_by"]
        return followedBack

    def __removeFollow(self,userid):
        self.__api.friendships_destroy(userid)

    #TODO: Need to be tested!
    def __removeNotFollowingBack(self):
        if(not self.__api == None):
            self.__updateStatus(Status.working)
            users = self.__dbmanager.getAllUsers()
            logging.info("Removing users not following back!")
            for user in users:
                logging.info("Checking user: " + user["username"])
                if (("removed" in user and user["removed"] == False) or ("removed" not in user)):
                    # check if user follows you
                    if (self.__userFollowsBack(user["id"]) == False):
                        time.sleep(5)
                        self.__removeFollow(user["id"])
                        self.__dbmanager.updateRemovedFlag(user["id"],True)
                        logging.info("User: " + user["username"] + " removed")
                    else:
                        logging.info("User: " + user["username"] + " is following you back!")
                # wait random time
                randomTime = randint(20, 40)
                time.sleep(randomTime)
            self.__updateStatus(Status.paused)

    def __work(self):
        if(not self.__api == None):
            self.__updateStatus(Status.working)
            following = []
            # init
            if os.path.exists("following.json"):
                following = self.__readFollowingFile()
                logging.info("following.json file exists and retrived!")
            else:
                following = self.__createFollowingFile()
                logging.info("following.json file create")

            while self.__status == Status.working:
                # create a random time in between i follow
                timeToWait = randint(10, 30) * 60
                logging.info("Cylce time sleep : " + str(timeToWait))
                # based on my first following all of my neach i select one
                user_cavia = self.__findRandomUser(following)
                time.sleep(1)
                logging.info("User cavia : " + str(user_cavia["username"]))

                # get the last user post
                lastpost = self.__findLastUserPost(user_cavia)
                time.sleep(1)
                logging.info("Last post for user_cavia : " + str(lastpost["pk"]))
                # get all the users who liked that post
                users = self.__findMediaLikers(lastpost)
                time.sleep(1)
                logging.info("Retrived users who liked!")

                # calculate how many user i need to follow
                usersToFollow = randint(3, 10);

                #check that the post has at lest 3-10 likes
                if(usersToFollow>=len(users)):
                    #else i will follow all the users in the list
                    usersToFollow = len(users)
                logging.info("Users to follow: " + str(usersToFollow))

                for i in range(usersToFollow):
                    # get random user from the list
                    randomIndex = randint(0, len(users)-1)
                    status = self.__followUser(users[randomIndex]["pk"])

                    #saving on db
                    self.__dbmanager.addUser(users[randomIndex])

                    #loggind and next follow random time
                    waitForNextFollow = randint(5, 20)
                    logging.info("followed user: " + str(users[randomIndex]["username"]) + " following status: " + str(
                        status) + ", wait for next follower : " + str(waitForNextFollow) + " sec")
                    time.sleep(waitForNextFollow)

                if(self.__status == Status.working):
                    logging.info("Cycle done! start waiting next cycle!")
                    time.sleep(timeToWait)
                else:
                    logging.info("Bot completed the work and is currently gone with status: "+str(self.__status))
