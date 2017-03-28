from app.db import connect_db

def find(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""SELECT * FROM userTable WHERE userId = %s;""", (id,))
	data = cur.fetchall()
	conn.close()
	return data
    else:
        return []

def insert(name, pw, capstone):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""INSERT INTO userTable(password, name, capstone) VALUES
  		(%s, %s);""", (pw, name, capstone))
	conn.commit()
	conn.close()

def update(id, name, password, capstone):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""UPDATE userTable SET name = %s,
  		password = %s WHERE userId = %s;""", (name, password, id, capstone))
	conn.commit()
	conn.close()

def delete(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""DELETE FROM userTable WHERE userId = %s;""", (id,))
	conn.commit()
	conn.close()

