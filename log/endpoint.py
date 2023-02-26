from flask import Blueprint, request, render_template, redirect, session, url_for

from config.setup import db
from .model import Log

log_blueprint = Blueprint('log', __name__)

# get all logs
@log_blueprint.route('/')
def retrieve_logs():
	# if no parameters are given return all logs
	if not request.args:
		logs = Log.query.all()
		return render_template('/log/log_list.html',
			logs=logs,
			loggedIn= 'user' in session,
			user=session.get('user')
		)

    # look for logs with a similar description to the one given
	description = request.args.get('description')
	logs = Log.query.filter(
		Log.description.like('%' + description + '%')
	).all()
	return render_template('/log/log_list.html',
		logs=logs, description=description,
		loggedIn= 'user' in session,
	    user=session.get('user')
	)
	

# get log details
@log_blueprint.route('/<int:id>')
def retrieve_log(id):
	log = Log.query.get(id)
	return render_template('/log/log_details.html',
		log=log,
		loggedIn= 'user' in session,
	    user=session.get('user')
	)

# delete log
@log_blueprint.route('/delete/<int:id>')
def delete_log(id):
	log = Log.query.get(id)
	db.session.delete(log)
	db.session.commit()
	return redirect(url_for('log.retrieve_logs'))