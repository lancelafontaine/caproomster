import UnitOfWork
import RoomIdMap

from app.TDG import RoomTDG

from app.core.room import Room


def makeNew(roomId, lock):
    room = Room(roomId, lock)
    RoomIdMap.addTo(room)
    UnitOfWork.registerNewRoom(room)
    return room

def find(roomId):
    room = RoomIdMap.find(roomId)
    result = []
    if room == None:
        result = RoomTDG.find(roomId)
        if result == None:
            return
        else:
            room = Room(result[0][0], result[0][1])
            RoomIdMap.addTo(room)
    return room

#returns array of all rooms
def findAll():
    result = RoomTDG.findAll()
    rooms = []
    if result == None:
        return
    else:
        for index, r in enumerate(result):
            room = RoomIdMap.find(r[0])
            if room == None:
                room = Room(r[0], r[1])
                RoomIdMap.addTo(room) 
                rooms.append(room)
    return rooms

def setRoom(roomId, lock):
    room = find(roomId)
    room.setLock(lock)
    update(room.getId(),room.getLock())

def delete(roomId):
    room = RoomIdMap.find(roomId)
    if room is not None:
        RoomIdMap.removeFrom(room)
    UnitOfWork.registerDeleted(room)
#save all work
def done():
    UnitOfWork.commit()
#adds room object
def save(room):
    RoomTDG.insert(room)
#updates room Object
def update(room,availability):
    RoomTDG.update(room, availability)
#deletes room object
def erase(room):
    RoomTDG.delete(room)