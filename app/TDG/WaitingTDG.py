#WaitingTDG
import psycopg2
from psycopg2.extensions import AsIs
import os


postgreSQLpass = os.environ['POSTGRES_PASSWORD']
def find(id):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""SELECT * FROM waitingTable WHERE waitingId = %s """, (id,))
	data = cur.fetchall()
	conn.close()
	#returns table row as list
	return data

def insert(room, reservee, description, timeslot):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()


	cur.execute("""INSERT INTO waitingTable(room, reservee, description, timeslot) VALUES
		(%s, %s, %s, %s);""", (room, reservee, description, timeslot))
	conn.commit()
	conn.close()

def update(id, roomId, userId, description, timeslotId):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""UPDATE waitingTable SET room = %s, reservee = %s,
		description = %s, timeslot = %s WHERE waitingId = %s;""",
		(roomId, userId, description, timeslotId,id))
	conn.commit()
	conn.close()

def delete(id):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""DELETE FROM waitingTable WHERE waitingId = %s;""", (id,))
	conn.commit()
	conn.close()


def findAll():
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
							port="5432")
	cur = conn.cursor()
	cur.execute("""SELECT * FROM waitingTable """)
	data = cur.fetchall()
	conn.close()
	# returns table row as list
	return data

def findByRoom(roomId, date):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""SELECT waitingId, room, reservee, description, timeslot, startTime, endTime FROM waitingTable LEFT OUTER JOIN timeslotTable
		ON (waitingTable.timeslot = timeslotTable.timeid) WHERE room = %s AND date = %s;""", (roomId, date))
	data = cur.fetchall()

	conn.close()
	return data

def findTimeslot(waitingId):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
							port="5432")
	cur = conn.cursor()

	cur.execute("""SELECT timeslot FROM waitingTable WHERE waitingId = %s;""", (waitingId,))
	data = cur.fetchall()

	conn.close()
	return data


def findByUser(userId):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
							port="5432")
	cur = conn.cursor()

	cur.execute("""SELECT * FROM waitingTable LEFT OUTER JOIN timeslotTable ON (waitingTable.timeslot = timeslotTable.timeid) WHERE reservee = %s;""", (userId,))
	data = cur.fetchall()

	conn.close()
	return data

