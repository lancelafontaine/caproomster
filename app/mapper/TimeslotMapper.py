import UnitOfWork

from app.TDG import TimeslotTDG
from app.core.timeslot import Timeslot


def makeNew(st, et, date, block, userId, timeId):
    timeslot = Timeslot(st, et, date, block, userId, timeId)
    UnitOfWork.registerNew(timeslot)
    return timeslot

def makeNewWithoutCommit(st, et, date, block, userId, timeId):
    return Timeslot(st, et, date, block, userId, timeId)

def find(timeslotId):
    result = TimeslotTDG.find(timeslotId)
    if not result:
        return
    else:
        return Timeslot(result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][0])


# Returns the most-recently created timeslot of a user
def findId(userId):
    result = TimeslotTDG.findUser(userId)
    if len(result) > 0:
        return result[-1][0]
    return None


def find_all_timeslots_for_user(user_id):
    return TimeslotTDG.findUser(user_id)


def set(timeslotId):
    timeslot = find(timeslotId)
    UnitOfWork.registerDirty(timeslot)


def done():
    UnitOfWork.commit()


# remove timeslot instance from unit of work
def delete(timeslotId):
    UnitOfWork.registerDeleted(Timeslot(0, 0, None, None, None, timeslotId))


def save(timeslot):
    TimeslotTDG.insert(
        timeslot.getId(),
        timeslot.getStartTime(),
        timeslot.getEndTime(),
        timeslot.getDate(),
        timeslot.getBlock(),
        timeslot.getUserId()
   )


# remove waiting instance from database

def erase(timeslot):
    TimeslotTDG.delete(timeslot.getId())
