import urllib.parse

import requests
from flask import Blueprint, session, request, redirect, abort, flash, url_for

from vkpoll import db
from ..models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')


def get_vk():
    from vkpoll import app
    ans = {
        'id': app.config['VK_API_ID'],
        'secret': app.config['VK_API_SECRET'],
        'url': app.config['VK_API_URL']
    }
    return ans


@auth.route('/testing', methods=['POST'])
def login_testing():
    from vkpoll import app
    if app.config.get('testing'):
        information_about_user = {
            'logged_in': True,
            'id': request.form['user_id'],
            'token': request.form['token'],
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name']
        }
        session.update(information_about_user)
        check_of_user = User.query.filter_by(id=session['id']).all()
        if not check_of_user:
            db.session.add(User(session['id'], session['token']))
        else:
            check_of_user[0].update(session['token'])

    return 'ID: %s' % session.get('id')


@auth.route('/')
def login():
    """ Redirecting to VK to get the code """
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

    url = 'https://oauth.vk.com/authorize?{0}'.format(params)
    return redirect(url)


@auth.route('/get_token')
def get_token():
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
    check_of_user = User.query.filter_by(
        id=response.json().get('user_id')).first()
    if not check_of_user:
        new_user = User(
            response.json().get('user_id'),
            response.json().get('access_token')
        )
        db.session.add(new_user)
    else:
        check_of_user.update(response.json().get('access_token'))

    db.session.commit()

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
        'id': response.get('id'),
        'first_name': response.get('first_name'),
        'last_name': response.get('last_name')
    }
    session.update(information_about_user)
    flash('Welcome! You were logged in', category='success')
    return redirect(session['previous_url'])


@auth.route('/logout')
def logout():
    session.clear()
    flash('You were logged out', category='success')
    return redirect(url_for('index'))
