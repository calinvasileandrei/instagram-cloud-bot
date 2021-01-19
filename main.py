from flask import Flask,request, jsonify
from bot.bot import InstagramCloudBot
import os
from bot.status import Status,Operation
from bot.localdb.db_manager import DBmanager
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
global bot

@app.route('/')
def hello_world():
    return 'Welcome to Instagram Cloud Bot! '

@app.route('/work',methods=['GET'])
def work():
    global bot

    if(bot is None):
        username = os.getenv("username")
        password = os.getenv("password")
        bot = InstagramCloudBot(username,password,Operation.work)
        bot.start()
        status = bot.status()
        return jsonify({"status": 200, "bot_status": str(status), "message": "Bot created and started!"})
    else:
        status = bot.status()
        if(status == Status.offline or status == Status.paused):
            bot.__work()
            return jsonify({"status": 200, "bot_status": str(status), "message": "Bot is working again!"})
        else:
            return jsonify({"status": 200, "bot_status": str(status), "message": "Bot is already working!"})


@app.route('/unfollowall',methods=['GET'])
def unfollowall():
    global bot
    if(bot is None):
        username = os.getenv("username")
        password = os.getenv("password")
        bot = InstagramCloudBot(username,password,Operation.unfollowall)
        bot.start()
        status = bot.status()
        return jsonify({"status": 200, "bot_status": str(status), "message": "Bot created and started with unfollow operation!"})
    else:
        status = bot.status()
        if(status == Status.offline or status == Status.paused):
            bot.__work()
            return jsonify({"status": 200, "bot_status": str(status), "message": "Bot is working again!"})
        else:
            return jsonify({"status": 200, "bot_status": str(status), "message": "Bot is already working!"})

@app.route('/unfollow24h',methods=['GET'])
def unfollow24h():
    global bot
    if(bot is None):
        username = os.getenv("username")
        password = os.getenv("password")
        bot = InstagramCloudBot(username,password,Operation.unfollow24h)
        bot.start()
        status = bot.status()
        return jsonify({"status": 200, "bot_status": str(status), "message": "Bot created and started with unfollow operation!"})
    else:
        status = bot.status()
        if(status == Status.offline or status == Status.paused):
            bot.__work()
            return jsonify({"status": 200, "bot_status": str(status), "message": "Bot is working again!"})
        else:
            return jsonify({"status": 200, "bot_status": str(status), "message": "Bot is already working!"})



@app.route('/stop',methods=['GET'])
def stop():
    global bot
    if(bot is not None):
        status = bot.status()
        if(not status == Status.offline):
            bot.stop()
            return jsonify({"status": 200, "bot_status": str(status), "message": "Bot stopped!"})
        else:
            return jsonify({"status": 200, "bot_status": str(status), "message": "Bot is already offline!"})
    else:
        return jsonify({"status": 200, "bot_status": "offline", "message": "Bot not created/started!"})


@app.route('/status',methods=['GET'])
def status():
    global bot
    if(bot is not None):
        status = bot.status()
        return jsonify({"status": 200, "bot_status": str(status), "message": "Bot status retrieved!"})
    else:
        return jsonify({"status": 200, "bot_status": "offline", "message": "Bot is offline!"})




@app.route('/followingusers',methods=['GET'])
def followingusers():
    global bot
    if(bot is not None):
        status = bot.status()
        users = bot.getBotFollowedUsers()
        return jsonify({"status": 200, "bot_status": str(status), "message": "Bot status retrieved!", "following_users":users})
    else:
        dbmanager = DBmanager()
        users = dbmanager.getAllUsers()
        return jsonify({"status": 200, "bot_status": "offline" ,"message": "Bot status offline, data retrived from db!", "following_users":users})


@app.route('/followingusersnumber',methods=['GET'])
def followingusersnumber():
    global bot
    if(bot is not None):
        status = bot.status()
        usersNumber = bot.getBotFollowingNumber()
        return jsonify({"status": 200, "bot_status": str(status), "message": "Bot status retrieved!", "following_users_number":usersNumber})
    else:
        dbmanager = DBmanager()
        usersNumber = dbmanager.getFollowingNumber()
        return jsonify({"status": 200, "bot_status": "offline" ,"message": "Bot status offline, data retrived from db!", "following_users_number":usersNumber})






if __name__ == '__main__':
    global bot
    bot = None
    app.run()