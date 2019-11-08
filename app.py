import os
import base64
from flask import Flask, Response, flash, render_template, request, url_for, redirect, session

from functools import wraps
import requests
import json
from podgen import Podcast, Episode, Media
from sql import create_table, insert_user, insert_token, get_the_userID, check_password, get_the_latest_token_info, get_the_user_info
from passlib.hash import sha256_crypt
import qrcode
import PIL


#create the application object
app = Flask(__name__)
app.secret_key = 'y\x9b+\xcb\x9f\n\x8d+\x7fp\x9b7\xbfc3y\xfe\x80*\x04\xd2/\xea\xe9' 

# login required decorator 
def login_required(f):
	@wraps(f)

	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Please login')
			return redirect(url_for('login', next=request.url))
	return wrap


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
	'''https://podgen.readthedocs.io/en/latest/'''

	if request.method == 'POST':
		dropbox_access_token = request.form['token']
		title = request.form['title']
		description = request.form['description']
		url_token = base64.b64encode(os.urandom(5), 'ab').strip('=') # replace '+/' with 'ab', and trim '=' from head and tail.

		userID = get_the_userID(session['username'])[0]

		link = 'http://audio-cast.herokuapp.com/rss/{}'.format(url_token)
		qr = qrcode.QRCode( version=1,  box_size=10, border=4)
		qr.add_data(link)
		qr.make(fit=True)
		img = qr.make_image(fill='black', back_color='RGB(52, 235, 222)')
		name = '{}.png'.format(url_token)
		img.save('static/{}'.format(name))

		insert_token(userID, dropbox_access_token, url_token, title, description)

		return render_template('rss.html', url_token=url_token)
	return render_template('index.html')


@app.route('/rss/<url_token>')
@login_required
def rss(url_token):
	dropbox_access_token, title, description = get_the_latest_token_info(url_token)
	urls = get_temporary_link(dropbox_access_token)
	p = Podcast()
	p.name = title
	p.description = description
	p.website = "https://www.google.com"
	p.explicit = True	

	for i, (size, url, uid, name) in enumerate(urls):
		my_episode = Episode()
		my_episode.title = os.path.splitext(name)[0]
		my_episode.id = uid
		my_episode.media = Media(url, size=size, type="audio/mpeg")
		p.episodes.append(my_episode)
	return Response(str(p), mimetype='text/xml')


@app.route('/user')
@login_required
def user():
	userID = get_the_userID(session['username'])[0]
	infos = get_the_user_info(userID)
	return render_template('user.html', infos=infos)
	


@app.route('/register',  methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form['username'].strip().lower()
		password = request.form['psw']
		repeated_password = request.form['psw-repeat']
		if get_the_userID(username):
			flash('Username exists, please choose another one')
			return render_template('register.html')			
		if password != repeated_password:
			flash("password doesn't match, please try again")
			return render_template('register.html')	
		pwd = sha256_crypt.encrypt(password)
		insert_user(username, pwd)
		session['logged_in'] = True
		session['username'] = username		
		flash(' {}, Thanks for registering'.format(username.title()))
		return redirect(url_for('home'))
	return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'logged_in' in session and session['logged_in']:
		redirect(url_for('home'))
	error = None
	if request.method == 'POST':
		username = request.form.get('username', None)
		password = request.form.get('psw', None)
		if get_the_userID(username) == None:
			error = 'Username does not exist, please try again'

		elif not sha256_crypt.verify(password, check_password(username)):
			error = 'Password does not match, pleae try again'
		else:
			session['logged_in'] = True
			session['username'] = username
			flash('{}, You were just logged in!'.format(username.title()))
			# return redirect(request.args.get('next', ''))
			return redirect(url_for('home'))
	return render_template('login.html', error=error)



@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	session.pop('username', None)
	flash('You were just logged out!')
	return redirect(url_for('login'))


def list_folder(access_token):
	'''https://dropbox.github.io/dropbox-api-v2-explorer/#files_list_folder'''
	url = "https://api.dropboxapi.com/2/files/list_folder"
	headers = {
		"Authorization": "Bearer {}".format(access_token),
		"Content-Type": "application/json",
	}
	data = {
		"path": ""
	}

	r = requests.post(url, headers=headers, data=json.dumps(data))
	paths = []
	for path in r.json()['entries']:
		paths.append(path['path_lower'])
	return paths


def get_temporary_link(access_token):
	'''https://dropbox.github.io/dropbox-api-v2-explorer/#files_get_temporary_link'''
	paths = list_folder(access_token)
	url = "https://api.dropboxapi.com/2/files/get_temporary_link"

	headers = {
		"Authorization": "Bearer {}".format(access_token),
		"Content-Type": "application/json",
	}

	urls = []
	for path in paths:
		data = {
			"path": path
		}
		r = requests.post(url, headers=headers, data=json.dumps(data))		
		urls.append((r.json()['metadata']['size'], r.json()['link'], r.json()['metadata']['id'], r.json()['metadata']['name']))
	return urls

if  __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT'), debug=True)



# @app.route('/rss/<userID>/<tokenID>')
# @login_required
# def rss(userID, tokenID):
# 	tokenid, dropbox_access_token, title, description = get_the_latest_token_info(userID, tokenID)[0]
# 	urls = get_temporary_link(dropbox_access_token)
# 	p = Podcast()
# 	p.name = title
# 	p.description = description
# 	p.website = "https://www.google.com"
# 	p.explicit = True	

# 	for i, (size, url, uid, name) in enumerate(urls):
# 		my_episode = Episode()
# 		my_episode.title = os.path.splitext(name)[0]
# 		my_episode.id = uid
# 		my_episode.media = Media(url, size=size, type="audio/mpeg")
# 		p.episodes.append(my_episode)
# 	return Response(str(p), mimetype='text/xml')



