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
