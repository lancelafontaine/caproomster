import UserMapper
import RoomMapper
import ReservationMapper
import WaitingMapper
import TimeslotMapper

from app.core.user import User
from app.core.room import Room
from app.core.reservation import Reservation
from app.core.waiting import Waiting
from app.core.timeslot import Timeslot

newList = []
changedList = []
deletedList = []


def registerNew(object):
	newList.append(object)


def registerDirty(object):
	changedList.append(object)


def registerDeleted(object):
	deletedList.append(object)


def commit():
	print('Unit of Work - committing')
	for index, object in enumerate(newList):
		if isinstance(object, User):
			UserMapper.save(object)
		if isinstance(object, Room):
			RoomMapper.save(object)
		if isinstance(object, Reservation):
			ReservationMapper.save(object)
		if isinstance(object, Waiting):
			WaitingMapper.save(object)
		if isinstance(object, Timeslot):
			TimeslotMapper.save(object)

	for index, object in enumerate(changedList):
		if isinstance(object, User):
			UserMapper.update(object)
		if isinstance(object, Room):
			RoomMapper.update(object)
		if isinstance(object, Reservation):
			ReservationMapper.update(object)
		if isinstance(object, Waiting):
			WaitingMapper.update(object)
		if isinstance(object, Timeslot):
			TimeslotMapper.update(object)

	for index, object in enumerate(deletedList):
		if isinstance(object, User):
			UserMapper.erase(object)
		if isinstance(object, Room):
			RoomMapper.erase(object)
		if isinstance(object, Reservation):
			ReservationMapper.erase(object)
		if isinstance(object, Waiting):
			WaitingMapper.erase(object)
		if isinstance(object, Timeslot):
			TimeslotMapper.erase(object)

	del newList[:]
	del changedList[:]
	del deletedList[:]
