from flask import Blueprint, request, render_template, redirect, url_for, session
from sqlalchemy import or_
from config.setup import db, logger
from log.utils import LogType, LogModule
from .model import Department
from user.model import User
from werkzeug.exceptions import BadRequest

from user.utils import login_required

department_blueprint = Blueprint('department', __name__)

@department_blueprint.route('/')
@login_required
def retrieve_departments():
    # return all departments with an id different than 0
	departments = Department.query.filter(Department.id != 0).all()

	return render_template('/department/department_list.html',
		departments=departments, loggedIn= 'user' in session,
		user=session.get('user')
	)

@department_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_department():
	if request.method == 'GET':
		return render_template('/department/department_add.html',
			loggedIn= 'user' in session,
			user=session.get('user')                    
		)

	if request.method == 'POST':
		# get name
		name = request.form['name']

		# check name is not already in use
		if Department.query.filter_by(name=name).first():
			return render_template('/department/department_add.html',
				name=name,
				loggedIn= 'user' in session,
				user=session.get('user'),
				error='Ya existe un departamento con ese nombre'
			)

		# create a new department
		department = Department(name)

		# add department to db
		db.session.add(department)
		db.session.commit()

		# log the event
		description = f"Creación de departamento \"{department.name}\""
		logger.catch(session['user']['username'], LogType.ADD.value, LogModule.DEPARTMENTS.value, description)

		return redirect(url_for('department.retrieve_departments'))
	
@department_blueprint.route('/update', methods=['POST'])
@login_required
def update_department():
	# get name
	id = request.form['id']
	name = request.form['name']

	# check name is not already in use
	department = Department.query.filter_by(name=name).first()
	if department and department.id != int(id):
		return render_template('/department/department_add.html',
			loggedIn= 'user' in session,
			user=session.get('user'),
			error='Ya existe un departamento con ese nombre'
		)
	
	# update department
	department = Department.query.filter_by(id=id).first()
	department.name = name
	db.session.commit()

	# log the event
	description = f"Modificación de departamento \"{department.name}\""
	logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.DEPARTMENTS.value, description)

	return redirect(url_for('department.retrieve_departments'))

@department_blueprint.route('/delete', methods=['POST'])
@login_required
def delete_department():
	id = request.form['id']

	if id == '0':
		raise BadRequest('No se puede eliminar el departamento Undefined')
	

	# Department exists
	department = Department.query.filter_by(id=id).first()
	if department:
		for user in department.users:
			user.department_id = 0
			user.department = Department.query.filter_by(id=0).first()
			db.session.commit()
		db.session.delete(department)
		db.session.commit()

	# log the event
	description = f"Eliminado departamento \"{department.name}\""
	logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.DEPARTMENTS.value, description)

	return redirect(url_for('department.retrieve_departments'))

@department_blueprint.route('/search', methods=['GET'])
@login_required
def search_department():
	phrase = request.args.get('phrase')

	if not phrase:
		return redirect(url_for('department.retrieve_departments'))

	departments = db.session.query(Department).select_from(Department).join(User).filter(
        or_(
            Department.id.like('%' + phrase + '%'),
            Department.name.like('%' + phrase + '%'),
            User.name.like('%' + phrase + '%'),
            User.username.like('%' + phrase + '%'),
        )
    ).filter(Department.id != 0)

	description = f"Busqueda de departamentos por frase \"{phrase}\""
	logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.DEPARTMENTS.value, description)

	return render_template('/department/department_list.html', departments=departments, phrase=phrase, loggedIn= 'user' in session, user=session.get('user'))
