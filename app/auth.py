import requests
import urllib
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


@auth.route('/redirect_to_vk_login', methods=['POST', 'GET'])
def vk_login():
	session['previous_url'] = request.referrer

	vk_info = get_vk()
	params = urllib.parse.urlencode(
		{
			'client_id': vk_info['id'],
			'display': 'popup',
			'redirect_uri': vk_info['url'],
			'response_type': 'code',
			'v': 5.73
		}
	)
	url = 'https://oauth.vk.com/authorize?%s' % params
	return redirect(url)


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
	data = {
		'user_ids': response.json().get('user_id'),
		'fields': 'bdate',
		'v': 5.73
	}
	url = 'https://api.vk.com/method/users.get'
	response = requests.post(url, params=data).json()
	response = response.get('response')[0]

	information_about_user = {
		'logged_in': True,
		'user_id': response.get('id'),
		'first_name': response.get('first_name'),
		'last_name': response.get('last_name')
	}
	session.update(information_about_user)
	return redirect(session['previous_url'])


@auth.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('main.index'))
