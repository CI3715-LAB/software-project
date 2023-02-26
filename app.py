from flask import Flask, render_template, session
from flask_assets import Environment, Bundle
from os import environ

from config.setup import db, SECRET_KEY
from user.endpoint import user_blueprint
from project.endpoint import project_blueprint
from log.endpoint import log_blueprint

# Flask initialization
app = Flask(__name__)
app.app_context().push()
app.config.from_object('config.setup.DevelopmentConfig')

# Assets Bundle initialization
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/*.scss', filters='pyscss, cssmin', output='css/all.css')
assets.register('scss_all', scss)

# DB initialization
db.init_app(app)
@app.before_first_request
def create_table():
    db.create_all()

@app.context_processor
def inject_user_from_session():
    loggedIn = False
    user = None
        
    if 'user' in session:
        loggedIn = True
        user = session['user']
        
    return dict(user=user, loggedIn=loggedIn)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Blueprints Registration (Endpoints)
app.register_blueprint(user_blueprint, url_prefix='/user') # User endpoints
app.register_blueprint(project_blueprint, url_prefix='/project') # Project endpoints
app.register_blueprint(log_blueprint, url_prefix='/log') # Log endpoints

# Runner
if __name__ == '__main__':
    app.run()