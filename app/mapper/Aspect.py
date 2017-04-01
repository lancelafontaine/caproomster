import IdMap

from app.core.user import User
from app.core.timeslot import Timeslot
from app.core.room import Room
from app.core.waiting import Waiting
from app.core.reservation import Reservation

import UserMapper
import TimeslotMapper
import RoomMapper
import WaitingMapper
import ReservationMapper

def wrap_find(func, object_class):
    def new_find(objectId):
        user = IdMap.find(object_class, objectId)
        if user is not None:
            print(object_class.__name__ + ' - find() - Cache HIT')
            return user
        print(object_class.__name__ + ' -  find() - Cache MISS')
        result = func(objectId)
        if not result:
            return
        else:
            IdMap.addTo(object_class, result)
        return result
    return new_find

def wrap_makeNew(func, object_class):
    def new_makeNew(*args):
        result = func(*args)
        print(object_class.__name__  + ' - Added a new object')
        IdMap.addTo(object_class, result)
        return result
    return new_makeNew

def wrap_delete(func, object_class):
    def new_delete(objectId):
        result = func(objectId)
        object = IdMap.find(object_class, objectId)
        if object is not None:
            IdMap.removeFrom(object_class, object)
            print(object_class.__name__  + ' - Deleted an object')
        return result
    return new_delete

def wrap_findAll(func, object_class):
    def new_find():
        results = func()
        if results:
            IdMap.clear(object_class)
            print(object_class.__name__ + ' -  findAll() - Loading All instances')
            for object in results:
                IdMap.addTo(object_class, object)
        return results
    return new_find

UserMapper.find = wrap_find(UserMapper.find, User)
UserMapper.makeNew = wrap_makeNew(UserMapper.makeNew, User)
UserMapper.delete = wrap_delete(UserMapper.delete, User)

TimeslotMapper.find = wrap_find(TimeslotMapper.find, Timeslot)
TimeslotMapper.makeNew = wrap_makeNew(TimeslotMapper.makeNew, Timeslot)
TimeslotMapper.delete = wrap_delete(TimeslotMapper.delete, Timeslot)

RoomMapper.find = wrap_find(RoomMapper.find, Room)
RoomMapper.makeNew = wrap_makeNew(RoomMapper.makeNew, Room)
RoomMapper.delete = wrap_delete(RoomMapper.delete, Room)
RoomMapper.findAll = wrap_findAll(RoomMapper.findAll, Room)

WaitingMapper.find = wrap_find(WaitingMapper.find, Waiting)
WaitingMapper.makeNew = wrap_makeNew(WaitingMapper.makeNew, Waiting)
WaitingMapper.delete = wrap_delete(WaitingMapper.delete, Waiting)
WaitingMapper.findAll = wrap_findAll(WaitingMapper.findAll, Waiting)

ReservationMapper.find = wrap_find(ReservationMapper.find, Reservation)
ReservationMapper.makeNew = wrap_makeNew(ReservationMapper.makeNew, Reservation)
ReservationMapper.delete = wrap_delete(ReservationMapper.delete, Reservation)
ReservationMapper.findAll = wrap_findAll(ReservationMapper.findAll, Reservation)

print('--- Attached Aspects successfully ----')
