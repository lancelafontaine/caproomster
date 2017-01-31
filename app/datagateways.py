from django.db import connection

class ReservationTDG:
    def __init__(self):
        pass

    def insert(self, username, roomNumber, status, timeslot, timestamp):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO reservations (USER_ID,ROOM_ID,STATUS,TIMESLOT,TSP) \
                            VALUES ((SELECT ID from users WHERE USERNAME=%s), \
                                    (SELECT ID from rooms WHERE ROOMNUMBER=%s),%s,%s,%s)",
                            [username, roomNumber, status, timeslot, timestamp])

    def delete(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM reservations \
                            WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                            AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                            AND TIMESLOT=%s", [username,roomNumber,timeslot])

    def deleteAllOtherPendingReservations(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM reservations \
                            WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                            AND ROOM_ID!=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                            AND STATUS='pending' \
                            AND TIMESLOT=%s", [username, roomNumber, timeslot])

    def getNumOfReservations(self, username, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(TIMESLOT) FROM reservations \
                            WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s)\
                            AND strftime('%%W', TIMESLOT)=strftime('%%W', %s)", [username, timeslot])
            count = int(cursor.fetchone()[0])
        return count

    def find(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT users.USERNAME, \
                                   rooms.ROOMNUMBER, \
                                   reservations.STATUS, \
                                   reservations.TIMESLOT,\
                                   reservations.TSP \
                            FROM reservations \
                            INNER JOIN users ON users.ID=reservations.USER_ID \
                            INNER JOIN rooms ON rooms.ID=reservations.ROOM_ID \
                            AND USERNAME=%s \
                            AND ROOMNUMBER=%s \
                            AND TIMESLOT=%s", [username, roomNumber, timeslot])
            row = cursor.fetchone()
        return row

    def findNextPendingReservation(self, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT users.USERNAME,\
                                   rooms.ROOMNUMBER,\
                                   reservations.STATUS, \
                                   reservations.TIMESLOT, \
                                   reservations.TSP \
                            FROM reservations \
                            INNER JOIN users ON users.ID=reservations.USER_ID \
                            INNER JOIN rooms ON rooms.ID=reservations.ROOM_ID \
                            WHERE reservations.TSP=(SELECT min(TSP) FROM reservations \
                                                    WHERE ROOMNUMBER=%s \
                                                    AND TIMESLOT=%s \
                                                    AND STATUS='pending')", [roomNumber, timeslot])
            row = cursor.fetchone()
        return row

    def setFilled(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE reservations \
                            SET STATUS='filled' \
                            WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                            AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                            AND TIMESLOT=%s", [username,roomNumber,timeslot])

    def getFilledCount(self, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(1) FROM reservations \
                            WHERE ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                            AND TIMESLOT=%s \
                            AND STATUS='filled'", [roomNumber, timeslot])
            count = int(cursor.fetchone()[0])
        return count

    def getReservationCount(self, username, roomNumber, timeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(1) FROM reservations \
                            WHERE USER_ID=(SELECT ID from users WHERE USERNAME=%s) \
                            AND ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                            AND TIMESLOT=%s", [username,roomNumber,timeslot])
            count = int(cursor.fetchone()[0])
        return count

    def getReservations(self, roomNumber, startTimeslot):
        with connection.cursor() as cursor:
            cursor.execute("SELECT USERNAME, TIMESLOT FROM users INNER JOIN reservations \
                            ON users.ID=reservations.USER_ID \
                            AND reservations.ROOM_ID=(SELECT ID from rooms WHERE ROOMNUMBER=%s) \
                            AND STATUS='filled' \
                            AND strftime('%%W', TIMESLOT)=strftime('%%W', %s) \
                            ORDER BY TIMESLOT ASC", [roomNumber, startTimeslot])
            rows = cursor.fetchall()
        return [list(row) for row in rows]

    def getReservationsForUsername(self, username, status):
        with connection.cursor() as cursor:
            cursor.execute("SELECT USERNAME, rooms.ROOMNUMBER, reservations.TIMESLOT FROM users \
                            INNER JOIN reservations \
                            ON users.ID = reservations.USER_ID \
                            INNER JOIN rooms \
                            ON rooms.ID = reservations.ROOM_ID \
                            AND USERNAME=%s \
                            AND STATUS=%s \
                            ORDER BY TIMESLOT ASC", [username, status])
            rows = cursor.fetchall()
        return [list(row) for row in rows]

class RoomTDG:
    def __init__(self):
        pass

    def insert(self, roomNumber):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO rooms (ROOMNUMBER) VALUES (%s)", [roomNumber])

    def getRooms(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT ROOMNUMBER FROM rooms")
            rows = cursor.fetchall()
        return [tupl[0] for tupl in rows]

class UserTDG:
    def __init__(self):
        pass

    def insert(self, username, password):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (USERNAME, PASSWORD) VALUES (%s,%s)", [username, password])

    def isRegistered(self, username, password):
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(1) FROM users WHERE USERNAME=%s AND PASSWORD=%s", [username, password])
            count = int(cursor.fetchone()[0])
        return count

