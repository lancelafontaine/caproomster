#ReservationTDG
import psycopg2
import os
from psycopg2.extensions import AsIs

postgreSQLpass = os.environ['POSTGRES_PASSWORD']
try:
        shouldSkipDbConnect = os.environ['CIRCLE_DB_FLAG']
except KeyError:
        shouldSkipDbConnect = False


def find(id):
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
                cur = conn.cursor()

                cur.execute("""SELECT * FROM reservationTable WHERE reservationId = %s;""", (id,))
                data = cur.fetchall()
                conn.close()
                #returns row as list
                return data
        else:
                return []

def insert(room, description, holder, timeslot):
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
                cur = conn.cursor()

                print(timeslot)
                cur.execute("""INSERT INTO reservationTable(room, description, holder, timeslot) VALUES
                        (%s, %s, %s, %s);""", (room, description, holder, timeslot))

                conn.commit()
                conn.close()

def update(id, roomId, userId, description, timeslot):
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
                cur = conn.cursor()

                cur.execute("""UPDATE reservationTable SET room = %s, holder = %s,
                         description = %s, timeslot = %s WHERE reservationId = %s;""",
                          (roomId, userId, description, timeslot, id))
                conn.commit()
                conn.close()

def delete(id):
        if (not shouldSkipDbConnect):
            conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
            cur = conn.cursor()
            print(id)
            cur.execute("""DELETE FROM reservationTable WHERE reservationId = %s;""", (id,))
            conn.commit()
            conn.close()


def findByDate(date):
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
                cur = conn.cursor()
                cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
                        ON (reservationTable.timeslot = timeslotTable.timeid) WHERE date = %s;""", (date,))
                data = cur.fetchall()

                conn.close()
                return data
        else:
                return []

def findByUserId(userId):
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
                cur = conn.cursor()

                cur.execute("""SELECT * FROM reservationTable WHERE holder = %s;""", (userId,))
                data = cur.fetchall()
                conn.close()
                # returns row as list
                return data
        else:
                return []

def findAll():
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
                                                                port="5432")
                cur = conn.cursor()

                cur.execute("""SELECT * FROM reservationTable""")
                data = cur.fetchall()
                conn.close()
                # returns row as list
                return data
        else:
                return []

def findUserRes(userId):
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
                                                                port="5432")
                cur = conn.cursor()
                cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
                        ON (reservationTable.timeslot = timeslotTable.timeid) WHERE userid = %s;""", (userId,))
                data = cur.fetchall()

                conn.close()
                return data
        else:
                return []


def insertDirect(room, description, holder, timeslot):
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
                                                                port="5432")
                cur = conn.cursor()


                cur.execute("""INSERT INTO reservationTable(room, description, holder, timeslot) VALUES
                        (%s, %s, %s, %s);""", (room, description, holder, timeslot))

                conn.commit()
                conn.close()

def findDateRoom(roomId, date):
        if (not shouldSkipDbConnect):
                conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
                                                                port="5432")
                cur = conn.cursor()
                cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
                                ON (reservationTable.timeslot = timeslotTable.timeid) WHERE room = %s AND date = %s;""", (roomId,date))
                data = cur.fetchall()

                conn.close()
                return data
        else:
                return []
