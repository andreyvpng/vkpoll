from functools import wraps
from random import choice
from string import ascii_letters

from flask import Blueprint, redirect, render_template, session, abort, \
    request, url_for, flash

from app import database

main = Blueprint('main', __name__)


def is_logged(func):
    """ Processing requests for unauthorized users """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            flash('You are not authorized!', category='danger')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return wrapper


@main.route('/')
def index():
    if session.get('logged_in'):
        polls = database.get_polls_of_user(session.get('user_id'))
        return render_template('my_polls.html', polls=polls), 200
    return render_template('index.html'), 200


@main.route('/add_poll', methods=['GET', 'POST'])
@is_logged
def add_poll():
    if request.method == "POST":
        while True:
            url_length = 8
            url_of_poll = ''.join(choice(ascii_letters) for _ in range(url_length))
            if database.is_url_available(url_of_poll):
                break
        choices = request.form.getlist('choice')
        database.create_new_poll(
            url_of_poll,
            session['user_id'],
            request.form['title'], choices
        )
        flash('Poll successfully created', category='success')
        return redirect(url_for('main.show_poll', url_of_poll=url_of_poll))
    return render_template('add_poll.html')


@main.route('/del_poll_<poll_id>', methods=['POST'])
@is_logged
def dell_poll(poll_id):
    poll = database.get_poll_via_id(poll_id)
    if poll.get('user_id') == session.get('user_id'):
        database.delete_poll(poll_id)
    else:
        flash(
            'You do not have the right to remove this poll!',
            category='danger'
        )
        return redirect(url_for('main.index'))
    flash('Poll successfully deleted', category='success')
    return redirect(url_for('main.index'))


@main.route('/poll_<url_of_poll>')
def show_poll(url_of_poll):
    poll = database.get_poll_via_url(url_of_poll)
    if not poll:
        abort(404)

    options = database.get_possible_choice(poll['id'])
    user_choice = None
    if session.get('logged_in'):
        user_choice = database.is_user_take_part(session['user_id'], poll['id'])
    return render_template(
        'poll.html', poll=poll, options=options, user_choice=user_choice
    )


@main.route('/make_choice', methods=['POST'])
@is_logged
def make_choice():
    poll_id = request.form.get('poll_id')
    choice_id = request.form.get('choice_id')
    user_choice = database.is_user_take_part(session['user_id'], poll_id)

    if not user_choice:
        database.create_choice(session['user_id'], poll_id, choice_id)
        flash('You have successfully voted', category='success')
    return redirect(
        url_for('main.show_poll', url_of_poll=request.form.get('poll_url'))
    )
