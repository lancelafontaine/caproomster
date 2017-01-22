#UserTDG
import psycopg2
from psycopg2.extensions import AsIs

postgreSQLpass = "Intel1234"
def find(id):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()
	
	cur.execute("""SELECT * FROM timeslotTable WHERE timeid = %s;""", (id,))
	data = cur.fetchall()
	conn.close()
	#returns table row as list
	return data

def findUser(userid):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1",
							port="5432")
	cur = conn.cursor()

	cur.execute("""SELECT * FROM timeslotTable WHERE userid = %s;""", (userid,))
	data = cur.fetchall()
	conn.close()
	# returns table row as list
	return data
def insert(timeslot):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()
	
	startTime = timeslot.getStartTime()
	endTime = timeslot.getEndTime()
	date = timeslot.getDate()
	block = timeslot.getBlock()
	userId = timeslot.getId()

	cur.execute("""INSERT INTO timeslotTable(startTime, endTime, date, block,userId) VALUES
		(%s, %s, %s, %s, %s);""", (startTime, endTime, date, block,userId))
	conn.commit()
	conn.close()

def update(id, st, et, date, block):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""UPDATE timeslotTable SET startTime = %s, endTime = %s,
		date = %s, block = %s WHERE timeid = %s;""", (st, et, date, block, id))
	conn.commit()
	conn.close()

def delete(id):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()

	cur.execute("""DELETE FROM timeslotTable WHERE timeid = %s;""", (id,))
	conn.commit()
	conn.close()







	