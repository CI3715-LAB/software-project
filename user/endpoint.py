from flask import Blueprint, request, render_template, redirect, session

from config.setup import db
from .model import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def retrieve_users():
    if not 'user' in session: return redirect('/user/login')
    users = User.query.all()
    return render_template('/user/user_list.html', users = users)

@user_blueprint.route('/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        if 'user' in session: return redirect('/user')
        return render_template('/user/user_register.html')
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User(username = username, email=email, password=password)

        db.session.add(user)
        db.session.commit()
        return redirect('/user')

@user_blueprint.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        if 'user' in session: return redirect('/user')
        return render_template('/user/user_login.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # User exists
        user = User.query.filter_by(username = username).first()
        if (user):
            check = User.check_password(user, password)
            if (not check):
                return render_template(
                    '/user/user_login.html', error = "Credentials do not match")
            else:
                session['user'] = user.id
                    
        else:
            return render_template(
                '/user/user_login.html', error = "User does not exists")
               
        return redirect('/')

@user_blueprint.route('/logout')
def user_logout():
    if 'user' in session: 
        session.pop('user')
    
    return redirect('/')