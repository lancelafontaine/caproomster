from datetime import datetime
from datetime import timedelta
from app.mapper import ReservationMapper
from app.mapper import RoomMapper
from app.mapper import UserMapper
from app.mapper import EquipmentMapper
from app.mapper import WaitingMapper
from app.mapper import TimeslotMapper
from app.core.equipment import Equipment
from app.core.timeslot import Timeslot
from flask import jsonify
from app.constants import STATUS_CODE, MAX_EQUIPMENT_NUMBER
from uuid import uuid4

class ReservationBook:
    def __init__(self):
        self.reservationList = ReservationMapper.findAll()
        self.waitingListRegular = WaitingMapper.findAllRegular()
        self.waitingListCapstone = WaitingMapper.findAllCapstone()

    def get_all_rooms(self):
        room_models = RoomMapper.findAll()
        if room_models:
            return sorted([room.getId() for room in room_models])
        return []

    def get_all_reservations(self):
        reservations_data = []
        for reservation in self.reservationList:
            reservations_data += [reservation.to_dict()]
        data = {
            'reservations': reservations_data
        }
        waitings_data = []
        for waiting in self.waitingListRegular:
            waitings_data += [waiting.to_dict()]
        for waiting in self.waitingListCapstone:
            waitings_data += [waiting.to_dict()]
        data.update({'waitings': waitings_data})
        return jsonify(data)

    def get_reservations_by_room(self, roomId):
        reservations_data = []
        for reservation in self.reservationList:
            if str(reservation.getRoom().getId()) == str(roomId):
                reservations_data += [reservation.to_dict()]
        data = {
            'roomId': roomId,
            'reservations': reservations_data
        }

        waitings_data = []
        for waiting in self.waitingListCapstone:
            if str(waiting.getRoom().getId()) == str(roomId):
                waitings_data += [waiting.to_dict()]
        for waiting in self.waitingListRegular:
            if str(waiting.getRoom().getId()) == str(roomId):
                waitings_data += [waiting.to_dict()]
        data.update({'waitings': waitings_data})

        return jsonify(data)

    def get_reservations_by_user(self, username):
        reservations_data = []
        for reservation in self.reservationList:
            if reservation.getUser().getId() == username:
                reservations_data += [reservation.to_dict()]
        data = {
            'username': username,
            'reservations': reservations_data
        }

        waitings_data = []
        for waiting in self.waitingListCapstone:
            if waiting.getUser().getId() == username:
                waitings_data += [waiting.to_dict()]
        for waiting in self.waitingListRegular:
            if waiting.getUser().getId() == username:
                waitings_data += [waiting.to_dict()]
        data.update({'waitings': waitings_data})

        return jsonify(data)

    def make_new_reservation(self, data):
        startTime = int(data['timeslot']['startTime'])
        endTime = int(data['timeslot']['endTime'])
        date = str(data['timeslot']['date'])
        dateList = date.split('/')
        roomId = data['roomId']
        username = data['username']
        description = str(data['description'])
        laptop = int(data['equipment']['laptop'])
        board = int(data['equipment']['board'])
        projector = str(data['equipment']['projector'])

        if not UserMapper.find(username) or not RoomMapper.find(roomId):
            response = jsoeify({'makeNewReservation error': 'Either the room or user does not exist.'})
            response.status_code = STATUS_CODE['NOT_FOUND']
            return response

        # no use for `block` parameter, for now, just passing empty strin
        timeslot = TimeslotMapper.makeNew(startTime, endTime, datetime(int(dateList[0]), int(dateList[1]), int(dateList[2])), '', username, str(uuid4()))
        room = RoomMapper.find(roomId)
        user = UserMapper.find(username)
        equipment = EquipmentMapper.makeNew(laptop, projector, board, str(uuid4()))

        if self.find_total_reserved_time_for_user_for_a_given_week(user.getId(), timeslot.getDate().strftime('%Y/%m/%d')) >= 3:
            TimeslotMapper.delete(timeslot.getId())
            EquipmentMapper.delete(equipment.getId())
            TimeslotMapper.done()
            EquipmentMapper.done()
            response = jsonify({'error': 'You have already booked for your maximum amount of time this week. Aborting.'})
            response.status_code = STATUS_CODE['UNPROCESSABLE']
            return response

        TimeslotMapper.done()
        EquipmentMapper.done()

        if not self.isTimeslotAvailableforRoom(room, timeslot):
            return jsonify(self.commit_new_waiting(room, user, timeslot, description, equipment, 'There is a timeslot conflict: added to the waiting list'))

        if not self.isEquipmentAvailableForTimeSlot(timeslot, equipment):
            return jsonify(self.commit_new_waiting(room, user, timeslot, description, equipment, 'There is not enough equipment: added to the waiting list'))

        # Successfully adding a reservation
        return jsonify(self.commit_new_reservation(room, user, timeslot, description, equipment))



    def commit_new_waiting(self, room, user, time, description, equipment, message):
        waiting = WaitingMapper.makeNew(room, user, time, description, equipment, str(uuid4()))
        if waiting.getUser().isCapstone():
            self.waitingListCapstone.append(waiting)
        else:
            self.waitingListRegular.append(waiting)
        WaitingMapper.done()
        response_data = {
            'makeNewReservation': message,
            'waitingId': waiting.getId()
        }
        return response_data


    def commit_new_reservation(self, room, user, time, description, equipment):
        reservation = ReservationMapper.makeNew(room, user, time, description, equipment, str(uuid4()))
        self.reservationList.append(reservation)
        ReservationMapper.done()
        response_data = {
            'makeNewReservation': 'successfully created reservation',
            'reservation': reservation.getId()
        }
        return response_data

    def delete_reservation(self, reservationId):
        reservation = ReservationMapper.find(reservationId)
        waiting = WaitingMapper.find(reservationId)
        if not reservation and not waiting:
            response = jsonify({'reservation error': 'that reservationId does not exist in any list'})
            response.status_code = STATUS_CODE['NOT_FOUND']
            return response

        if reservation:
            timeslotId = reservation.getTimeslot().getId()
            equipmentId = reservation.getEquipment().getId()
            ReservationMapper.delete(reservationId)
            ReservationMapper.done()
            data = {
                'success': 'reservation successfully deleted',
                'reservationId': reservationId
            }
            self.reservationList = ReservationMapper.findAll()


        if waiting:
            timeslotId = waiting.getTimeslot().getId()
            equipmentId = waiting.getEquipment().getId()
            WaitingMapper.delete(reservationId)
            WaitingMapper.done()
            data = {
                'success': 'reservation on waiting list successfully deleted',
                'waitingId': reservationId
            }
            self.waitingListRegular = WaitingMapper.findAllRegular()
            self.waitingListCapstone = WaitingMapper.findAllCapstone()

        TimeslotMapper.delete(timeslotId)
        TimeslotMapper.done()
        EquipmentMapper.delete(equipmentId)
        EquipmentMapper.done()

        # update reservation and waiting lists here
        return jsonify(data)

    def isEquipmentAvailableForTimeSlot(self, timeslot, equipment):
        # type: (Timeslot, Equipment) -> bool
        currentEquipmentAvailable = self.getAllEquipmentAvailableAtTimeslot(timeslot)
        for type, quantity in equipment.equipment.iteritems():
            amountAvailable = currentEquipmentAvailable.equipment[type]
            currentEquipmentAvailable.equipment[type] = int(amountAvailable) - int(quantity)
        return currentEquipmentAvailable.getNumLaptops() >= 0 and \
               currentEquipmentAvailable.getNumProjectors() >= 0 and \
               currentEquipmentAvailable.getNumWhiteboards() >= 0

    def getAllEquipmentAvailableAtTimeslot(self, timeslot):
        """

        :rtype: Equipment
        """
        maxEquipmentAvailable = Equipment("equipmentID_uvu", laptops=MAX_EQUIPMENT_NUMBER, projectors=MAX_EQUIPMENT_NUMBER, whiteboards=MAX_EQUIPMENT_NUMBER)
        # iterate through reservations list, get total equipment already reserved
        for r in self.getAllReservationsForTimeslot(timeslot):
            for type, quantity in r.getEquipment().equipment.iteritems():
                amountAvailable = maxEquipmentAvailable.equipment[type]
                maxEquipmentAvailable.equipment[type] = int(amountAvailable) - int(quantity)
        return maxEquipmentAvailable

    def getAllReservationsForTimeslot(self, timeslot):
        listOfReservations = []
        for r in self.reservationList:
            if r.getTimeslot().overlaps(timeslot):
                listOfReservations.append(r)
        return listOfReservations


    def isTimeslotAvailableforRoom(self, room, timeslot):
        for r in self.reservationList:
            if r.getRoom().getId() == room.getId() and timeslot.overlaps(r.getTimeslot()):
                return False
        return True

    def find_total_reserved_time_for_user_for_a_given_week(self, user_id, date):
        diff_between_monday_and_sunday = 6
        total_time = 0
        # filter date values
        date_split_list = date.split('/')
        year = int(date_split_list[0])
        month = int(date_split_list[1])
        day = int(date_split_list[2])

        # Create datetime object
        reservation_date = datetime(year, month, day)

        # find start of the week
        monday_date = reservation_date - timedelta(days=reservation_date.weekday())

        sunday_date = monday_date + timedelta(days=diff_between_monday_and_sunday)

        user_timeslot_list = TimeslotMapper.find_all_timeslots_for_user(user_id)
        for timeslot in user_timeslot_list:

            reservation_date = datetime(timeslot[3].year, timeslot[3].month, timeslot[3].day)

            # check if reservation_date lies between monday and sunday.
            if monday_date < reservation_date < sunday_date:
                total_time += timeslot[4]

        return total_time

    def getReservationList(self):
        return self.reservationList

    def setReservationList(self, reservationList):
        self.reservationList = reservationList

    def getRegularWaitingList(self):
        return self.waitingListRegular

    def setRegularWaitingList(self, waitingList):
        self.waitingListRegular = waitingList

    def getCapstoneWaitingList(self):
        return self.waitingListCapstone

    def setCapstoneWaitingList(self, waitingList):
        self.waitingListCapstone = waitingList


    ######################################################




    # Method to update the waiting list
    def updateWaiting(self, roomId):
        # Iterate over a queue of all reservations in specify room
        for w in self.getWaitlistForRoom(roomId):
            if self.isTimeslotAvailableforRoom(w.getRoom(), w.getTimeslot()) \
                    and self.isEquipmentAvailableForTimeSlot(w.getTimeslot(), w.getEquipment()):
                if not self.isRestricted(w.getUser(), w.getTimeslot()):
                    r = Reservation(w.getRoom(), w.getUser(), w.getTimeslot(), w.getDescription(), w.getEquipment(),
                                    str(uuid4()))
                    self.reservationList.append(r)
                    if w.getUser().isCapstone():
                        self.waitingListCapstone.remove(w)
                    else:
                        self.waitingListRegular.remove(w)
                    break




    # Method for restriction
    def isRestricted(self, user, time):
        restrictions = False
        nbMyReservationInWeek = 0

        # Get week nb of specify Timeslot
        date1 = time.getDate()
        day1 = int(date1[8:10])
        month1 = int(date1[5:7])
        year1 = int(date1[0:4])
        dt1 = datetime(year1, month1, day1)
        wk1 = dt1.isocalendar()[1]

        for r in self.getUserReservations(user):
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




    def makeRepeatedReservation(self, room, user, timeslot, description, equipment, repeat_amount):
        max_repetition = 2
        days_in_a_week = 7

        # safe guard if repeat amount is greater than max repetition
        if repeat_amount > max_repetition:
            repeat_amount = max_repetition

        # filter date values
        date_split_list = timeslot.getDate().split('/')
        year = int(date_split_list[0])
        month = int(date_split_list[1])
        day = int(date_split_list[2])

        # Create datetime object
        reservation_date = datetime(year, month, day)

        # repeatAmount + 1 : because at least 1 reservation should be made
        for i in range(repeat_amount + 1):
            # create and register a timeslot object
            timeslot.setDate(reservation_date.strftime('%Y/%m/%d'))
            timeslot = TimeslotMapper.makeNew(timeslot.getStartTime(), timeslot.getEndTime(), timeslot.getDate(),
                                              timeslot.getBlock(), user.getId())
            TimeslotMapper.save(timeslot)
            timeslot_id = TimeslotMapper.findId(user.getId())
            timeslot.setId(timeslot_id)

            # create and register a reservation object
            reservation = ReservationMapper.makeNew(room, user, timeslot, description, equipment, timeslot_id)
            self.reservationList.append(reservation)
            # add a week to the current reservation date
            reservation_date += timedelta(days=days_in_a_week)
