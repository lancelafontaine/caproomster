# ReservationTDG
from app.db import connect_db


def find(id):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		cur.execute("""SELECT * FROM reservationTable WHERE reservationId = %s;""", (id,))
		data = cur.fetchall()
		conn.close()
		return data
	else:
		return []


def insert(id, room, description, holder, timeslot, equipment):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		print(timeslot)
		cur.execute("""INSERT INTO reservationTable(reservationId, room, description, holder, timeslot, equipment) VALUES
                (%s, %s, %s, %s, %s, %s);""", (id, room, description, holder, timeslot, equipment))
		conn.commit()
		conn.close()


def update(id, roomId, userId, description, timeslot):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		cur.execute("""UPDATE reservationTable SET room = %s, holder = %s,
                 description = %s, timeslot = %s WHERE reservationId = %s;""",
		            (roomId, userId, description, timeslot, id))
		conn.commit()
		conn.close()


def delete(id):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		print(id)
		cur.execute("""DELETE FROM reservationTable WHERE reservationId = %s;""", (id,))
		conn.commit()
		conn.close()


def findByDate(date):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
                ON (reservationTable.timeslot = timeslotTable.timeid) WHERE date = %s;""", (date,))
		data = cur.fetchall()
		conn.close()
		return data
	else:
		return []


def findByUserId(userId):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		cur.execute("""SELECT * FROM reservationTable WHERE holder = %s;""", (userId,))
		data = cur.fetchall()
		conn.close()
		return data
	else:
		return []


def findByRoom(roomId):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		cur.execute("""SELECT * FROM reservationTable WHERE room = %s;""", (roomId))
		data = cur.fetchall()
		conn.close()
		return data
	else:
		return []


def findAll():
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		cur.execute("""SELECT * FROM reservationTable""")
		data = cur.fetchall()
		conn.close()
		return data
	else:
		return []


def findUserRes(userId):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
                ON (reservationTable.timeslot = timeslotTable.timeid) WHERE userid = %s;""", (userId,))
		data = cur.fetchall()
		conn.close()
		return data
	else:
		return []


def findDateRoom(roomId, date):
	conn = connect_db()
	if conn:
		cur = conn.cursor()
		cur.execute("""SELECT * FROM reservationTable LEFT OUTER JOIN timeslotTable
                        ON (reservationTable.timeslot = timeslotTable.timeid) WHERE room = %s AND date = %s;""",
		            (roomId, date))
		data = cur.fetchall()
		conn.close()
		return data
	else:
		return []
