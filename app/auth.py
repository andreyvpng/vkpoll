import requests
import psycopg2.extras
from flask import Blueprint, request, abort, redirect, url_for, session
from db_helper import get_db

auth = Blueprint('auth', __name__)


def get_vk():
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('select *from vk_api')
	return cur.fetchall()[0]


@auth.route('/login')
def login():
	if request.args.get('code') is None:
		return abort(501)

	vk_info = get_vk()
	data = {
		'client_id': vk_info['id'],
		'client_secret': vk_info['secret'],
		'redirect_uri': vk_info['url'],
		'code': request.args.get('code')
	}
	url = 'https://oauth.vk.com/access_token'
	response = requests.post(url, params=data)

	if response.json().get('access_token') is None:
		abort(501)

	db = get_db()
	cur = db.cursor()
	cur.execute('select *from USERS where id = (%s)', [response.json().get('user_id')])
	check_for_user = cur.fetchall()

	if not check_for_user:
		cur.execute('insert into USERS (id, token) values(%s, %s)',
			[response.json().get('user_id'), response.json().get('access_token')])
	else:
		cur.execute('update USERS set token = (%s) where id = (%s)',
				[response.json().get('access_token'), response.json().get('user_id')])
	db.commit()

	session['logged_in'] = True
	session['user_id'] = response.json().get('user_id')
	data = {
		'user_id': session['user_id']
	}
	url = 'https://api.vk.com/method/users.get'
	response = requests.post(url, params=data).json()
	response = response['response'][0]
	session['first_name'] = response['first_name']
	session['last_name'] = response['last_name']
	return redirect(url_for('main.index'))


@auth.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('main.index'))
