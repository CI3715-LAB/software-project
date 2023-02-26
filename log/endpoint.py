from flask import Blueprint, request, render_template, redirect, session, url_for
from sqlalchemy import or_, select

from config.setup import db
from .model import Log, Module, Type

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
@log_blueprint.route('/detail/<int:id>', methods=['GET'])
def retrieve_log(id):
	log = Log.query.filter_by(id = id).first()

	return render_template('/log/log_details.html',
		log=log,
		loggedIn= 'user' in session,
		user=session.get('user')
	)

# delete log
@log_blueprint.route('/delete', methods=['POST'])
def delete_log():
	id = request.form['id']

	# Log exists
	log = Log.query.filter_by(id = id).first()
	if log:
		db.session.delete(log)
		db.session.commit()

	return redirect(url_for('log.retrieve_logs'))

@log_blueprint.route('/search', methods=['GET'])
def search_log():
	phrase = request.args.get('phrase')

	logs = db.session.query(Log).select_from(Log).join(Type).join(Module).filter(
		or_(
			Log.id.like('%' + phrase + '%'),
			Log.description.like('%' + phrase + '%'),
			Log.date.like('%' + phrase + '%'),
			Log.time.like('%' + phrase + '%'),
			Type.name.like('%' + phrase + '%'),
			Module.name.like('%' + phrase + '%')
		)
	).all()


	return render_template('/log/log_list.html', logs=logs, phrase=phrase)
