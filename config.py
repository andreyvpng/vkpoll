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

    # DATABASE_NAME = url.path[1:]
    # DATABASE_USER = url.username
    # DATABASE_PASSWORD = url.password
    # DATABASE_HOST = url.hostname
    # DATABASE_PORT = url.port


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig
}
