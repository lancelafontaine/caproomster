idMapList = []

#add instance to list
def addTo(timeslot):
	idMapList.append(timeslot)

#remove instance from list
def removeFrom(timeslot):
	idMapList.remove(timeslot)

#get instance from list
def find(timeslotId):
	for i in range(len(idMapList)):
		if timeslotId == idMapList[i].getId():
			return idMapList[i]
	return

# Clear the ID Map
def clear():
  del idMapList[:]
