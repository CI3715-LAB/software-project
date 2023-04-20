from flask import Blueprint, request, render_template, redirect, session, url_for
from werkzeug.exceptions import BadRequest
from sqlalchemy import or_

from config.setup import db, logger
from log.utils import LogType, LogModule
from .model import User, Role
from project.model import Project
from department.model import Department

from .utils import login_required

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
@login_required
def retrieve_users():
	# Only administrators can see user list
	if not 'user' in session or not session['user']['admin']:
		return redirect(url_for('home'))
	
	users = User.query.filter(User.id != 0).all()
	roles = Role.query.all()
	projects = Project.query.all()
	departments = Department.query.all()

	return render_template('/user/user_list.html', users=users, roles=roles, projects=projects, departments=departments, user=session.get('user'))

@user_blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def user_register():
	if request.method == 'GET':
		# only administrators can create users
		if 'user' in session and session['user']['admin']:
			roles = Role.query.all()
			projects = Project.query.all()
			departments = Department.query.all()
			return render_template('/user/user_register.html', roles=roles, projects=projects, departments=departments, user=session.get('user'))
		
		return redirect(url_for('home'))
	
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		name = request.form['name']
		lastname = request.form['lastname']
		role_selected = request.form.get('role')
		project_selected = request.form.get('project')
		department_selected = request.form.get('department')

		roles = Role.query.all()
		projects = Project.query.all()
		departments = Department.query.all()

		# Role exists
		role = Role.query.filter_by(name = role_selected).first()
		if role == None:
			error = "El rol suministrado no existe en la base de datos"
			return render_template(
				'/user/user_register.html', error = error, roles=roles, projects=projects, departments=departments, user=session.get('user'))

		# Project exists
		project = Project.query.filter_by(description = project_selected).first()
		if project == None:
			error = "El proyecto suministrado no existe en la base de datos"
			return render_template(
				'/user/user_register.html', error = error, roles=roles, projects=projects, departments=departments, user=session.get('user'))
		
		# Department exists
		department = Department.query.filter_by(name = department_selected).first()
		if department == None:
			error = "El departamento suministrado no existe en la base de datos"
			return render_template(
				'/user/user_register.html', error = error, roles=roles, projects=projects, departments=departments, user=session.get('user'))

		# User exists
		user = User.query.filter_by(username = username).first()
		if user:
			error = "Este nombre se usuario ya se encuentra registrado"
			return render_template(
				'/user/user_register.html', error = error, roles=roles, projects=projects, departments=departments, user=session.get('user'))
		
		user = User(username, password, name, lastname, role.id, project.id, department.id)

		db.session.add(user)
		db.session.commit()

		description = f"Registro de usuario \"{user.username}\""
		logger.catch(session['user']['username'], LogType.ADD.value, LogModule.USERS.value, description)

		return redirect(url_for('user.retrieve_users'))

@user_blueprint.route('/login', methods=['GET', 'POST'])
def user_login():
	if request.method == 'GET':
		if 'user' in session:
			return redirect(url_for('user.retrieve_users'))
		
		return render_template('/user/user_login.html', user=session.get('user'))
	
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		# User exists
		user = User.query.filter_by(username = username).first()
		if user:
			check = user.check_password(password)
			if not check:
				return render_template(
					'/user/user_login.html', error = "Las credenciales suministradas no son validas")
			else:
				session['user'] = {'id': user.id, 'username': user.username, 'role': user.role.name, 'admin': user.role.name == 'admin'}
				session['user_id'] = user.id
					
		else:
			return render_template(
				'/user/user_login.html', error = "El nombre de usuario suministrado no existe")

		return redirect(url_for('home'))

@user_blueprint.route('/logout')
@login_required
def user_logout():
	if 'user' in session: 
		session.pop('user')
		session.pop('user_id')

	return redirect(url_for('home'))

@user_blueprint.route('/delete', methods=['POST'])
@login_required
def user_delete():
	id = request.form['id']

	# User exists
	user = User.query.filter_by(id = id).first()
	if user:
		projects = Project.query.filter_by(manager_id = user.id)
		for project in projects:
			project.manager_id = 0
			project.manager = User.query.filter_by(id = 0).first()

		db.session.delete(user)
		db.session.commit()

	description = f"Eliminado usuario \"{user.username}\""
	logger.catch(session['user']['username'], LogType.DELETE.value, LogModule.USERS.value, description)

	return redirect(url_for('user.retrieve_users'))

@user_blueprint.route('/update', methods=['POST'])
@login_required
def user_update():
	id = request.form['id']
	name = request.form['name']
	lastname = request.form['lastname']
	role_selected = request.form.get('role')
	project_selected = request.form.get('project')
	department_selected = request.form.get('department')

	# Role exists
	role = Role.query.filter_by(name = role_selected).first()
	if role == None:
		error = "El rol suministrado no existe en la base de datos"
		raise BadRequest(error)

	# Project exists
	project = Project.query.filter_by(description = project_selected).first()
	if project == None:
		error = "El proyecto suministrado no existe en la base de datos"
		raise BadRequest(error)
	
	# Department exists
	department = Department.query.filter_by(name = department_selected).first()
	if department == None:
		error = "El departamento suministrado no existe en la base de datos"
		raise BadRequest(error)

	# User exists
	user = User.query.filter_by(id = id).first()
	if not user:
		error = "El usuario suministrado no existe en la base de datos"
		raise BadRequest(error)
	
	user.name = name
	user.lastname = lastname
	user.role_id = role.id
	user.project_id = project.id
	user.department_id = department.id

	db.session.commit()

	description = f"Modificación de usuario \"{user.username}\""
	logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.USERS.value, description)

	return redirect(url_for('user.retrieve_users'))

@user_blueprint.route('/search', methods=['GET'])
@login_required
def user_search():
	phrase = request.args.get('phrase')

	if not phrase:
		return redirect(url_for('user.retrieve_users'))

	search = db.session.query(User).select_from(User).join(Role).join(Project).join(Department).filter(
		or_(
			User.id.like('%' + phrase + '%'),
			User.username.like('%' + phrase + '%'),
			User.name.like('%' + phrase + '%'),
			User.lastname.like('%' + phrase + '%'),
			Role.name.like('%' + phrase + '%'),
			Project.description.like('%' + phrase + '%'),
			Department.name.like('%' + phrase + '%')
		)
	)

	roles = Role.query.all()
	projects = Project.query.all()
	departments = Department.query.all()

	description = f"Busqueda de usuarios por frase \"{phrase}\""
	logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.USERS.value, description)

	return render_template('/user/user_list.html', users=search.all(), roles=roles, projects=projects, departments=departments, phrase=phrase, user=session.get('user'))

@user_blueprint.route('/reset', methods=['GET','POST'])
@login_required
def user_reset():
	if request.method == 'GET':
		if 'user' in session and session['user']['admin']:
			return render_template('/user/user_password_reset.html', user=session.get('user'))
		
		return redirect(url_for('home'))
		
	if request.method == 'POST':
		username = request.form['username']
		password_prev = request.form['password_prev']
		password_next = request.form['password_next']

		# User exists
		user = User.query.filter_by(username = username).first()
		if user:
			check = user.check_password(password_prev)
			if not check:
				return render_template(
					'/user/user_password_reset.html', error = "Las credenciales suministradas no son validas", user=session.get('user'))
			else:
				user.password = user.generate_password(password_next)
				db.session.commit()

				description = f"Cambio de contraseña de usuario \"{user.username}\""
				logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.USERS.value, description)

				return redirect(url_for('user.user_login'))
					
		else:
			return render_template(
				'/user/user_password_reset.html', error ="El nombre de usuario suministrado no existe", user=session.get('user'))
