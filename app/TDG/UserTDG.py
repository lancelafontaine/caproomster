#UserTDG
import psycopg2

postgreSQLpass = "Intel1234"
def find(id):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()
	cur.execute("""SELECT * FROM userTable WHERE userId = %s;""", (id,))
	data = cur.fetchall()
	conn.close()
	#returns table row as list
	return data

def insert(user):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()
	name = user.getName()
	pw = user.getPassword()
	cur.execute("""INSERT INTO userTable(password, name) VALUES
  		(%s, %s);""", (pw, name))
	conn.commit()
	conn.close()

def update(id, name, password):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()
	cur.execute("""UPDATE userTable SET name = %s,
  		password = %s WHERE userId = %s;""", (name, password, id))
	conn.commit()
	conn.close()

def delete(id):
	conn = psycopg2.connect(database="development", user="postgres", password=postgreSQLpass, host="127.0.0.1", port="5432")
	cur = conn.cursor()
	cur.execute("""DELETE FROM userTable WHERE userId = %s;""", (id,))
	conn.commit()
	conn.close()






	