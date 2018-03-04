import os
from flask import Flask, g
from db_helper import init_db
from config import config
from app.main import main as main_blueprint
from app.auth import auth as auth_blueprint

app = Flask(__name__)
app.config.from_object(
	config[os.environ.get('FLASK_CONFIG') or 'development']
)


@app.cli.command('init_db')
def init_db_command():
	init_db(app)
	print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'db'):
		g.db.close()


app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')


if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
