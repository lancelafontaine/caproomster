import UnitOfWork

from app.TDG import TimeslotTDG
from app.core.equipment import Equipment


def makeNew(laptops, projectors, whiteboards, equipmentId):
    equipment = Equipment(laptops=laptops, projectors=projectors, whiteboards=whiteboards)
    UnitOfWork.registerNew(timeslot)
    return timeslot


def find(timeslotId):
    result = TimeslotTDG.find(timeslotId)
    if not result:
        return
    else:
        return Timeslot(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])

def set(timeslotId):
    timeslot = find(timeslotId)
    UnitOfWork.registerDirty(timeslot)


def done():
    UnitOfWork.commit()


# remove timeslot instance from unit of work
def delete(equipmentId):
    UnitOfWork.registerDeleted(Equipment(equipmentId, 0, 0, 0))


def save(timeslot):
    TimeslotTDG.insert(timeslot.getStartTime(),
                       timeslot.getEndTime(),
                       timeslot.getDate(),
                       timeslot.getBlock(),
                       timeslot.getId()
                       )


# remove waiting instance from database

def erase(timeslotId):
    TimeslotTDG.delete(timeslotId)
