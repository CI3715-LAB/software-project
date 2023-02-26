from flask import Blueprint, request, render_template, redirect, session
from sqlalchemy import or_

from config.setup import db
from .model import User, Role
from project.model import Project

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def retrieve_users():
    # Only administrators can see user list
    if not 'user' in session or not session['user']['admin']:
        return redirect('/')
    
    users = User.query.all()
    roles = Role.query.all()
    projects = Project.query.all()
    return render_template('/user/user_list.html', users=users, roles=roles, projects=projects)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        # only administrators can create users
        if 'user' in session and session['user']['admin']:
            roles = Role.query.all()
            projects = Project.query.all()
            return render_template('/user/user_register.html', roles=roles, projects=projects)
        
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        lastname = request.form['lastname']
        role_selected = request.form.get('role')
        project_selected = request.form.get('project')

        # Role exists
        role = Role.query.filter_by(name = role_selected).first()
        if role == None:
            error = "El rol suministrado no existe en la base de datos"
            return redirect('/user')

        # Project exists
        project = Project.query.filter_by(description = project_selected).first()
        if project == None:
            error = "El proyecto suministrado no existe en la base de datos"
            return redirect('/user')

        # User exists
        user = User.query.filter_by(username = username).first()
        if user:
            error = "Este nombre se usuario ya se encuentra registrado"
            return render_template(
                '/user/user_register.html', error = error)
        
        user = User(username, password, name, lastname, role.id, project.id)

        db.session.add(user)
        db.session.commit()
        return redirect('/user')

@user_blueprint.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        if 'user' in session and session['user']['admin']:
            return redirect('/user')
        
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
                    
        else:
            return render_template(
                '/user/user_login.html', error = "El nombre de usuario suministrado no existe")
               
        return redirect('/')

@user_blueprint.route('/logout')
def user_logout():
    if 'user' in session: 
        session.pop('user')
    
    return redirect('/')

@user_blueprint.route('/delete', methods=['POST'])
def user_delete():
    id = request.form['id']

    # User exists
    user = User.query.filter_by(id = id).first()
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect('/user')

@user_blueprint.route('/update', methods=['POST'])
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
        return redirect('/user')

    # Project exists
    project = Project.query.filter_by(description = project_selected).first()
    if project == None:
        error = "El proyecto suministrado no existe en la base de datos"
        return redirect('/user')

    # User exists
    user = User.query.filter_by(id = id).first()
    if not user:
        error = "El usuario suministrado no existe en la base de datos"
        return redirect('/user')
    
    user.name = name
    user.lastname = lastname
    user.role_id = role.id
    user.project_id = project.id

    db.session.commit()
    return redirect('/user')

@user_blueprint.route('/search', methods=['GET'])
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

    return render_template('/user/user_list.html', users=search.all(), roles=roles, projects=projects)

@user_blueprint.route('/reset', methods=['GET','POST'])
def user_reset():
    if request.method == 'GET':
        if 'user' in session and session['user']['admin']:
            return render_template('/user/user_password_reset.html', user=session.get('user'))
        
        return redirect('/')
        
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
                    '/user/user_login.html', error = "Las credenciales suministradas no son validas")
            else:
                user.password = user.generate_password(password_next)
                db.session.commit()
                return redirect("/user/login")
                    
        else:
            return render_template(
                '/user/user_login.html', error ="El nombre de usuario suministrado no existe")
               
        return redirect('/')