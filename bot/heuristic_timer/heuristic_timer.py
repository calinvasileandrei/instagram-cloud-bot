from bot.status import HeuristisStatus

class HeuristiTimer:

    def __init__(self):
        pass

    def generateTime(self,status):
        if(status == HeuristisStatus.waitNextCycle ):
            pass
        elif(status == HeuristisStatus.waitUserDelete ):
            pass
        elif(status == HeuristisStatus.waitToFollowNextUser ):
            pass
        elif (status == HeuristisStatus.waitSimpleOperation):
            pass
        elif (status == HeuristisStatus.waitComplexOperation):
            pass
        else:
            pass
