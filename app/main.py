import psycopg2
import psycopg2.extras
from flask import Blueprint, redirect, render_template, session, abort, request, url_for
from app.auth import get_vk
from db_helper import get_db

main = Blueprint('main', __name__)


@main.route('/')
def index():
	db = get_db()
	cur = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute('select * from entries')
	entries = cur.fetchall()
	vk_info = get_vk()
	return render_template('index.html', vk_id=vk_info['id'], vk_url=vk_info['url'],
							session=session, entries=entries)


@main.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	cur = db.cursor()
	cur.execute('insert into entries (title, text, user_id) values (%s, %s, %s)',
				[request.form['title'], request.form['text'], session.get('user_id')])
	db.commit()
	return redirect(url_for('main.index'))


