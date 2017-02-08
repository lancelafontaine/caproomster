#ReservationTDG
import psycopg2
import os
from psycopg2.extensions import AsIs

postgreSQLpass = os.environ['POSTGRES_PASSWORD']
def find(id):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""SELECT * FROM reservationTable WHERE reservationId = %s;""", (id,))
	data = cur.fetchall()
	conn.close()
	#returns row as list
	return data

def insert(room, description, holder, timeslot):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	print(timeslot)
	cur.execute("""INSERT INTO reservationTable(room, description, holder, timeslot) VALUES
		(%s, %s, %s, %s);""", (room, description, holder, timeslot))

	conn.commit()
	conn.close()

def update(id, roomId, userId, description, timeslot):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""UPDATE reservationTable SET room = %s, holder = %s,
		 description = %s, timeslot = %s WHERE reservationId = %s;""",
		  (roomId, userId, description, timeslot, id))
	conn.commit()
	conn.close()

def delete(id):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()
	print(id)
	cur.execute("""DELETE FROM reservationTable WHERE reservationId = %s;""", (id,))
	conn.commit()
	conn.close()


def findByDate(date):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()
	cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
		ON (reservationTable.timeslot = timeslotTable.timeid) WHERE date = %s;""", (date,))
	data = cur.fetchall()

	conn.close()
	return data

def findByUserId(userId):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""SELECT * FROM reservationTable WHERE holder = %s;""", (userId,))
	data = cur.fetchall()
	conn.close()
	# returns row as list
	return data

def findAll():
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
							port="5432")
	cur = conn.cursor()

	cur.execute("""SELECT * FROM reservationTable""")
	data = cur.fetchall()
	conn.close()
	# returns row as list
	return data

def findUserRes(userId):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
							port="5432")
	cur = conn.cursor()
	cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
    		ON (reservationTable.timeslot = timeslotTable.timeid) WHERE userid = %s;""", (userId,))
	data = cur.fetchall()

	conn.close()
	return data


def insertDirect(room, description, holder, timeslot):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
							port="5432")
	cur = conn.cursor()


	cur.execute("""INSERT INTO reservationTable(room, description, holder, timeslot) VALUES
		(%s, %s, %s, %s);""", (room, description, holder, timeslot))

	conn.commit()
	conn.close()

def findDateRoom(roomId, date):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
							port="5432")
	cur = conn.cursor()
	cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
        		ON (reservationTable.timeslot = timeslotTable.timeid) WHERE room = %s AND date = %s;""", (roomId,date))
	data = cur.fetchall()

	conn.close()
	return data