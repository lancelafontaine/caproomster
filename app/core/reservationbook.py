from reservation import Reservation
from waiting import Waiting
from collections import deque
from datetime import datetime
from app.mapper import ReservationMapper
from app.mapper import WaitingMapper
from app.mapper import UnitOfWork


# ReservationBook object
class ReservationBook(object):
	def __init__(self):
		self.reservationList = deque()
		self.waitingListRegular = deque()
		self.waitingListCapstone = deque()

	# Constructor
	def __init__(self, reservationlist, waitinglist, capstoneList):
		self.reservationList = reservationlist
		self.waitingListRegular = waitinglist
		self.waitingListCapstone = capstoneList

	# Method to make a reservation
	def makeReservation(self, room, holder, time, description):
		# Check if room is available at specifie time
		if (self.available(room, time) == True):
			r = Reservation(room, holder, time, description)
			self.reservationList.append(r)
			UnitOfWork.registerNew(r)
			ReservationMapper.done()

	# Method to add to the waiting list
	def addToWaitingList(self, room, holder, time, description):
		w = Waiting(room, holder, time, description, self.genWid())
		if w.getUser().isCapstone():
			self.waitingListCapstone.append(w)
		else:
			self.waitingListRegular.append(w)
		print(w)
		UnitOfWork.registerNew(w)
		WaitingMapper.done()

	# Method to modify reservation
	def modifyReservation(self, reservationId, time):
		r = self.getReservationById(reservationId)
		if self.available(r.getRoom(), r.getTimeslot(), reservationId):
			r.setTimeslot(time)

	# Method to cancel reservation
	def cancel(self, reservationId):
		r = self.getReservationById(reservationId)
		print(self.reservationList)
		# self.reservationList.remove(r)
		ReservationMapper.delete(reservationId)

	# Method to update the waiting list
	def updateWaiting(self, roomId):
		# Iterate over a queue of all reservations in specify room
		for w in self.getListByRoom(roomId):
			if self.available(w.getRoom(), w.getTimeslot()):
				if not self.isRestricted(w.getUser(), w.getTimeslot()):
					r = Reservation(w.getRoom(), w.getUser(), w.getTimeslot(), w.getDescription(), self.genRid())
					self.reservationList.append(r)
					if w.getUser().isCapstone():
						self.waitingListCapstone.remove(w)
					else:
						self.waitingListRegular.remove(w)
					break

	# Method to view all reservations
	def view(self):
		return self.display()

	# Method that return all reservations
	def display(self):
		return self.getReservationList()

	# Method that return a reservation based on Id
	def getReservationById(self, reservationId):
		for r in self.reservationList:
			if r.getId() == reservationId:
				return r

	# Method to get a queue of all Waiting
	def getListByRoom(self, roomId):
		wList = deque()

		# First get all capstone students
		for w in self.waitingListCapstone:
			if w.getRoom() == roomId:
				wList.append(w)

		# Then add the regular students at end
		for w in self.waitingListRegular:
			if w.getRoom() == roomId:
				wList.append(w)

		return wList

	# Method to check if the timeslot is available, also overloaded for modifyReservation case
	def available(self, room, time, rid=None):
		isAvailable = True
		for r in self.reservationList:
			if r.getId() == rid:
				continue
			if r.getRoom() == room:
				t = r.getTimeslot()
				# Check if same date
				if t.getDate() == time.getDate():
					# Check if same start time
					if t.getStartTime() == time.getStartTime():
						isAvailable = False
					# Check if same end time
					if t.getEndTime() == time.getEndTime():
						isAvailable = False
					# Check if the time overlaps with each other
					if t.getStartTime() < time.getStartTime() and time.getEndTime() < t.getEndTime():
						isAvailable = False

		if isAvailable == False:
			print("Timeslot is unavailable")
		return isAvailable

	# Method to view MY reservations
	def viewMyReservations(self, user):
		myReservationList = []
		for r in self.reservationList:
			if (r.getUser() == user):
				myReservationList.append(r)
		return myReservationList

	# Print method for current number of reservations and waitings in the system
	def printNb(self):
		print("Nb of Reservations: " + str(len(self.reservationList)))
		print("Nb of Waiting: " + str(len(self.waitingListRegular)))

	# Method to generate reservationId
	def genRid(self):
		if len(self.reservationList) !=0:
			largeList = []
			# Find the largest ID
			for r in self.reservationList:
				largeList.append(r.getId())
			return max(largeList) + 1
		else:
			return 1

	# Method to generate waitingId
	def genWid(self):
		if len(self.waitingListRegular) != 0:
			largeList = []
			for w in self.waitingListRegular:
				largeList.append(w.getId())
			return max(largeList) + 1
		else:
			return 1

	# Method to generate timeslotId
	def genTid(self):
		timeslotList = []
		for w in self.waitingListRegular:
			timeslotList.append(w.getTimeslot())
		for r in self.reservationList:
			timeslotList.append(r.getTimeslot())

		if len(timeslotList) != 0 :
			largeList = []
			for t in timeslotList:
				largeList.append(t.getId())
			return max(largeList) + 1
		else:
			return 1

	# Method for restriction
	def isRestricted(self, user, time):
		restrictions = False
		nbMyReservationInWeek = 0

		# Get week nb of specify Timeslot
		date1 = time.getDate()
		day1 = int(date1[8:10])
		month1 = int(date1[5:7])
		year1 = int(date1[0:4])
		dt1 = datetime(year1, month1, day1)
		wk1 = dt1.isocalendar()[1]

		for r in self.viewMyReservations(user):
			# Get week nb
			date2 = r.getTimeslot().getDate()
			day2 = int(date2[8:10])
			month2 = int(date2[5:7])
			year2 = int(date2[0:4])
			dt2 = datetime(year2, month2, day2)
			wk2 = dt2.isocalendar()[1]
			# Compare if week nb matches
			if wk1 == wk2:
				nbMyReservationInWeek = nbMyReservationInWeek + 1
			# Check if user is attempting to make another reservation on same day
			if r.getTimeslot().getDate() == time.getDate():
				restrictions = True
				print("Request Failed: Only one reservation per day.")
				break
		# Check if user is at max reservation
		if nbMyReservationInWeek >= 3:
			restrictions = True
			print("Request Failed: At maximum number of reservations for this week.")

		return restrictions

	# Accessors and Mutators
	def getReservationList(self):
		return self.reservationList

	def setReservationList(self, reservationList):
		self.reservationList = reservationList

	def getRegularWaitingList(self):
		return self.waitingListRegular

	def setRegularWaitingList(self, waitingList):
		self.waitingListRegular = waitingList

	def getCapstoneWaitingList(self):
		return self.waitingListCapstone

	def setCapstoneWaitingList(self, waitingList):
		self.waitingListCapstone = waitingList