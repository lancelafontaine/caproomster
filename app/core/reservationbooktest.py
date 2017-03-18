from app import app
from app.core.reservationbook import ReservationBook
from app.core.waiting import Waiting
from app.core.timeslot import Timeslot
from app.core.user import User
from app.core.room import Room

"""Tests whether a capstone student really has priority over a regular student in the waitlist"""


def test_capstone_priority():
	with app.app_context():
		"""
		Add a reservation for a certain room
		Try to add another reservation for same room at the same time (regular student)
		Regular student is waitlisted
		Try to add another reservation at the same time (capstone student)
		Capstone student is waitlisted
		First user cancels their reservation
		Check whether it is the regular student or the capstone student
		 who gets the freed reservation slot
			"""


	# Mock


	# Execute


	# Verify
