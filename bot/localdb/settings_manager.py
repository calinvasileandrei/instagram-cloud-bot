from tinydb import TinyDB, Query
from datetime import datetime
from bot.status import SettingOptions
from utils.Singleton import Singleton

class SettingManager(metaclass=Singleton):
    settings= None
    def __init__(self):
        self.settings = TinyDB('settings.json')
        self.__initSettings()

    def __initSettings(self):
        SettingsQuery = Query()
        time_wait_start = self.settings.search(SettingsQuery.name == SettingOptions.time_wait_start.value)
        time_wait_finish = self.settings.search(SettingsQuery.name == SettingOptions.time_wait_finish.value)
        min_users_to_follow =  self.settings.search(SettingsQuery.name == SettingOptions.min_users_to_follow.value )
        max_users_to_follow =  self.settings.search(SettingsQuery.name == SettingOptions.max_users_to_follow.value)
        min_users_to_unfollow = self.settings.search(SettingsQuery.name == SettingOptions.min_users_to_unfollow.value)
        max_users_to_unfollow =  self.settings.search(SettingsQuery.name == SettingOptions.max_users_to_unfollow.value)

        if(not time_wait_start):
            self.__initSingleSetting(SettingOptions.time_wait_start.value, 30)
        if(not time_wait_finish):
            self.__initSingleSetting(SettingOptions.time_wait_finish.value, 45)
        if(not min_users_to_follow):
            self.__initSingleSetting(SettingOptions.min_users_to_follow.value, 3)
        if(not max_users_to_follow):
            self.__initSingleSetting(SettingOptions.max_users_to_follow.value, 10)
        if(not min_users_to_unfollow):
            self.__initSingleSetting(SettingOptions.min_users_to_unfollow.value, 7)
        if(not max_users_to_unfollow):
            self.__initSingleSetting(SettingOptions.max_users_to_unfollow.value, 20)


    def __initSingleSetting(self, setting_option, value):
        return self.settings.insert({"name":setting_option,"value":value})


    def updateSingleSetting(self,setting_option,value):
        SettingQuery = Query()
        return self.settings.update({"value":value},SettingQuery.name == str(setting_option));

    def getSettings(self):
        settings = self.settings.all()
        return settings

    def updateSettings(self,settings_data):
        response_message= "Settings updated: ";
        for setting in settings_data:
            try:
                response_update = self.updateSingleSetting(setting["name"],setting["value"])
                response_message += setting["name"]+" ";
            except Exception as e:
                response_message += "error getting value "
                print("error getting the data,error: ",e);

        return response_message

    def getValueOfSettings(self,settings,setting_name):
        setting= next((item for item in settings if item["name"] == setting_name), None)
        return int(setting["value"])