import os
from urllib import parse

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    parse.uses_netloc.append("postgres")
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    url = parse.urlparse(os.environ.get("DATABASE_URL"))

    VK_API_ID = os.environ.get('VK_API_ID')
    VK_API_SECRET = os.environ.get('VK_API_SECRET')
    VK_API_URL = os.environ.get('VK_API_URL')


class DevelopmentConfig(Config):
    DEBUG = True


class HerokuConfig(Config):
    DEBUG = False


config = {
    'heroku': HerokuConfig,
    'development': DevelopmentConfig
}
