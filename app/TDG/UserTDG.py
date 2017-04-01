from app.db import connect_db


def find(username):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM userTable WHERE username = %s;""", (username,))
        data = cur.fetchall()
        conn.close()
        return data
    else:
        return []


def insert(username, password, capstone):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO userTable(username, password, capstone) VALUES
  		(%s, %s);""", (username, password, capstone))
        conn.commit()
        conn.close()


def update(username, password, capstone):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""UPDATE userTable SET password = %s AND capstone = %s WHERE username = %s;""", (password, capstone, username))
        conn.commit()
        conn.close()


def delete(username):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""DELETE FROM userTable WHERE username = %s;""", (id))
        conn.commit()
        conn.close()
