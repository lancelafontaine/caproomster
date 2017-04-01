from app.db import connect_db

def find(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""SELECT * FROM equipmentTable WHERE equipmentid = %s;""", (id,))
	data = cur.fetchall()
	conn.close()
	return data
    else:
        return []

def insert(laptops, projectors, whiteboards):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""INSERT INTO equipmentTable(laptops, projectors, whiteboards) VALUES
		(%s, %s, %s);""", (laptops, projectors, whiteboards))
	conn.commit()
	conn.close()

def update(id, st, et, date, block):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""UPDATE timeslotTable SET startTime = %s, endTime = %s,
		date = %s, block = %s WHERE timeid = %s;""", (st, et, date, block, id))
	conn.commit()
	conn.close()

def delete(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""DELETE FROM timeslotTable WHERE equipmentid = %s;""", (id,))
	conn.commit()
	conn.close()

