import UnitOfWork

from app.TDG import RoomTDG

from app.core.room import Room


def makeNew(roomId):
    room = Room(roomId)
    UnitOfWork.registerNew(room)
    return room

def find(roomId):
    result = []
    result = RoomTDG.find(roomId)
    if not result:
        return
    else:
        return Room(result[0][0], result[0][1])

#returns array of all rooms
def findAll():
    result = RoomTDG.findAll()
    rooms = []
    if not result:
        return
    else:
        for index, r in enumerate(result):
            room = Room(r[0], r[1])
            rooms.append(room)
    return rooms

#need to remove do thing
'''def setRoom(roomId, lock):
    room = find(roomId)
#    room.setLock(lock)
    update(room.getId())'''

def delete(roomId):
    UnitOfWork.registerDeleted(Room(roomId,None))
#save all work
def done():
    UnitOfWork.commit()

#adds room object
#def save(room):
  #  RoomTDG.insert(room.getLock())

#updates room Object
#need to remove do thing
'''def update(room):
    RoomTDG.update(room)'''

#deletes room object
def erase(roomId):
    RoomTDG.delete(roomId)