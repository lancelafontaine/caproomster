from app.db import connect_db

def find(id):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM roomTable WHERE roomId = %s;""", (id,))
        data = cur.fetchall()
        conn.close()
        return data
    else:
        return []

def findAll():
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM roomTable;""")
        data = cur.fetchall()
        conn.close()
        return data
    else:
        return []

def delete(id):
    conn = connect_db()
    if conn:
	cur = conn.cursor()
	cur.execute("""DELETE FROM roomTable WHERE userId = %s;""", (id,))
	conn.commit()
	conn.close()

