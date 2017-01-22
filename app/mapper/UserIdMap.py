userList = []
#constructor
def __init__(self):
	pass

#add user to list
def addTo(user):
	userList.append(user)

#remove user from list
def removeFrom(user):
	userList.remove(user)

#find user from list
def find(userId):
	for i in range(len(userList)):
		if userId == userList[i].getId():
			return userList[i]
	return
