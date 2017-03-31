from app.db import connect_db


def find(id):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM timeslotTable WHERE timeid = %s;""", (id,))
        data = cur.fetchall()
        conn.close()
        return data
    else:
        return []


def findUser(username):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM timeslotTable WHERE username = %s;""", (username,))
        data = cur.fetchall()
        conn.close()
        return data
    else:
        return []


def insert(timeslotId, startTime, endTime, date, block, username):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        cur.execute("""INSERT INTO timeslotTable(timeid, startTime, endTime, date, block, username) VALUES
            (%s, %s, %s, %s, %s, %s);""", (timeslotId, startTime, endTime, date, block, username,))
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
        cur.execute("""DELETE FROM timeslotTable WHERE timeid = %s;""", (id,))
        conn.commit()
        conn.close()
