import pytest
from app.core.reservationbook import ReservationBook
from app.core.timeslot import Timeslot
from app.core.user import User
from app.mapper import UnitOfWork
from app.mapper import WaitingMapper
from collections import deque

"""Tests whether students get added to the appropriate waitlist based on capstone flag"""
def test_add_to_appropriate_waiting_list(monkeypatch):
	# Initialization
	reservationBook = ReservationBook([], [], [])

	# mock
	def mockUOW_registernew(_):
		pass

	def mockWaitingMapperDone():
		pass

	monkeypatch.setattr(UnitOfWork, 'registerNew', mockUOW_registernew)
	monkeypatch.setattr(WaitingMapper, 'done', mockWaitingMapperDone)

	# check the size of the waitlist for capstone
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.waitingListRegular) == 0

	# execute
	reservationBook.addToWaitingList(2, User(3, 'usrname', 'pass', True),
	                                 Timeslot(11, 13, '2017-03-25', 2, 4567), 'desc')
	# verify
	assert len(reservationBook.waitingListCapstone) == 1

	# execute
	reservationBook.addToWaitingList(2, User(4, 'usrname', 'pass', False),
	                                 Timeslot(11, 13, '2017-03-25', 2, 4567), 'desc')
	# verify
	assert len(reservationBook.waitingListRegular) == 1

	# execute
	reservationBook.addToWaitingList(2, User(5, 'usrname', 'pass', False),
	                                 Timeslot(11, 13, '2017-03-25', 2, 4567), 'desc')
	# verify
	assert len(reservationBook.waitingListRegular) == 2

#
def test_update_waiting(monkeypatch):
	# Initialization
	reservationBook = ReservationBook([], [], [])

	# mock
	def mockUOW_registernew(_):
		pass

	def mockWaitingMapperDone():
		pass

	monkeypatch.setattr(UnitOfWork, 'registerNew', mockUOW_registernew)
	monkeypatch.setattr(WaitingMapper, 'done', mockWaitingMapperDone)

	"""Populating the list with 2 regular students,
	1 capstone student all in room 5, in that order.
	This was already tested in test_add_to_appropriate_waiting_list()"""
	#putting regular student into waitlist at room 5
	reservationBook.addToWaitingList(5, User(3, 'mary', 'pass', False),
	                                 Timeslot(11, 13, '2017-03-25', 2, 1243), 'desc')

	#putting regular student into waitlist at room 5
	reservationBook.addToWaitingList(5, User(4, 'john', 'pass', False),
	                                 Timeslot(11, 13, '2017-03-25', 2, 1246), 'desc')

	#putting regular student into waitlist at room 5
	reservationBook.addToWaitingList(5, User(1, 'gary', 'pass', False),
	                                 Timeslot(11, 13, '2017-03-25', 2, 1248), 'desc')

	#putting capstone student into waitlist at room 5
	reservationBook.addToWaitingList(5, User(5, 'emir', 'pass', True),
	                                 Timeslot(11, 13, '2017-03-25', 2, 1234), 'desc')

	#putting regular student into waitlist at room 5
	reservationBook.addToWaitingList(5, User(6, 'cody', 'pass', False),
	                                 Timeslot(11, 13, '2017-03-25', 2, 1222), 'desc')

	#putting capstone student into waitlist at room 5
	reservationBook.addToWaitingList(5, User(7, 'mark', 'pass', True),
	                                 Timeslot(11, 13, '2017-03-25', 2, 1212), 'desc')

	assert len(reservationBook.waitingListRegular) == 4
	assert len(reservationBook.waitingListCapstone) == 2
	assert len(reservationBook.reservationList) == 0

	#Execute
	reservationBook.updateWaiting(5)

	"""The user with the highest priority has been popped out of the whole waitlist."""
	#Verify
	assert len(reservationBook.waitingListRegular) == 4
	assert len(reservationBook.waitingListCapstone) == 1
	assert len(reservationBook.reservationList) == 1

	"""Making sure the user is the first capstone student at the top of the list"""
	assert reservationBook.reservationList[0].getUser().getName() == 'emir'

	"""Calling update again, this should not change the waitlists since """
	#Execute
	reservationBook.updateWaiting(5)
	assert len(reservationBook.waitingListRegular) == 4
	assert len(reservationBook.waitingListCapstone) == 1
	assert len(reservationBook.reservationList) == 1

	"""Calling update again, this should not change the waitlists since """
	#Execute
	reservationBook.updateWaiting(5)
	assert len(reservationBook.waitingListRegular) == 4
	assert len(reservationBook.waitingListCapstone) == 1
	assert len(reservationBook.reservationList) == 1

	""""Toying around with update, clearing the reservationlist, this can be done with a method"""
	reservationBook.reservationList = []
	assert len(reservationBook.waitingListRegular) == 4
	assert len(reservationBook.waitingListCapstone) == 1
	assert len(reservationBook.reservationList) == 0

	reservationBook.updateWaiting(5)
	assert len(reservationBook.waitingListRegular) == 4
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 1

	"""Making sure that the user in the reservation list is Mark"""
	assert reservationBook.reservationList[0].getUser().getName() == "mark"

	""""Toying around with update, clearing the reservationlist, this can be done with a method"""
	reservationBook.reservationList = []
	assert len(reservationBook.waitingListRegular) == 4
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 0

	reservationBook.updateWaiting(5)
	assert len(reservationBook.waitingListRegular) == 3
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 1

	"""Making sure that the user in the reservation list is Mary"""
	assert reservationBook.reservationList[0].getUser().getName() == "mary"

	""""Toying around with update, clearing the reservationlist, this can be done with a method"""
	reservationBook.reservationList = []
	assert len(reservationBook.waitingListRegular) == 3
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 0

	reservationBook.updateWaiting(5)
	assert len(reservationBook.waitingListRegular) == 2
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 1

	"""Making sure that the user in the reservation list is John"""
	assert reservationBook.reservationList[0].getUser().getName() == "john"

	""""Toying around with update, clearing the reservationlist, this can be done with a method"""
	reservationBook.reservationList = []
	assert len(reservationBook.waitingListRegular) == 2
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 0

	reservationBook.updateWaiting(5)
	assert len(reservationBook.waitingListRegular) == 1
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 1

	"""Making sure that the user in the reservation list is Gary"""
	assert reservationBook.reservationList[0].getUser().getName() == "gary"

	""""Toying around with update, clearing the reservationlist, this can be done with a method"""
	reservationBook.reservationList = []
	assert len(reservationBook.waitingListRegular) == 1
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 0

	reservationBook.updateWaiting(5)
	assert len(reservationBook.waitingListRegular) == 0
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 1

	"""Making sure that the user in the reservation list is Cody"""
	assert reservationBook.reservationList[0].getUser().getName() == "cody"

	"""At this point the list is empty, both regular and capstone"""
	""""Toying around with update, clearing the reservationlist, this can be done with a method"""
	reservationBook.reservationList = []
	assert len(reservationBook.waitingListRegular) == 0
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 0

	reservationBook.updateWaiting(5)
	assert len(reservationBook.waitingListRegular) == 0
	assert len(reservationBook.waitingListCapstone) == 0
	assert len(reservationBook.reservationList) == 0

	"""Since both waitlists are empty, reservation remains empty upon update"""
	assert reservationBook.reservationList == []