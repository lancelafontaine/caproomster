idMapList = []
#add instance to list
def add(waiting):
    idMapList.append(waiting)
#remove instance from list
def delete(waiting):
    idMapList.remove(waiting)
#get instance from list
def get(waitingId):
    for i in range(len(idMapList)):
        if waitingId in idMapList:
            return idMapList[i]
    return

def getRoomOnDate(room,date):
    waitingList = []
    for waiting in idMapList:
        if waiting[1] == room and waiting[2] == date:
            waitingList.append(waiting)
    return waitingList



