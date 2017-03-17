from app.core.registry import Registry
from app.core.reservationbook import ReservationBook
from app.core.room import Room
from app.TDG import TimeslotTDG
from app.mapper import ReservationMapper
from app.mapper import TimeslotMapper
import checkAvailabilities
from app.mapper import UserMapper
from app.mapper import WaitingMapper
import pytest


def test_valid_registry_init():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    registry = Registry(reservationBook)

    assert(type(registry.reservationBook.reservationList) is list)
    assert(type(registry.reservationBook.waitingList) is list)

def test_invalid_registry_init():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    registry = Registry(reservationBook)

    with pytest.raises(AttributeError) as e:
        registry.fakeAttributeDoesntExist

def test_issue2():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    registry = Registry(reservationBook)
    startTime = 9
    endTime = 10
    roomId = 2
    block = endTime + 1 - startTime
    date = '2016-04-04'
    if block < 3:
        block = block + 1
        description = ""
        userId = 1
        processed_description = description.upper()
        user = UserMapper.find(userId)
        if checkAvailabilities.validateAvailability(roomId, date, startTime, endTime):
            userTimeslots = TimeslotTDG.findUser(user.getId())
            checkBlock = 0
            print(userTimeslots)
            if userTimeslots:
                print("userTimeslots:")
                for timeslots in userTimeslots:
                    checkBlock = checkBlock + timeslots[2] + 1 - timeslots[1]
                for timeslots in userTimeslots:
                    print("checkBlock:")
                    print (checkBlock)
                    if str(timeslots[3]) == str(date) and checkBlock > 1:
                        print(timeslots[3])
                        print("You can only have a reservation that totals to 2 hours per day")
                room = Room(roomId, False)
                if registry.initiateAction(room.getId()):
                    # Instantiate parameters
                    timeSlot = TimeslotMapper.makeNew(startTime, endTime, date, block, user.getId())
                    TimeslotMapper.save(timeSlot)
                    timeslotId = TimeslotMapper.findId(user.getId())
                    timeSlot.setId(timeslotId)
                    time = TimeslotMapper.findTotalReservedTimeForUser(user.getId())

                    # Make Reservation
                    reservation = ReservationMapper.makeNewReservation(room, user, timeSlot,
                                                                       processed_description, timeslotId)
                    ReservationMapper.save(reservation)
                    registry.endAction(roomId)
                    return
            else:
                room = Room(roomId,False)
                if registry.initiateAction(roomId):
                    #Instantiate parameters
                    timeSlot = TimeslotMapper.makeNew(startTime,endTime,date,block, user.getId())
                    TimeslotMapper.save(timeSlot)
                    timeslotId = TimeslotMapper.findId(user.getId())
                    timeSlot.setId(timeslotId)
                    time = TimeslotMapper.findTotalReservedTimeForUser(user.getId())
                    #Make Reservation
                    reservation = ReservationMapper.makeNewReservation(room, user, timeSlot, processed_description,timeslotId)
                    ReservationMapper.save(reservation)
                    registry.endAction(roomId)
                    return
        else:
            userTimeslots = TimeslotTDG.findUser(user.getId())
            if userTimeslots:
                print("userTimeslots:")
                for timeslots in userTimeslots:
                    if str(timeslots[3]) == str(date):
                        print(timeslots[3])
                        print("You can only have 1 reservation per day")
            else:
                room = Room(roomId, False)
                timeSlot = TimeslotMapper.makeNew(startTime, endTime, date, block, user.getId())
                TimeslotMapper.save(timeSlot)
                timeslotId = TimeslotMapper.findId(user.getId())
                timeSlot.setId(timeslotId)
                waiting = WaitingMapper.makeNew(room,description,user,timeSlot)
                WaitingMapper.save(waiting)
                return
    else:
        print("You can only reserve the room for 2 consecutive hours.")
        return
    assert (type(registry.reservationBook.reservationList) is list)
