from flask import Flask, render_template, session
from flask_assets import Environment, Bundle
import secrets

from config.setup import db
from user.endpoint import user_blueprint

# Flask initialization
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets.token_hex(16)

# Assets Bundle initialization
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/main.scss', filters='pyscss', output='css/all.css')
assets.register('scss_all', scss)

# DB initialization
db.init_app(app)
@app.before_first_request
def create_table():
    db.create_all()

# Home route
@app.route('/')
def home():
    loggedIn = 'user' in session
    return render_template('index.html', loggedIn = loggedIn)

# Blueprints Registration (Endpoints)
app.register_blueprint(user_blueprint, url_prefix='/user') # User endpoints

# Runner
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)