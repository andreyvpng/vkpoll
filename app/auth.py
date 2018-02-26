import requests
from flask import Blueprint, request, abort, redirect, url_for, session
from db_helper import create_new_user, update_token_of_user, get_user

auth = Blueprint('auth', __name__)


def get_vk():
	from main import app
	ans = {
		'id': app.config['VK_API_ID'],
		'secret': app.config['VK_API_SECRET'],
		'url': app.config['VK_API_URL']
	}
	return ans


@auth.route('/login')
def login():
	if request.args.get('code') is None:
		return abort(501)

	# Get api token
	vk_info = get_vk()
	data = {
		'client_id': vk_info['id'],
		'client_secret': vk_info['secret'],
		'redirect_uri': vk_info['url'],
		'code': request.args.get('code')
	}
	response = requests.post('https://oauth.vk.com/access_token', params=data)

	if response.json().get('access_token') is None:
		abort(501)

	# Check if the user in the database
	check_of_user = get_user(response.json().get('user_id'))
	if not check_of_user:
		create_new_user(response.json().get('user_id'), response.json().get('access_token'))
	else:
		update_token_of_user(response.json().get('access_token'), response.json().get('user_id'))

	# Get information about the user
	data = {'user_id': response.json().get('user_id')}
	url = 'https://api.vk.com/method/users.get'
	response = requests.post(url, params=data).json()['response'][0]

	information_about_user = {
		'logged_in': True,
		'user_id': response['uid'],
		'first_name': response['first_name'],
		'last_name': response['last_name']
	}
	session.update(information_about_user)
	return redirect(url_for('main.index'))


@auth.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('main.index'))
