from app.db import connect_db

def find(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""SELECT * FROM waitingTable WHERE waitingId = %s """, (id,))
	data = cur.fetchall()
	conn.close()
	return data
    else:
        return []

def insert(waitingId, room, reservee, description, timeslot, equipment):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""INSERT INTO waitingTable(waitingId, room, reservee, description, timeslot, equipment) VALUES
		(%s, %s, %s, %s, %s, %s);""", (waitingId, room, reservee, description, timeslot, equipment))
	conn.commit()
	conn.close()

def update(id, roomId, userId, description, timeslotId, equipmentId):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""UPDATE waitingTable SET room = %s, reservee = %s,
		description = %s, timeslot = %s WHERE waitingId = %s;""",
		(roomId, userId, description, timeslotId, equipmentId,id))
	conn.commit()
	conn.close()

def delete(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""DELETE FROM waitingTable WHERE waitingId = %s;""", (id,))
	conn.commit()
	conn.close()

def findAll():
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""SELECT * FROM waitingTable """)
	data = cur.fetchall()
	conn.close()
	return data
    else:
        return []

def findByRoom(roomId):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""SELECT waitingId, room, reservee, description, timeslot, equipment, startTime, endTime FROM waitingTable LEFT OUTER JOIN timeslotTable
		ON (waitingTable.timeslot = timeslotTable.timeid) WHERE room = %s;""", (roomId))
	data = cur.fetchall()
	conn.close()
	return data
    else:
        return []

def findTimeslot(waitingId):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""SELECT timeslot FROM waitingTable WHERE waitingId = %s;""", (waitingId,))
	data = cur.fetchall()
	conn.close()
	return data
    else:
        return []

def findByUser(userId):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""SELECT * FROM waitingTable LEFT OUTER JOIN timeslotTable ON (waitingTable.timeslot = timeslotTable.timeid) WHERE reservee = %s;""", (userId,))
	data = cur.fetchall()
	conn.close()
	return data
    else:
        return []
