import os

from flask import Flask, render_template, session, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app)


def create_app(name_of_config):
    from vkpoll.blueprints.auth import auth
    app.register_blueprint(auth)

    from vkpoll.blueprints.poll import poll
    app.register_blueprint(poll)

    app.config.from_object(config[name_of_config])

    @app.route('/')
    def index():
        if session.get('logged_in'):
            return redirect(url_for('poll.my_polls'))
        return render_template('index.html')

    return app
