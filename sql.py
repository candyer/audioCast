import os
import psycopg2

version = 'postgres'
DATABASE_URL = os.environ['DATABASE_URL']	

def my_connect():
	if version == 'postgres':
		return psycopg2.connect(DATABASE_URL, sslmode='require')
	elif version == 'sqlite':
		return sqlite3.connect('info.db')
	raise "unknown DB"

def create_table():
	conn = my_connect()
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT, password TEXT);')
	#c.execute('DROP TABLE tokens;')
	c.execute('CREATE TABLE IF NOT EXISTS tokens (tokenid SERIAL PRIMARY KEY, \
												  userid INTEGER REFERENCES users(id), \
												  dropbox_access_token TEXT, \
												  url_token TEXT, \
												  title TEXT, \
												  description TEXT, \
												  qrcode TEXT);')
	conn.commit()
	c.close()
	conn.close()
# create_table() # only need to call it once


def insert_user(username, password):
	conn = my_connect()
	c = conn.cursor()
	c.execute('INSERT INTO users (name, password) VALUES (%s, %s);', (username, password))
	conn.commit()
	c.close()
	conn.close()


def insert_token(userid, dropbox_access_token, url_token, title, description, qrcode):
	conn = my_connect()
	c = conn.cursor()
	c.execute('INSERT INTO tokens (userid, dropbox_access_token, url_token, title, description, qrcode) VALUES (%s, %s, %s, %s, %s, %s);', 
								  (userid, dropbox_access_token, url_token, title, description, qrcode))
	conn.commit()
	c.close()
	conn.close()


def get_the_userID(username):
	conn = my_connect()
	c = conn.cursor()
	#c.execute("SELECT * FROM users")
	c.execute("SELECT id FROM users where name = %s", (username,))
	data = c.fetchone()
	# print('data:', data)
	conn.commit()
	c.close()
	conn.close()
	return data


def check_password(username):
	conn = my_connect()
	c = conn.cursor()
	c.execute("SELECT password FROM users where name = %s", (username,))
	data = c.fetchone()	
	conn.commit()
	c.close()
	conn.close()
	return data[0]


def get_the_latest_token_info(url_token):
	conn = my_connect()
	c = conn.cursor()
	c.execute("SELECT dropbox_access_token, title, description FROM tokens where url_token = %s", (url_token,))
	data = c.fetchone()	
	conn.commit()
	c.close()
	conn.close()
	return data

def get_the_user_info(userID):
	conn = my_connect()
	c = conn.cursor()
	c.execute("SELECT title, description, url_token, qrcode FROM tokens where userID = %s ORDER BY tokenid ASC", (userID,))
	data = c.fetchall()	
	conn.commit()
	c.close()
	conn.close()
	return data




