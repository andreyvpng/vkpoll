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
	db = get_db()
	cur = db.cursor()
	with app.open_resource('schema.sql', mode='r') as f:
		cur.execute(f.read())

	print('-' * 8)
	print('VK API')
	print('write: id secret url')
	print('-' * 8)
	vk_id, vk_secret, vk_url = input().split()
	cur.execute('insert into vk_api (id, secret, url) values(%s, %s, %s)', [vk_id, vk_secret, vk_url])
	db.commit()
