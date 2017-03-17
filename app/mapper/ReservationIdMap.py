reservationList = []
#constructor
def __init__(self):
	pass

#add user to list
def addTo(reservation):
    reservationList.append(reservation)

#remove user from list
def removeFrom(reservation):
    reservationList.remove(reservation)

#find user from list
def find(reservationId):
	for i in range(len(reservationList)):
		if reservationId == reservationList[i].getId():
			return reservationList[i]
	return


# Clear the ID Map
def clear():
    del reservationList[:]
