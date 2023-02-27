from flask import Blueprint, request, render_template, redirect, session, url_for
from werkzeug.exceptions import BadRequest
from sqlalchemy import or_

from config.setup import db, logger
from log.utils import LogType, LogModule
from .model import User, Role
from project.model import Project

from .utils import login_required

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
@login_required
def retrieve_users():
	# Only administrators can see user list
	if not 'user' in session or not session['user']['admin']:
		return redirect(url_for('home'))
	
	users = User.query.all()
	roles = Role.query.all()
	projects = Project.query.all()

	# description = "Busqueda de usuarios"
	# logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.USERS.value, description)

	return render_template('/user/user_list.html', users=users, roles=roles, projects=projects)

@user_blueprint.route('/register', methods=['GET', 'POST'])
@login_required
def user_register():
	if request.method == 'GET':
		# only administrators can create users
		if 'user' in session and session['user']['admin']:
			roles = Role.query.all()
			projects = Project.query.all()
			return render_template('/user/user_register.html', roles=roles, projects=projects)
		
		return redirect(url_for('home'))
	
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		name = request.form['name']
		lastname = request.form['lastname']
		role_selected = request.form.get('role')
		project_selected = request.form.get('project')

		roles = Role.query.all()
		projects = Project.query.all()

		# Role exists
		role = Role.query.filter_by(name = role_selected).first()
		if role == None:
			error = "El rol suministrado no existe en la base de datos"
			return render_template(
				'/user/user_register.html', error = error, roles=roles, projects=projects)

		# Project exists
		project = Project.query.filter_by(description = project_selected).first()
		if project == None:
			error = "El proyecto suministrado no existe en la base de datos"
			return render_template(
				'/user/user_register.html', error = error, roles=roles, projects=projects)

		# User exists
		user = User.query.filter_by(username = username).first()
		if user:
			error = "Este nombre se usuario ya se encuentra registrado"
			return render_template(
				'/user/user_register.html', error = error, roles=roles, projects=projects)
		
		user = User(username, password, name, lastname, role.id, project.id)

		db.session.add(user)
		db.session.commit()

		description = f"Registro de usuario \"{user.username}\""
		logger.catch(session['user']['username'], LogType.ADD.value, LogModule.USERS.value, description)

		return redirect(url_for('user.retrieve_users'))

@user_blueprint.route('/login', methods=['GET', 'POST'])
def user_login():
	if request.method == 'GET':
		if 'user' in session and session['user']['admin']:
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
			   
		# description = "Acceso de usuario"
		# logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.USERS.value, description)

		return redirect(url_for('home'))

@user_blueprint.route('/logout')
@login_required
def user_logout():
	username = session['user']['username']

	if 'user' in session: 
		session.pop('user')
		session.pop('user_id')
	
	# description = "Salida de usuario"
	# logger.catch(username, LogType.SEARCH.value, LogModule.USERS.value, description)

	return redirect(url_for('home'))

@user_blueprint.route('/delete', methods=['POST'])
@login_required
def user_delete():
	id = request.form['id']

	# User exists
	user = User.query.filter_by(id = id).first()
	if user:
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

	# User exists
	user = User.query.filter_by(id = id).first()
	if not user:
		error = "El usuario suministrado no existe en la base de datos"
		raise BadRequest(error)
	
	user.name = name
	user.lastname = lastname
	user.role_id = role.id
	user.project_id = project.id

	db.session.commit()

	description = f"Modificación de usuario \"{user.username}\""
	logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.USERS.value, description)

	return redirect(url_for('user.retrieve_users'))

@user_blueprint.route('/search', methods=['GET'])
@login_required
def user_search():
	phrase = request.args.get('phrase')

	search = db.session.query(User).select_from(User).join(Role).join(Project).filter(
		or_(
			User.id.like('%' + phrase + '%'),
			User.username.like('%' + phrase + '%'),
			User.name.like('%' + phrase + '%'),
			User.lastname.like('%' + phrase + '%'),
			Role.name.like('%' + phrase + '%'),
			Project.description.like('%' + phrase + '%')
		)
	)

	roles = Role.query.all()
	projects = Project.query.all()

	description = f"Busqueda de usuarios por frase \"{phrase}\""
	logger.catch(session['user']['username'], LogType.SEARCH.value, LogModule.USERS.value, description)

	return render_template('/user/user_list.html', users=search.all(), roles=roles, projects=projects)

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
					'/user/user_password_reset.html', error = "Las credenciales suministradas no son validas")
			else:
				user.password = user.generate_password(password_next)
				db.session.commit()

				description = f"Cambio de contraseña de usuario \"{user.username}\""
				logger.catch(session['user']['username'], LogType.MODIFY.value, LogModule.USERS.value, description)

				return redirect(url_for('user.user_login'))
					
		else:
			return render_template(
				'/user/user_password_reset.html', error ="El nombre de usuario suministrado no existe")
