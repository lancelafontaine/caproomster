from app.TDG import ReservationTDG

def checkModifyAvail(reservations):
    rooms = []
    for i in range(13):
        rooms.append("Available")
    rooms[0] = reservations[0][1]
    for roomtime in reservations:
        if roomtime[6] == 9:
            rooms[1] = "unavailable"
            if roomtime[7] == 10:
                rooms[2] = "unavailable"
        if roomtime[6] == 10:
            rooms[2] = "unavailable"
            if roomtime[7] == 11:
                rooms[3] = "unavailable"
        if roomtime[6] == 11:
            rooms[3] = "unavailable"
            if roomtime[7] == 12:
                rooms[4] = "unavailable"
        if roomtime[6] == 12:
            rooms[4] = "unavailable"
            if roomtime[7] == 13:
                rooms[5] = "unavailable"
        if roomtime[6] == 13:
            rooms[5] = "unavailable"
            if roomtime[7] == 14:
                rooms[6] = "unavailable"
        if roomtime[6] == 14:
            rooms[6] = "unavailable"
            if roomtime[7] == 15:
                rooms[7] = "unavailable"
        if roomtime[6] == 15:
            rooms[7] = "unavailable"
            if roomtime[7] == 16:
                rooms[8] = "unavailable"
        if roomtime[6] == 16:
            rooms[8] = "unavailable"
            if roomtime[7] == 17:
                rooms[9] = "unavailable"
        if roomtime[6] == 17:
            rooms[9] = "unavailable"
            if roomtime[7] == 18:
                rooms[10] = "unavailable"
        if roomtime[6] == 18:
            rooms[10] = "unavailable"
            if roomtime[7] == 19:
                rooms[11] = "unavailable"
        if roomtime[6] == 19:
            rooms[11] = "unavailable"
            if roomtime[7] == 20:
                rooms[12] = "unavailable"
        if roomtime[6] == 20:
            rooms[12] = "unavailable"

    return rooms
def checkAvailabilities(date):
    rooms = []
    for i in range(5):
        availabilities = []
        for j in range(12):
            availabilities.append("Available")
        rooms.append(availabilities)
    print(date)
    allReservation = ReservationTDG.findByDate(date)
    for roomtime in allReservation:
        if roomtime[1] == 1:
            if roomtime[6] == 9:
                rooms[0][0] = "unavailable"
                if roomtime[7] == 10:
                    rooms[0][1] = "unavailable"
            if roomtime[6] == 10:
                rooms[0][1] = "unavailable"
                if roomtime[7] == 11:
                    rooms[0][2] = "unavailable"
            if roomtime[6] == 11:
                rooms[0][2] = "unavailable"
                if roomtime[7] == 12:
                    rooms[0][3] = "unavailable"
            if roomtime[6] == 12:
                rooms[0][3] = "unavailable"
                if roomtime[7] == 13:
                    rooms[0][4] = "unavailable"
            if roomtime[6] == 13:
                rooms[0][4] = "unavailable"
                if roomtime[7] == 14:
                    rooms[0][5] = "unavailable"
            if roomtime[6] == 14:
                rooms[0][5] = "unavailable"
                if roomtime[7] == 15:
                    rooms[0][6] = "unavailable"
            if roomtime[6] == 15:
                rooms[0][6] = "unavailable"
                if roomtime[7] == 16:
                    rooms[0][7] = "unavailable"
            if roomtime[6] == 16:
                rooms[0][7] = "unavailable"
                if roomtime[7] == 17:
                    rooms[0][8] = "unavailable"
            if roomtime[6] == 17:
                rooms[0][8] = "unavailable"
                if roomtime[7] == 18:
                    rooms[0][9] = "unavailable"
            if roomtime[6] == 18:
                rooms[0][9] = "unavailable"
                if roomtime[7] == 19:
                    rooms[0][10] = "unavailable"
            if roomtime[6] == 19:
                rooms[0][10] = "unavailable"
                if roomtime[7] == 20:
                    rooms[0][11] = "unavailable"
            if roomtime[6] == 20:
                rooms[0][11] = "unavailable"
        if roomtime[1] == 2:
            if roomtime[6] == 9:
                rooms[1][0] = "unavailable"
                if roomtime[7] == 10:
                    rooms[1][1] = "unavailable"
            if roomtime[6] == 10:
                rooms[1][1] = "unavailable"
                if roomtime[7] == 11:
                    rooms[1][2] = "unavailable"
            if roomtime[6] == 11:
                rooms[1][2] = "unavailable"
                if roomtime[7] == 12:
                    rooms[1][3] = "unavailable"
            if roomtime[6] == 12:
                rooms[1][3] = "unavailable"
                if roomtime[7] == 13:
                    rooms[1][4] = "unavailable"
            if roomtime[6] == 13:
                rooms[1][4] = "unavailable"
                if roomtime[7] == 14:
                    rooms[1][5] = "unavailable"
            if roomtime[6] == 14:
                rooms[1][5] = "unavailable"
                if roomtime[7] == 15:
                    rooms[1][6] = "unavailable"
            if roomtime[6] == 15:
                rooms[1][6] = "unavailable"
                if roomtime[7] == 16:
                    rooms[1][7] = "unavailable"
            if roomtime[6] == 16:
                rooms[1][7] = "unavailable"
                if roomtime[7] == 17:
                    rooms[1][8] = "unavailable"
            if roomtime[6] == 17:
                rooms[1][8] = "unavailable"
                if roomtime[7] == 18:
                    rooms[1][9] = "unavailable"
            if roomtime[6] == 18:
                rooms[1][9] = "unavailable"
                if roomtime[7] == 19:
                    rooms[1][10] = "unavailable"
            if roomtime[6] == 19:
                rooms[1][10] = "unavailable"
                if roomtime[7] == 20:
                    rooms[1][11] = "unavailable"
            if roomtime[6] == 20:
                rooms[1][11] = "unavailable"
        if roomtime[1] == 3:
            if roomtime[6] == 9:
                rooms[2][0] = "unavailable"
                if roomtime[7] == 10:
                    rooms[2][1] = "unavailable"
            if roomtime[6] == 10:
                rooms[2][1] = "unavailable"
                if roomtime[7] == 11:
                    rooms[2][2] = "unavailable"
            if roomtime[6] == 11:
                rooms[2][2] = "unavailable"
                if roomtime[7] == 12:
                    rooms[2][3] = "unavailable"
            if roomtime[6] == 12:
                rooms[2][3] = "unavailable"
                if roomtime[7] == 13:
                    rooms[2][4] = "unavailable"
            if roomtime[6] == 13:
                rooms[2][4] = "unavailable"
                if roomtime[7] == 14:
                    rooms[2][5] = "unavailable"
            if roomtime[6] == 14:
                rooms[2][5] = "unavailable"
                if roomtime[7] == 15:
                    rooms[2][6] = "unavailable"
            if roomtime[6] == 15:
                rooms[2][6] = "unavailable"
                if roomtime[7] == 16:
                    rooms[2][7] = "unavailable"
            if roomtime[6] == 16:
                rooms[2][7] = "unavailable"
                if roomtime[7] == 17:
                    rooms[2][8] = "unavailable"
            if roomtime[6] == 17:
                rooms[2][8] = "unavailable"
                if roomtime[7] == 18:
                    rooms[2][9] = "unavailable"
            if roomtime[6] == 18:
                rooms[2][9] = "unavailable"
                if roomtime[7] == 19:
                    rooms[2][10] = "unavailable"
            if roomtime[6] == 19:
                rooms[2][10] = "unavailable"
                if roomtime[7] == 20:
                    rooms[2][11] = "unavailable"
            if roomtime[6] == 20:
                rooms[2][11] = "unavailable"
        if roomtime[1] == 4:
            if roomtime[6] == 9:
                rooms[3][0] = "unavailable"
                if roomtime[7] == 10:
                    rooms[3][1] = "unavailable"
            if roomtime[6] == 10:
                rooms[3][1] = "unavailable"
                if roomtime[7] == 11:
                    rooms[3][2] = "unavailable"
            if roomtime[6] == 11:
                rooms[3][2] = "unavailable"
                if roomtime[7] == 12:
                    rooms[3][3] = "unavailable"
            if roomtime[6] == 12:
                rooms[3][3] = "unavailable"
                if roomtime[7] == 13:
                    rooms[3][4] = "unavailable"
            if roomtime[6] == 13:
                rooms[3][4] = "unavailable"
                if roomtime[7] == 14:
                    rooms[3][5] = "unavailable"
            if roomtime[6] == 14:
                rooms[3][5] = "unavailable"
                if roomtime[7] == 15:
                    rooms[3][6] = "unavailable"
            if roomtime[6] == 15:
                rooms[3][6] = "unavailable"
                if roomtime[7] == 16:
                    rooms[3][7] = "unavailable"
            if roomtime[6] == 16:
                rooms[3][7] = "unavailable"
                if roomtime[7] == 17:
                    rooms[3][8] = "unavailable"
            if roomtime[6] == 17:
                rooms[3][8] = "unavailable"
                if roomtime[7] == 18:
                    rooms[3][9] = "unavailable"
            if roomtime[6] == 18:
                rooms[3][9] = "unavailable"
                if roomtime[7] == 19:
                    rooms[3][10] = "unavailable"
            if roomtime[6] == 19:
                rooms[3][10] = "unavailable"
                if roomtime[7] == 20:
                    rooms[3][11] = "unavailable"
            if roomtime[6] == 20:
                rooms[3][11] = "unavailable"
        if roomtime[1] == 5:
            if roomtime[6] == 9:
                rooms[4][0] = "unavailable"
                if roomtime[7] == 10:
                    rooms[4][1] = "unavailable"
            if roomtime[6] == 10:
                rooms[4][1] = "unavailable"
                if roomtime[7] == 11:
                    rooms[4][2] = "unavailable"
            if roomtime[6] == 11:
                rooms[4][2] = "unavailable"
                if roomtime[7] == 12:
                    rooms[4][3] = "unavailable"
            if roomtime[6] == 12:
                rooms[4][3] = "unavailable"
                if roomtime[7] == 13:
                    rooms[4][4] = "unavailable"
            if roomtime[6] == 13:
                rooms[4][4] = "unavailable"
                if roomtime[7] == 14:
                    rooms[4][5] = "unavailable"
            if roomtime[6] == 14:
                rooms[4][5] = "unavailable"
                if roomtime[7] == 15:
                    rooms[4][6] = "unavailable"
            if roomtime[6] == 15:
                rooms[4][6] = "unavailable"
                if roomtime[7] == 16:
                    rooms[4][7] = "unavailable"
            if roomtime[6] == 16:
                rooms[4][7] = "unavailable"
                if roomtime[7] == 17:
                    rooms[4][8] = "unavailable"
            if roomtime[6] == 17:
                rooms[4][8] = "unavailable"
                if roomtime[7] == 18:
                    rooms[4][9] = "unavailable"
            if roomtime[6] == 18:
                rooms[4][9] = "unavailable"
                if roomtime[7] == 19:
                    rooms[4][10] = "unavailable"
            if roomtime[6] == 19:
                rooms[4][10] = "unavailable"
                if roomtime[7] == 20:
                    rooms[4][11] = "unavailable"
            if roomtime[6] == 20:
                rooms[0][11] = "unavailable"
    return rooms

def validateAvailability(room, date, starttime, endtime):
    isavailable = True
    starttime = int(starttime)
    endtime = int(endtime)
    room = int(room)
    allReservation = ReservationTDG.findByDate(date)
    for roomtime in allReservation:
        if roomtime[1] == room:
            if roomtime[6] == starttime:
                isavailable =  False
            elif roomtime[6] == endtime:
                isavailable = False
            elif roomtime[7] == endtime:
                isavailable = False
            elif roomtime[7] == starttime:
                isavailable = False
    return isavailable


