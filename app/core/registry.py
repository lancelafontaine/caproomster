from app.mapper import RoomMapper
from app.TDG import RoomTDG
# Registry Object
class Registry:

    # Constructor
    def __init__(self,directory, reservationBook):
        self.directory = directory
        self.reservationBook = reservationBook

    # Method to initiate an action
    def initiateAction(self,roomId):
        room = self.directory.getRoom(roomId)
        if(room.getLock() == False):
            RoomMapper.setRoom(roomId,True)
            return True
        else:
            print("Room Occupied")
            return False

    # Method to end an action
    def endAction(self,roomId):
        room = RoomTDG.find(roomId)
        if (room[0][1] == True):
            print("Room was set False")
            RoomTDG.update(roomId, False)


    # Method to make a reservation
    def makeNewReservation(self,roomId,holder,time,description):
        # Verifiy if there is any restrictions
        if self.isRestricted(holder,time) == False:
            self.reservationBook.makeReservation(self.directory.getRoom(roomId),holder,time,description)

    # Method to add to the waiting list
    def addToWaitingList(self,roomId,holder,time,description):
        self.reservationBook.addToWaitingList(self.directory.getRoom(roomId),holder,time,description)

    # Method to modify a reservation
    def modifyReservation(self,reservationId, time):
        self.reservationBook.modifyReservation(reservationId, time)

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
    def viewMyReservation(self, user):
        return self.reservationBook.viewMyReservation(user)

    # Print method for debugging
    def printNb(self):
        self.reservationBook.printNb()

    # Method to generate a time id
    def genTid(self):
        return self.reservationBook.genTid()

    # Method for restriction
    def isRestricted(self, user, time):
        return self.reservationBook.isRestricted(user,time)

    # Accessors and Mutators
    def getDirectory(self):
        return self.directory

    def setDirectory(self,directory):
        self.directory = directory

    def getReservationBook(self):
        return self.reservationBook

    def setReservationBook(self, reservationBook):
        self.reservationBook = reservationBook