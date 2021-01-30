from enum import Enum

class Status(Enum):
    offline = "offline"
    working = "working"
    paused = "paused"


class Operation(Enum):
    work = "work"
    unfollowall = "unfollowall"
    unfollow24h = "unfollow24h"

class HeuristisStatus(Enum):
    waitToFollowNextUser= "waitToFollowNextUser"
    waitNextCycle = "waitNextCycle"
    waitUserDelete = "waitUserDelete"
    waitSimpleOperation = "waitSimpleOperation"
    waitComplexOperation = "waitSimpleOperation"


class SettingOptions(Enum):
    time_wait_start ="time_wait_start"
    time_wait_finish ="time_wait_finish"
    min_users_to_follow = "min_users_to_follow"
    max_users_to_follow ="max_users_to_follow"
    min_users_to_unfollow ="min_users_to_unfollow"
    max_users_to_unfollow ="max_users_to_unfollow"
