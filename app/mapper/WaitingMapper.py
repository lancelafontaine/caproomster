import UnitOfWork
import RoomMapper
import UserMapper
import TimeslotMapper

from app.TDG import WaitingTDG

from app.core.waiting import Waiting

def makeNew(room, description, reservee, timeslot):
    waiting = Waiting(room, reservee, timeslot, description,0)
    UnitOfWork.registerNew(waiting)
    return waiting


def find(waitingId):
    result = []
    result = WaitingTDG.find(waitingId)
    if not result:
        return
    else:
        room = RoomMapper.find(result[0][1])
        reservee = UserMapper.find(result[0][2])
        timeslot = TimeslotMapper.find(result[0][4])
        return Waiting(room, reservee, timeslot, result[0][3], result[0][0])

def findRoomOnDate(roomId,date):
    waitingList = WaitingTDG.findByRoom(roomId,date)
    return waitingList


def findAll():
    result = WaitingTDG.findAll()
    waitings = []
    if not result:
        return
    else:
        for _, r in enumerate(result):
            room = RoomMapper.find(r[1])
            reservee = UserMapper.find(r[2])
            timeslot = TimeslotMapper.find(r[4])
            waiting = Waiting(room, reservee, timeslot, r[3], r[0])
            waitings.append(waiting)
    return waitings


def set(waitingId):
    waiting = find(waitingId)
    UnitOfWork.registerDirty(waiting)

def done():
    UnitOfWork.commit()

# remove waiting instance from unit of work
def delete(waitingId):
    UnitOfWork.registerDeleted(Waiting(None,None,None,None,waitingId))


def save(waiting):
    WaitingTDG.insert(
        waiting.getRoom().getId(),
        waiting.getUser().getId(),
        waiting.getDescription(),
        waiting.getTimeslot().getId()
    )

def update(waiting):
    WaitingTDG.update(waiting)

# remove waiting instance from database
def erase(waitingId):
    WaitingTDG.delete(waitingId)