import os
from urllib import parse


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	VK_API_ID = os.environ.get('VK_API_ID')
	VK_API_SECRET = os.environ.get('VK_API_SECRET')
	VK_API_URL = os.environ.get('VK_API_URL')


class DevelopmentConfig(Config):
	DEBUG = True
	DATABASE_NAME = 'new_database'
	DATABASE_USER = 'postgres'
	DATABASE_PASSWORD = 'q'
	DATABASE_HOST = '127.0.0.1'
	DATABASE_PORT = '5432'


class HerokuConfig(Config):
	parse.uses_netloc.append("postgres")
	url = parse.urlparse(os.environ.get("DATABASE_URL"))

	DEBUG = False
	DATABASE_NAME = url.path[1:]
	DATABASE_USER = url.username
	DATABASE_PASSWORD = url.password
	DATABASE_HOST = url.hostname
	DATABASE_PORT = url.port


config = {
	'development': DevelopmentConfig,
	'heroku': HerokuConfig
}
