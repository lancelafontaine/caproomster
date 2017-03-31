from app.mapper import RoomMapper

# Registry Object
class Registry:

    # Constructor
    def __init__(self, reservationBook):
        self.reservationBook = reservationBook

    # Method to initiate an action
    def initiateAction(self,roomId):
        room = RoomMapper.find(roomId)

        if room.getLock() == False:
            RoomMapper.setRoom(roomId,True)
            return True
        else:
            print("Room Occupied")
            return False

    # Method to end an action
    def endAction(self,roomId):
        room = RoomMapper.find(roomId)
        if room.getLock() == True:
            print("Room was set False")
            RoomMapper.update(roomId, False)


    # Method to make a reservation
    def makeNewReservation(self, roomId, user, timeslot, description, equipment):
        # Verifiy if there is any restrictions
        if self.isUserRestricted(user, timeslot) == False:
            self.reservationBook.makeReservation(RoomMapper.find(roomId), user, timeslot, description, equipment)

    # Method to add to the waiting list
    def addToWaitingList(self, roomId, user, timeslot, description):
        self.reservationBook.addToWaitingList(RoomMapper.find(roomId), user, timeslot, description)

    # Method to modify a reservation
    def modifyReservation(self, reservationId, timeslot):
        self.reservationBook.modifyReservation(reservationId, timeslot)

    # Method to cancel a reservation
    def cancelReservation(self,reservationId):
        self.reservationBook.cancel(reservationId)

    # Method to view ALL reservations
    def viewSchedule(self):
        return self.reservationBook.view()

    # Method to update the waiting list
    def updateWaiting(self,roomId):
        self.reservationBook.updateWaiting(roomId)

    # Method to view MY reservations only
    def viewUserReservations(self, user):
        return self.reservationBook.getUserReservations(user)

    # Print method for debugging
    def printNb(self):
        self.reservationBook.printNb()

    # Method to generate a time id
    def genTid(self):
        return self.reservationBook.genTid()

    # Method for restriction
    def isUserRestricted(self, user, time):
        return self.reservationBook.isUserRestricted(user, time)

    # Accessors and Mutators
    def getReservationBook(self):
        return self.reservationBook

    def setReservationBook(self, reservationBook):
        self.reservationBook = reservationBook
