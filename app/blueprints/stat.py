from app import database
from flask import Blueprint, render_template

stat = Blueprint('stat', __name__)


@stat.route('/')
def show_stat():
	return render_template('stat.html', stat=database.get_stat())
