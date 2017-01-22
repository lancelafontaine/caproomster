idMapList = []
#add instance to list
def add(timeslot):
	idMapList.append(timeslot)
#remove instance from list
def delete(timeslot):
	idMapList.remove(timeslot)
#get instance from list
def get(timeslotId):
	for i in range(len(idMapList)):
		if timeslotId in idMapList:
			return idMapList[i]
	return