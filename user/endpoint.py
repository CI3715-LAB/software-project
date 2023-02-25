from flask import Blueprint, request, render_template, redirect, session

from config.setup import db
from .model import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def retrieve_users():
    # Only administrators can see user list
    if not 'user' in session or not session['user']['admin']:
        return redirect('/')
    
    users = User.query.all()
    return render_template('/user/user_list.html', users=users)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        # only administrators can create users
        if 'user' in session and session['user']['admin']:
            return render_template('/user/user_register.html')
        
        return redirect('/')
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        admin = request.form.get('admin') == 'on'

        print(username, email, password, admin)
        
        user = User(username, email, password, admin)

        if user:
            print('user created')
        else:
            print('not created SAEREIAHFRUAEHK')

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
                    '/user/user_login.html', error = "Credentials do not match")
            else:
                session['user'] = {'id': user.id, 'username': user.username, 'role': user.role.name, 'admin': user.role.name == 'admin'}
                    
        else:
            return render_template(
                '/user/user_login.html', error = "User does not exists")
               
        return redirect('/')

@user_blueprint.route('/logout')
def user_logout():
    if 'user' in session: 
        session.pop('user')
    
    return redirect('/')