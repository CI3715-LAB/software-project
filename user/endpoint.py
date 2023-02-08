from flask import Blueprint, request, render_template, redirect

from config.setup import db
from .model import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def retrieve_users():
    users = User.query.all()
    return render_template('/user/user_list.html', users = users)

@user_blueprint.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'GET':
        return render_template('/user/user_add.html')
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/user')