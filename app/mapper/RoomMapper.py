import UnitOfWork

from app.TDG import RoomTDG

from app.core.room import Room


def makeNew(roomId):
    room = Room(roomId)
    UnitOfWork.registerNew(room)
    return room

def find(roomId):
    result = RoomTDG.find(roomId)
    if not result:
        return
    else:
        return Room(result[0][0])

#returns array of all rooms
def findAll():
    result = RoomTDG.findAll()
    rooms = []
    if not result:
        return
    else:
        for index, r in enumerate(result):
            room = Room(r[0])
            rooms.append(room)
    return rooms


def delete(roomId):
    UnitOfWork.registerDeleted(Room(roomId))

#save all work
def done():
    UnitOfWork.commit()

#adds room object
def save(room):
    RoomTDG.insert(room.getLock())

#updates room Object
def update(room,availability):
    RoomTDG.update(room, availability)

#deletes room object
def erase(roomId):
    RoomTDG.delete(roomId)