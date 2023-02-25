from flask import Blueprint, request, render_template, redirect, session

from config.setup import db
from .model import Log

log_blueprint = Blueprint('log', __name__)

# get all logs
@log_blueprint.route('/')
def retrieve_logs():
	logs = Log.query.all()
	return render_template('/log/log_list.html', logs=logs)

# get log details
@log_blueprint.route('/<int:id>')
def retrieve_log(id):
	log = Log.query.get(id)
	return render_template('/log/log_details.html', log=log)

# delete log
@log_blueprint.route('/delete/<int:id>')
def delete_log(id):
	log = Log.query.get(id)
	db.session.delete(log)
	db.session.commit()
	return redirect('/')