from random import choice
from string import ascii_letters
from flask import Blueprint, redirect, render_template, session, abort, request, url_for
from db_helper import get_polls_of_user, get_poll, get_possible_choice, create_new_poll, \
	create_choice, check_part_in_poll

main = Blueprint('main', __name__)


@main.route('/')
def index():
	from main import app
	polls = None
	if session.get('logged_in'):
		polls = get_polls_of_user(session.get('user_id'))
	return render_template('index.html', vk_id=app.config['VK_API_ID'], vk_url=app.config['VK_API_URL'], polls=polls)


@main.route('/add_poll', methods=['GET', 'POST'])
def add_poll():
	if not session.get('logged_in'):
		abort(401)

	if request.method == "POST":
		url_of_poll = ''.join(choice(ascii_letters) for _ in range(30))
		choices = request.form.getlist('choice')
		print(request.form['title'])
		create_new_poll(url_of_poll, session['user_id'], request.form['title'], choices)
		return redirect(url_for('main.show_poll', url_of_poll=url_of_poll))
	return render_template('add_poll.html')


@main.route('/poll_<url_of_poll>')
def show_poll(url_of_poll):
	if not session.get('logged_in'):
		abort(401)
	poll = get_poll(url_of_poll)
	if not poll:
		abort(404)

	options = get_possible_choice(poll['id'])
	user_choice = check_part_in_poll(session['user_id'], options)
	return render_template('poll.html', poll=poll, options=options, user_choice=user_choice)


@main.route('/make_choice', methods=['POST'])
def make_choice():
	if not session.get('logged_in'):
		abort(401)

	poll_id = request.form.get('poll_id')
	choice_id = request.form.get('choice_id')

	options = get_possible_choice(poll_id)
	user_choice = check_part_in_poll(session['user_id'], options)

	if not user_choice['answered']:
		create_choice(session['user_id'], poll_id, choice_id)
	return redirect(url_for('main.show_poll', url_of_poll=request.form.get('poll_url')))
