import psycopg2
import psycopg2.extras
from flask import g


def connect_db():
	from app import app
	conn = psycopg2.connect(
		database=app.config['DATABASE_NAME'],
		user=app.config['DATABASE_USER'],
		password=app.config['DATABASE_PASSWORD'],
		host=app.config['DATABASE_HOST'],
		port=app.config['DATABASE_PORT']
	)
	return conn


def get_db():
	if not hasattr(g, 'db'):
		g.db = connect_db()
	return g.db


def init_db(app):
	db = connect_db()
	cur = db.cursor()
	with app.open_resource('schema.sql', mode='r') as f:
		cur.execute(f.read())
	db.commit()


def create_new_user(user_id, user_token):
	db = get_db()
	cur = db.cursor()
	cur.execute('insert into USERS (id, token) values(%s, %s)', [user_id, user_token])
	db.commit()


def update_token_of_user(user_id, user_token):
	db = get_db()
	cur = db.cursor()
	cur.execute('update USERS set token = (%s) where id = (%s)', [user_id, user_token])
	db.commit()


def get_user(user_id):
	db = get_db()
	cur = db.cursor()
	cur.execute('select *from USERS where id = (%s)', [user_id])
	user = cur.fetchall()
	return user


def get_polls_of_user(user_id):
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('select * from polls where user_id = (%s)', [user_id])
	polls = cur.fetchall()
	return polls


def create_new_poll(poll_url, user_id, poll_question, choices):
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("insert into polls (url, user_id, question) values(%s, %s, %s)", [poll_url, user_id, poll_question])
	cur.execute('select *from polls where url = (%s)', [poll_url])
	pull_id = cur.fetchall()[0]['id']
	for possible_choice in choices:
		if possible_choice:
			cur.execute('insert into possible_choice(poll_id, text) values(%s, %s)', [pull_id, possible_choice])
	db.commit()


def get_poll_via_url(url_of_poll):
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('select *from polls where url = (%s)', [url_of_poll])
	poll = cur.fetchall()
	ans = dict()
	if poll:
		poll = poll[0]
		ans = {
			'title': poll['question'],
			'id': poll['id'],
			'user_id': poll['user_id'],
			'url': poll['url'],
			'time_of_creation': poll['time_of_creation']
		}
	return ans


def get_poll_via_id(poll_id):
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('select *from polls where id = (%s)', [poll_id])
	poll = cur.fetchall()
	ans = dict()
	if poll:
		poll = poll[0]
		ans = {
			'title': poll['question'],
			'id': poll['id'],
			'user_id': poll['user_id'],
			'url': poll['url'],
			'time_of_creation': poll['time_of_creation']
		}
	return ans


def delete_poll(poll_id):
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('delete from user_choice where poll_id = (%s)', [poll_id])
	cur.execute('delete from possible_choice where poll_id = (%s)', [poll_id])
	cur.execute('delete from polls where id = (%s)', [poll_id])
	db.commit()


def get_possible_choice(poll_id):
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('select * from possible_choice where poll_id = (%s)', [poll_id])
	options = cur.fetchall()
	ans = dict()
	for option in options:
		cur.execute("""select user_id from user_choice where poll_id = (%s) and
		choice_id= (%s);""", [option['poll_id'], option['id']])

		users = [item[0] for item in cur.fetchall()]
		ans[option['text']] = {
			'id': option['id'],
			'users': users,
			'count': len(users)
		}
	return ans


def is_user_take_part(user_id, options):
	user_choice = {
		'answered': False,
		'choice_id': None
	}
	for option in options.keys():
		user_choice['answered'] = user_choice['answered'] or (user_id in options[option]['users'])
		if user_choice['answered']:
			user_choice['choice_id'] = options[option]['id']
			break
	return user_choice


def create_choice(user_id, poll_id, choice_id):
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('insert into user_choice(user_id, poll_id, choice_id) values(%s, %s, %s)', [user_id, poll_id, choice_id])
	db.commit()


def is_url_available(url):
	db = get_db()
	cur = db.cursor()
	cur.execute('select from polls where url = (%s)', [url])
	poll = cur.fetchall()
	return len(poll) == 0
