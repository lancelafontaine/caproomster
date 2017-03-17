idMapList = []
#add instance to list
def addTo(waiting):
    idMapList.append(waiting)

#remove instance from list
def removeFrom(waiting):
    idMapList.remove(waiting)

#get instance from list
def find(waitingId):
    for i in range(len(idMapList)):
        if waitingId == idMapList[i].getId():
            return idMapList[i]
    return

# Clear the ID Map
def clear():
    del idMapList[:]
