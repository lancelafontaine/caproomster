from reservation import Reservation
from waiting import Waiting
from collections import deque
from datetime import datetime
from app.mapper import ReservationMapper
from app.mapper import WaitingMapper
# ReservationBook object
class ReservationBook:

    # Constructor
    def __init__(self,reservationlist,waitinglist):
        self.reservationList = reservationlist
        self.waitingList = waitinglist

    # Method to make a reservation
    def makeReservation(self, room, holder, time, description):
        # Check if room is available at specifie time
        if (self.available(room, time) == True):
            r = Reservation(room,holder,time,description)
            ReservationMapper.registerNew(r)
            ReservationMapper.done()
            self.reservationList.append(r)

    # Method to add to the waiting list
    def addToWaitingList(self, room, holder, time, description):
        w = Waiting(room,holder,time,description,self.genWid())
        WaitingMapper.registerNew(w)
        self.waitingList.append(w)

    # Method to modify reservation
    def modifyReservation(self,reservationId, time):
        r = self.getReservationById(reservationId)
        if self.available(r.getRoom(), r.getTimeslot(),reservationId) == True:
            r.setTimeslot(time)

    # Method to cancel reservation
    def cancel(self,reservationId):
        r = self.getReservationById(reservationId)
        print(self.reservationList)
        #self.reservationList.remove(r)
        ReservationMapper.delete(reservationId)

    # Method to update the waiting list
    def updateWaiting(self, roomId):
        # Get a queue of all reservations in specify room
        wList = self.getListByRoom(roomId)
        for index in range(len(wList)):
            w = wList.popleft() #Dequeue
            if self.available(w.getRoom(),w.getTimeslot()) == True:
                if self.isRestricted(w.getUser(), w.getTimeslot()) == False:
                    r = Reservation(w.getRoom(), w.getUser(), w.getTimeslot(), w.getDescription(),self.genRid())
                    self.reservationList.append(r)
                    self.waitingList.remove(w)
                    break

    # Method to view all reservations
    def view(self):
        return self.display()

    # Method that return all reservations
    def display(self):
        return self.getReservationList()

    # Method that return a reservation based on Id
    def getReservationById(self,reservationId):
        for index in range(len(self.reservationList)):
            if self.reservationList[index].getId() == reservationId:
                return self.reservationList[index]

    # Method to get a queue of Waiting
    def getListByRoom(self,roomId):
        wList = deque([])
        for index in range(len(self.waitingList)):
            if self.waitingList[index].getRoom().getId() == roomId:
                wList.append(self.waitingList[index])
        return wList

    # Method to check if the timeslot is available, also overloaded for modifyReservation case
    def available(self,room, time, rid = None):
        isAvailable = True
        if rid == None:
            for index in range(len(self.reservationList)):
                r = self.reservationList[index]
                if r.getRoom().getId() == room.getId():
                    t = r.getTimeslot()
                    # Check if same date
                    if t.getDate() == time.getDate():
                        # Check if same start time
                        if t.getStartTime() == time.getStartTime():
                            isAvailable = False
                        # Check if same end time
                        if t.getEndTime() == time.getEndTime():
                            isAvailable = False
                        # Check if the time overlaps with each other
                        if t.getStartTime() < time.getStartTime() and time.getEndTime() < t.getEndTime():
                            isAvailable = False

        # for modify only
        else:
            for index in range(len(self.reservationList)):
                r = self.reservationList[index]
                if r.getId() == rid:
                    continue
                if r.getRoom().getId() == room.getId():
                    t = r.getTimeslot()
                    if t.getDate() == time.getDate():
                        if t.getStartTime() == time.getStartTime():
                            isAvailable = False
                        if t.getEndTime() == time.getEndTime():
                            isAvailable = False
                        if t.getStartTime() < time.getStartTime() and time.getEndTime() < t.getEndTime():
                            isAvailable = False
        if isAvailable == False:
            print("Timeslot is unavailable")
        return isAvailable

    # Method to view MY reservations
    def viewMyReservation(self,user):
        myReservationList = []
        for index in range(len(self.reservationList)):
            r = self.reservationList[index]
            if(r.getUser() == user):
                myReservationList.append(r)
        return myReservationList

    # Print method for current number of reservations and waitings in the system
    def printNb(self):
        print("Nb of Reservations: " + str(len(self.reservationList)))
        print("Nb of Waiting: " + str(len(self.waitingList)))

    # Method to generate reservationId
    def genRid(self):
        if len(self.reservationList) != 0:
            largeList = []
            # Find the largest ID
            for index in range(len(self.reservationList)):
                largeList.append(self.reservationList[index].getId())
            rid = max(largeList) + 1
        else:
            rid = 0
        return rid

    # Method to generate waitingId
    def genWid(self):
        if len(self.waitingList) != 0:
            largeList = []
            for index in range(len(self.waitingList)):
                largeList.append(self.waitingList[index].getId())
            wid = max(largeList) + 1
        else:
            wid = 0
        return wid

    # Method to generate timeslotId
    def genTid(self):
        timeslotList = []
        for index in range(len(self.waitingList)):
            timeslotList.append(self.waitingList[index].getTimeslot())
        for index in range(len(self.reservationList)):
            timeslotList.append(self.reservationList[index].getTimeslot())

        if len(timeslotList) != 0:
            largeList = []
            for index in range(len(timeslotList)):
                largeList.append(timeslotList[index].getId())
            tid = max(largeList) + 1
        else:
            tid = 0
        return tid

    # Method for restriction
    def isRestricted(self,user,time):
        restrictions = False
        nbMyReservationInWeek = 0
        # Get user reservations
        myReservationList = self.viewMyReservation(user)

        # Get week nb of specify Timeslot
        date1 = time.getDate()
        day1 = int(date1[8:10])
        month1 = int(date1[5:7])
        year1 = int(date1[0:4])
        dt1 = datetime(year1, month1, day1)
        wk1 = dt1.isocalendar()[1]

        for index in range(len(myReservationList)):
            r = myReservationList[index]
            # Get week nb
            date2 = r.getTimeslot().getDate()
            day2 = int(date2[8:10])
            month2 = int(date2[5:7])
            year2 = int(date2[0:4])
            dt2 = datetime(year2, month2, day2)
            wk2 = dt2.isocalendar()[1]
            # Compare if week nb matches
            if wk1 == wk2:
                nbMyReservationInWeek = nbMyReservationInWeek + 1
            # Check if user is attempting to make another reservation on same day
            if r.getTimeslot().getDate() == time.getDate():
                 restrictions = True
                 print("Request Failed: Only one reservation per day.")
                 break
        # Check if user is at max reservation
        if nbMyReservationInWeek >= 3:
            restrictions = True
            print("Request Failed: At maximum number of reservations for this week.")

        return restrictions

    # Accessors and Mutators
    def getReservationList(self):
        return self.reservationList

    def setReservationList(self, reservationList):
        self.reservationList = reservationList

    def getWaitingList(self):
        return self.waitingList

    def setWaitingList(self, waitingList):
        self.waitingList = waitingList
