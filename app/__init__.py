import os
from flask import Flask, g
from app.database import DataBase
from config import config

app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_CONFIG') or 'development'])
database = DataBase(app)   # connection database


@app.cli.command('init_db')
def init_db_command():
	database.init_db(app)
	print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'db'):
		g.db.close()


from app.blueprints.main import main as main_blueprint
from app.blueprints.auth import auth as auth_blueprint
from app.blueprints.stat import stat as stat_blueprint

app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(stat_blueprint, url_prefix='/stat')
