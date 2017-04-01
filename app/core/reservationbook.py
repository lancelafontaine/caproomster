from reservation import Reservation
from waiting import Waiting
from collections import deque
from datetime import datetime
from datetime import timedelta
from app.mapper import ReservationMapper
from app.mapper import WaitingMapper
from app.mapper import TimeslotMapper
from app.mapper import UnitOfWork
from app.core.equipment import Equipment
from app.core.timeslot import Timeslot

from uuid import uuid4


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
	def makeReservation(self, room, holder, timeslot, description, equipment):
		# Check if room is timeslot is available and equipment also
		if self.isTimeslotAvailableforRoom(room, timeslot) \
				and self.isEquipmentAvailableForTimeSlot(timeslot, equipment):
			r = Reservation(room, holder, timeslot, description, equipment, str(uuid4()))
			self.reservationList.append(r)
			UnitOfWork.registerNew(r)
			ReservationMapper.done()

	# Method to add to the waiting list
	def addToWaitingList(self, room, holder, timeslot, description, equipment):
		w = Waiting(room, holder, timeslot, description, equipment, str(uuid4()))
		if w.getUser().isCapstone():
			self.waitingListCapstone.append(w)
		else:
			self.waitingListRegular.append(w)
		UnitOfWork.registerNew(w)
		WaitingMapper.done()

	# Method to modify reservation
	def modifyReservation(self, reservationId, timeslot):
		r = self.getReservationById(reservationId)
		if self.isTimeslotAvailableforRoom(r.getRoom(), r.getTimeslot(), reservationId) \
				and self.isEquipmentAvailableForTimeSlot(r.getTimeslot(), r.getEquipment()):
			r.setTimeslot(timeslot)

	# Method to cancel reservation
	def cancel(self, reservationId):
		r = self.getReservationById(reservationId)
		print(self.reservationList)
		# self.reservationList.remove(r)
		ReservationMapper.delete(reservationId)

	# Method to update the waiting list
	def updateWaiting(self, roomId):
		# Iterate over a queue of all reservations in specify room
		for w in self.getWaitlistForRoom(roomId):
			if self.isTimeslotAvailableforRoom(w.getRoom(), w.getTimeslot()) \
					and self.isEquipmentAvailableForTimeSlot(w.getTimeslot(), w.getEquipment()):
				if not self.isRestricted(w.getUser(), w.getTimeslot()):
					r = Reservation(w.getRoom(), w.getUser(), w.getTimeslot(), w.getDescription(), w.getEquipment(),
					                str(uuid4()))
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
	def getWaitlistForRoom(self, roomId):
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

	# Method to check if the timeslot is isTimeslotAvailableforRoom, also overloaded for modifyReservation case
	def isTimeslotAvailableforRoom(self, room, timeslot, rid=None):
		for r in self.reservationList:
			if r.getRoom() == room and timeslot.overlaps(r.getTimeslot()):
				return False
		return True

	def isEquipmentAvailableForTimeSlot(self, timeslot, equipment):
		# type: (Timeslot, Equipment) -> bool
		currentEquipmentAvailable = self.getAllEquipmentAvailableAtTimeslot(timeslot)
		for type, quantity in equipment.equipment.iteritems():
			amountAvailable = currentEquipmentAvailable.equipment[type]
			currentEquipmentAvailable.equipment[type] = amountAvailable - quantity
		return len(currentEquipmentAvailable) >= 0

	def getAllEquipmentAvailableAtTimeslot(self, timeslot):
		"""

		:rtype: Equipment
		"""
		maxEquipmentAvailable = Equipment("equipmentID_uvu",laptops=3, projectors=3, whiteboards=3)
		# iterate through reservations list, get total equipment already reserved
		for r in self.getAllReservationsForTimeslot(timeslot):
			for type, quantity in r.getEquipment().equipment.iteritems():
				amountAvailable = maxEquipmentAvailable.equipment[type]
				maxEquipmentAvailable.equipment[type] = amountAvailable - quantity
		return maxEquipmentAvailable

	def getAllReservationsForTimeslot(self, timeslot):
		listOfReservations = []
		for r in self.reservationList:
			if r.getTimeslot().overlaps(timeslot):
				listOfReservations.append(r)
		return listOfReservations

	# Method to view MY reservations
	def getUserReservations(self, user):
		userReservations = []
		for r in self.reservationList:
			if (r.getUser() == user):
				userReservations.append(r)
		return userReservations

	# Print method for current number of reservations and waitings in the system
	def printNb(self):
		print("Nb of Reservations: " + str(len(self.reservationList)))
		print("Nb of Waiting: " + str(len(self.waitingListRegular)))

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

		for r in self.getUserReservations(user):
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

	def makeRepeatedReservation(self, room, user, timeslot, description, equipment, repeat_amount):
		max_repetition = 2
		days_in_a_week = 7

		# safe guard if repeat amount is greater than max repetition
		if repeat_amount > max_repetition:
			repeat_amount = max_repetition

		# filter date values
		date_split_list = timeslot.getDate().split('-')
		year = int(date_split_list[0])
		month = int(date_split_list[1])
		day = int(date_split_list[2])

		# Create datetime object
		reservation_date = datetime(year, month, day)

		# repeatAmount + 1 : because at least 1 reservation should be made
		for i in range(repeat_amount + 1):
			# create and register a timeslot object
			timeslot.setDate(reservation_date.strftime('%Y-%m-%d'))
			timeslot = TimeslotMapper.makeNew(timeslot.getStartTime(), timeslot.getEndTime(), timeslot.getDate(),
			                                  timeslot.getBlock(), user.getId())
			TimeslotMapper.save(timeslot)
			timeslot_id = TimeslotMapper.findId(user.getId())
			timeslot.setId(timeslot_id)

			# create and register a reservation object
			reservation = ReservationMapper.makeNew(room, user, timeslot, description, equipment, timeslot_id)
			self.reservationList.append(reservation)
			# add a week to the current reservation date
			reservation_date += timedelta(days=days_in_a_week)

	@staticmethod
	def find_total_reserved_time_for_user_for_a_given_week(user_id, date):
		diff_between_monday_and_sunday = 6
		total_time = 0
		# filter date values
		date_split_list = date.split('-')
		year = int(date_split_list[0])
		month = int(date_split_list[1])
		day = int(date_split_list[2])

		# Create datetime object
		reservation_date = datetime(year, month, day)

		# find start of the week
		monday_date = reservation_date - timedelta(days=reservation_date.weekday())

		sunday_date = monday_date + timedelta(days=diff_between_monday_and_sunday)

		user_timeslot_list = TimeslotMapper.find_all_timeslots_for_user(user_id)
		for timeslot in user_timeslot_list:

			reservation_date = datetime(timeslot[3].year, timeslot[3].month, timeslot[3].day)

			# check if reservation_date lies between monday and sunday.
			if monday_date < reservation_date < sunday_date:
				total_time += timeslot[4]

		return total_time