from bot.localdb.settings_manager import SettingManager
from bot.status import SettingOptions

settings_manager = SettingManager()
#settings_manager.updateSingleSetting(SettingOptions.time_wait_start,100)

settings = settings_manager.getSettings()

val = settings_manager.getValueOfSettings(settings,"time_wait_start")
print(val)