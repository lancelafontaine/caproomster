from app.mapper import ReservationMapper
from app.core.reservation import Reservation
from app.mapper import WaitingMapper
from app.core.waiting import Waiting


# waitingList: list containing (waitingId, room, reservee, description, timeslotid, starttime, endtime) entries
# availabilityList: availabilities for that room (array of strings)
def updateWaiting(room_id, date, availability_list):
    i = 0
    waiting_list = WaitingMapper.findRoomOnDate(room_id, date)
    if waiting_list is None:
        return
    else:
        for waiting_with_start_and_end_time in waiting_list:

            start_time = waiting_with_start_and_end_time[5];
            end_time = waiting_with_start_and_end_time[6];
            waiting = Waiting(waiting_with_start_and_end_time[1], waiting_with_start_and_end_time[2],
                              waiting_with_start_and_end_time[4], waiting_with_start_and_end_time[3],
                              waiting_with_start_and_end_time[0])

            for time_availability in availability_list:
                if time_availability == "Available" and availability_list[i + 1] == "unavailable" and (i + 10) != 21:
                    if start_time == (i + 9) and end_time == (i + 9):
                        create_reservation(waiting.room, waiting.user, waiting.time, waiting.description,
                                           waiting_with_start_and_end_time)
                        return
                elif time_availability == "Available" and availability_list[i + 1] == "Available" and (i + 10) != 20:
                    if start_time == (i + 9) and end_time == (i + 10):
                        create_reservation(waiting.room, waiting.user, waiting.time, waiting.description,
                                           waiting_with_start_and_end_time)
                        return
                elif (i + 10) == 21 and time_availability == "Available":
                    if start_time == 21 and end_time == 21:
                        create_reservation(waiting.room, waiting.user, waiting.time, waiting.description,
                                           waiting_with_start_and_end_time)
                        return
            i = i + 1


def create_reservation(room, holder, time, description, waiting_with_start_and_end_time):
    r = Reservation(room, holder, time, description)
    ReservationMapper.save(r)
    WaitingMapper.delete(waiting_with_start_and_end_time)
