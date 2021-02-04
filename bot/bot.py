from instagram_private_api import Client, ClientCompatPatch
import json
import os
from random import randint
import time
import logging
from threading import Thread
from bot.localdb.db_manager import DBmanager
from bot.localdb.settings_manager import SettingManager
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(
    "debug.log"), logging.StreamHandler()])
from bot.status import Status, Operation


class InstagramCloudBot(Thread):
    __api = None
    __status = Status.offline
    __dbmanager = None
    __settings_manager = None
    __operation = None
    #TODO:Implement This whit api post, default are:
    __time_wait_start = 30 #minutes
    __time_wait_finish = 45 ##minutes
    __min_users_to_follow = 3
    __max_users_to_follow = 10
    __min_users_to_unfollow = 7
    __max_users_to_unfollow = 20


    def __init__(self, _username, _password, _operation):
        super().__init__()
        self.__api = Client(_username, _password)
        self.__dbmanager = DBmanager()
        self.__operation = _operation


    def run(self):
        if (self.__operation == Operation.work):
            self.__loadSettings()
            self.__work()
        elif (self.__operation == Operation.unfollowall):
            self.__removeNotFollowingBack(False, Status.paused)
        elif (self.__operation == Operation.unfollow24h):
            self.__removeNotFollowingBack(True,
                                          Status.paused)  # remove only the one which i have followed at least 24h ago

    def getBotFollowedUsers(self):
        return self.__dbmanager.getAllUsers()

    def getBotFollowingNumber(self):
        return self.__dbmanager.getFollowingNumber()

    def stop(self):
        self.__updateStatus(Status.offline)

    def status(self):
        return self.__status

    # private
    def __loadSettings(self):
        self.__settings_manager = SettingManager()
        settings = self.__settings_manager.getSettings()
        self.__time_wait_start = self.__settings_manager.getValueOfSettings(settings, "time_wait_start")
        self.__time_wait_finish = self.__settings_manager.getValueOfSettings(settings, "time_wait_finish")
        self.__min_users_to_follow = self.__settings_manager.getValueOfSettings(settings, "min_users_to_follow")
        self.__max_users_to_follow = self.__settings_manager.getValueOfSettings(settings, "max_users_to_follow")
        self.__min_users_to_unfollow = self.__settings_manager.getValueOfSettings(settings, "min_users_to_unfollow")
        self.__max_users_to_unfollow = self.__settings_manager.getValueOfSettings(settings, "max_users_to_unfollow")

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
        userChoosen = randint(0, maxFollowing - 1)
        return following[userChoosen]

    def __findLastUserPost(self, user):
        try:
            feed = self.__api.username_feed(user["username"])
        except:
            return None
        if (len(feed["items"]) > 0):
            lastPost = feed["items"][0]
            return lastPost

    def __findMediaLikers(self, post):
        mediaLikers = self.__api.media_likers(post["id"])
        return mediaLikers["users"]

    def __followUser(self, userId):
        result = self.__api.friendships_create(userId)
        return result["status"]

    def __updateStatus(self, newStatus):
        self.__status = newStatus

    def __userFollowsBack(self, userid):
        response = self.__api.friendships_show(userid)
        followedBack = {"following_back": response["followed_by"], "following": response["following"]}
        return followedBack

    def __removeFollow(self, userid):
        self.__api.friendships_destroy(userid)

    def __findValidUserCaviaPost(self, following):
        findCavia = True
        user_cavia = None
        lastpost = None
        while findCavia:
            user_cavia = self.__findRandomUser(following)
            time.sleep(1)
            logging.info("User cavia : " + str(user_cavia["username"]))

            # get the last user post
            lastpost = self.__findLastUserPost(user_cavia)
            if (lastpost is not None):
                logging.info("User Cavia not accepted for some reasons like private user!")
                findCavia = False
            time.sleep(2)

        return user_cavia, lastpost

    def __existsUserInDB(self, id):
        return self.__dbmanager.existsUser(id)

    def __generaterandomUser(self, users):
        generate = True
        randomUser = None
        while generate:
            randomIndex = randint(0, len(users) - 1)
            randomUser = users[randomIndex]
            # TODO: check if in db
            if not self.__existsUserInDB(randomUser["pk"]):
                generate = False

        return randomUser

    # TODO: Need to be tested!
    def __removeNotFollowingBack(self, removeLastDayFollowers, statusAfter):
        if (not self.__api == None):
            self.__updateStatus(Status.working)

            if (removeLastDayFollowers):
                users = self.__dbmanager.getAllUsersAdded24h()
            else:
                users = self.__dbmanager.getAllUsers()

            logging.info("Removing users not following back!")
            position = 0
            usersToUnFollow = randint(self.__min_users_to_unfollow, self.__max_users_to_unfollow)
            logging.info("Number of users to unfollow: " + str(usersToUnFollow))
            counter_removed = 0
            for user in users:
                if(counter_removed >= usersToUnFollow):
                    break
                position += 1
                logging.info("[" + str(counter_removed) + "/" + str(len(usersToUnFollow)) + "] Removed | Checking user ["+str(position)+"/"+str(len(users))+"]: " + user["username"])
                if (not ("removed" in user and user["removed"] == True)):
                    # check if user follows you
                    relationship = self.__userFollowsBack(user["id"])
                    if (relationship["following_back"] == False and relationship["following"] == True):
                        time.sleep(5)
                        self.__removeFollow(user["id"])
                        self.__dbmanager.updateRemovedFlag(user["id"], True)
                        logging.info("User: " + user["username"] + " removed")
                        counter_removed+=1
                        # wait random time
                        randomTime = randint(20, 40)
                        time.sleep(randomTime)
                    else:
                        if (relationship["following_back"] == True and relationship["following"] == True):
                            logging.info("User: " + user["username"] + " has a friendship relation!")
                            self.__dbmanager.updateRemovedFlag(user["id"], False)
                        elif (relationship["following_back"] == True and relationship["following"] == False):
                            logging.info("User: " + user["username"] + " is your follower!")
                            self.__dbmanager.updateRemovedFlag(user["id"], False)
                        else:
                            logging.info("User: " + user["username"] + " has no relation with you !")
                            self.__dbmanager.updateRemovedFlag(user["id"], True)
                            logging.info("User: " + user["username"] + " removed")

                        # wait random time
                        randomTime = randint(3, 10)
                        time.sleep(randomTime)
                else:
                    time.sleep(1)
            logging.info("Process of unfllowing done!")
            self.__updateStatus(statusAfter)

    def __work(self):
        if (not self.__api == None):
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

                timeToWait = randint(self.__time_wait_start, self.__time_wait_finish) * 60
                logging.info("Cylce time sleep : " + str(timeToWait / 60) + "minutes")

                # based on my first following all of my neach i select one
                user_cavia, lastpost = self.__findValidUserCaviaPost(following)

                logging.info("Last post for user_cavia : " + str(lastpost["pk"]))
                # get all the users who liked that post
                users = self.__findMediaLikers(lastpost)
                time.sleep(2)
                logging.info("Retrived users who liked!")

                # calculate how many user i need to follow
                usersToFollow = randint(self.__min_users_to_follow, self.__max_users_to_follow);

                # check that the post has at lest 3-10 likes
                if (usersToFollow >= len(users)):
                    # else i will follow all the users in the list
                    usersToFollow = len(users)
                logging.info("Users to follow: " + str(usersToFollow))

                for i in range(usersToFollow):
                    # get random user from the list
                    randomUser = self.__generaterandomUser(users)
                    status = self.__followUser(randomUser["pk"])
                    # saving on db
                    self.__dbmanager.addUser(randomUser)

                    # loggind and next follow random time
                    waitForNextFollow = randint(5, 20)
                    logging.info("followed user: " + str(randomUser["username"]) + " following status: " + str(
                        status) + ", wait for next follower : " + str(waitForNextFollow) + " sec")
                    time.sleep(waitForNextFollow)

                if (self.__status == Status.working):
                    logging.info("Cycle of follows done!")
                    logging.info("Cycle of unnfollow last day followers started...")
                    time.sleep(60)
                    self.__removeNotFollowingBack(True, Status.working)
                    logging.info("Cycle done! start waiting next cycle!")
                    time.sleep(timeToWait)

                else:
                    logging.info("Bot completed the work and is currently gone with status: " + str(self.__status))
