roomList = []
#constructor
def __init__(self):
	pass

#add user to list
def addTo(room):
	roomList.append(room)

#remove user from list
def removeFrom(room):
	roomList.remove(room)

#find user from list
def find(roomId):
	for i in range(len(roomList)):
		if roomId in roomList:
			return roomList[i]
	return
