import UnitOfWork
import RoomMapper
import UserMapper
import TimeslotMapper
import EquipmentMapper

from app.TDG import WaitingTDG

from app.core.waiting import Waiting


def makeNew(room, user, timeslot, description, equipment, waitingId):
    waiting = Waiting(room, user, timeslot, description, equipment, waitingId)
    UnitOfWork.registerNew(waiting)
    return waiting


def find(waitingId):
    result = WaitingTDG.find(waitingId)
    if not result:
        return
    else:
        room = RoomMapper.find(result[0][1])
        reservee = UserMapper.find(result[0][2])
        timeslot = TimeslotMapper.find(result[0][4])
        equipment = EquipmentMapper.find(result[0][5])
        return Waiting(room, reservee, timeslot, result[0][3], equipment, result[0][0])

def findAll():
    result = WaitingTDG.findAll()
    waitings = []
    if not result:
        return
    else:
        for _, r in enumerate(result):
            room = RoomMapper.find(r[1])
            user = UserMapper.find(r[2])
            timeslot = TimeslotMapper.find(r[4])
            equipment = EquipmentMapper.find(r[5])
            waiting = Waiting(room, user, timeslot, r[3], equipment, r[0])
            waitings.append(waiting)
    return waitings

def findByUser(userId):
    userWaitings = []
    result = WaitingTDG.findByUser(userId)
    for index, userR in enumerate(result):
        userWaitings.append(find(userR[0]))
    return userWaitings

def findByRoom(roomId):
    roomWaitings = []
    result = WaitingTDG.findByRoom(roomId)
    for index, roomW in enumerate(result):
        roomWaitings.append(find(roomW[0]))
    return roomWaitings

def set(waitingId):
    waiting = find(waitingId)
    UnitOfWork.registerDirty(waiting)

def done():
    UnitOfWork.commit()

# remove waiting instance from unit of work
def delete(waitingId):
    UnitOfWork.registerDeleted(find(waitingId))


def save(waiting):
    WaitingTDG.insert(
        waiting.getId(),
        waiting.getRoom().getId(),
        waiting.getUser().getId(),
        waiting.getDescription(),
        waiting.getTimeslot().getId(),
        waiting.getEquipment().getId()
    )

def update(waiting):
    WaitingTDG.update(waiting)

# remove waiting instance from database
def erase(waiting):
    WaitingTDG.delete(waiting.getId())