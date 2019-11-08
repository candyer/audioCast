import sqlite3


def create_table():
	conn = sqlite3.connect('info.db')
	c = conn.cursor()
	c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, password TEXT);')
	c.execute('CREATE TABLE IF NOT EXISTS tokens (tokenid INTEGER PRIMARY KEY, userid INTEGER, dropbox_access_token TEXT, url_token TEXT, title TEXT, description TEXT);')
	conn.commit()
	c.close()
	conn.close()
create_table() # only need to call it once


def insert_user(username, password):
	conn = sqlite3.connect('info.db')
	c = conn.cursor()
	c.execute('INSERT INTO users (name, password) VALUES (?, ?);', (username, password))
	conn.commit()
	c.close()
	conn.close()


def insert_token(userid, dropbox_access_token, url_token, title, description):
	conn = sqlite3.connect('info.db')
	c = conn.cursor()
	c.execute('INSERT INTO tokens (userid, dropbox_access_token, url_token, title, description) VALUES (?, ?, ?, ?, ?);', (userid, dropbox_access_token, url_token, title, description))
	conn.commit()
	c.close()
	conn.close()


def get_the_userID(username):
	conn = sqlite3.connect('info.db')
	c = conn.cursor()
	c.execute("SELECT id FROM users where name = ?", (username,))
	data = c.fetchone()	
	conn.commit()
	c.close()
	conn.close()
	return data


def check_password(username):
	conn = sqlite3.connect('info.db')
	c = conn.cursor()
	c.execute("SELECT password FROM users where name = ?", (username,))
	data = c.fetchone()	
	conn.commit()
	c.close()
	conn.close()
	return data[0]


def get_the_latest_token_info(url_token):
	conn = sqlite3.connect('info.db')
	c = conn.cursor()
	c.execute("SELECT dropbox_access_token, title, description FROM tokens where url_token = ?", (url_token,))
	data = c.fetchone()	
	conn.commit()
	c.close()
	conn.close()
	return data

def get_the_user_info(userID):
	conn = sqlite3.connect('info.db')
	c = conn.cursor()
	c.execute("SELECT title, description, url_token FROM tokens where userID = ? ORDER BY tokenid ASC", (userID,))
	data = c.fetchall()	
	conn.commit()
	c.close()
	conn.close()
	return data




