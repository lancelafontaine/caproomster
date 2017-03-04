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

def insert(name, pw):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""INSERT INTO userTable(password, name) VALUES
  		(%s, %s);""", (pw, name))
	conn.commit()
	conn.close()

def update(id, name, password):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""UPDATE userTable SET name = %s,
  		password = %s WHERE userId = %s;""", (name, password, id))
	conn.commit()
	conn.close()

def delete(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""DELETE FROM userTable WHERE userId = %s;""", (id,))
	conn.commit()
	conn.close()

