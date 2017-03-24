import UnitOfWork

from app.TDG import TimeslotTDG
from app.core.timeslot import Timeslot


def makeNew(st, et, date, block, userId):
    timeslot = Timeslot(st, et, date, block, userId)
    UnitOfWork.registerNew(timeslot)
    return timeslot


def find(timeslotId):
    result = []
    result = TimeslotTDG.find(timeslotId)
    if not result:
        return
    else:
        return Timeslot(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5])


def findId(userId):
    result = TimeslotTDG.findUser(userId)
    return result[-1][0]


def find_all_timeslots_for_user(user_id):
    result = TimeslotTDG.findUser(user_id)
    return result


def set(timeslotId):
    timeslot = find(timeslotId)
    UnitOfWork.registerDirty(timeslot)


def done():
    UnitOfWork.commit()


# remove timeslot instance from unit of work
def delete(timeslotId):
    UnitOfWork.registerDeleted(Timeslot(0, 0, None, None, timeslotId))


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
