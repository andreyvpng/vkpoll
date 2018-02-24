import psycopg2
import psycopg2.extras
from flask import g


def connect_db():
	from main import app
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
