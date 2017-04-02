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

def insert(equipmentId, laptops, projectors, whiteboards):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""INSERT INTO equipmentTable(equipmentId,laptops, projectors, whiteboards) VALUES
		(%s, %s, %s, %s);""", (equipmentId,laptops, projectors, whiteboards))
	conn.commit()
	conn.close()

def update(id, laptops, projectors, whiteboards):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""UPDATE equipmentTable SET equipmentId = %s, laptops = %s,
		projectors = %s, whiteboards = %s WHERE equipmentId= %s;""", (id, laptops, projectors, whiteboards,id))
	conn.commit()
	conn.close()

def delete(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""DELETE FROM equipmentTable WHERE equipmentid = %s;""", (id,))
	conn.commit()
	conn.close()

