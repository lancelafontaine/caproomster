from app.TDG import WaitingTDG
from app.TDG import ReservationTDG

#waitingList: list containing (waitingId, room, reservee, description, timeslotid, starttime, endtime) entries
#availabilityList: availabilities for that room (array of strings)
def updateWaiting(roomId, date, availabilityList):
	i = 0
	print(availabilityList)
	waitingList = WaitingTDG.findByRoom(roomId, date)
	if waitingList is None:
		return
	else:
		for w in waitingList:
			for a in availabilityList:

				if a == "Available" and availabilityList[i+1]=="unavailable" and (i+10)!=21:
					print("first if")
					if w[5]==(i+9) and w[6]==(i+9):
						ReservationTDG.insertDirect(w[1],w[3],w[2],w[4])
						WaitingTDG.delete(w[0])
						return
				elif a == "Available" and availabilityList[i+1]=="Available" and (i+10)!=20:
					print("first elif")
					if w[5]==(i+9) and w[6]==(i+10):
						print("first elif if")
						ReservationTDG.insertDirect(w[1], w[3], w[2], w[4])
						WaitingTDG.delete(w[0])
						return
				elif (i+10)==21 and a == "Available":
					print("second elif")
					if w[5]==21 and w[6]==21:
						print("second elif if")
						ReservationTDG.insertDirect(w[1], w[3], w[2], w[4])
						WaitingTDG.delete(w[0])
						return
			i = i + 1