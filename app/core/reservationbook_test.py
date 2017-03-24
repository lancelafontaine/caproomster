import pytest
from app.core.reservationbook import ReservationBook
from app.core.timeslot import Timeslot
from app.core.user import User
from app.mapper import UnitOfWork
from app.mapper import WaitingMapper
from collections import deque

"""Tests whether a capstone student really has priority over a regular student in the waitlist"""

def test_addToWaitingList(monkeypatch):
	#mock
	def mockUOW_registernew(_):
		pass

	def mockWaitingMapperDone():
		pass

	monkeypatch.setattr(UnitOfWork,'registerNew',mockUOW_registernew("dummy arg"))
	monkeypatch.setattr(WaitingMapper,'done',mockWaitingMapperDone())

	#execute
	ReservationBook.addToWaitingList(ReservationBook(deque(),deque(),deque()),2,User(3,'usrname','pass',True),Timeslot(11,13,'2017-03-25',2,4567),'desc')

	#verify
	assert len(ReservationBook.capstoneList) == 0
	print("hello")
