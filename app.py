from flask import Flask, render_template, session, redirect, url_for
from flask_assets import Environment, Bundle
from sqlalchemy import text

from config.setup import db, SECRET_KEY
from user.endpoint import user_blueprint
from project.endpoint import project_blueprint
from client.endpoint import client_blueprint
from vehicle.endpoint import vehicle_blueprint
from log.endpoint import log_blueprint
from department.endpoint import department_blueprint
from log.model import Log

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_object('config.setup.DevelopmentConfig')
	else:
		# load the test config if passed in
		app.config.from_object(test_config)

		import logging
		log = logging.getLogger('werkzeug')
		log.setLevel(logging.ERROR)
	
	# Assets Bundle initialization
	assets = Environment(app)
	assets.url = app.static_url_path
	scss = Bundle('scss/*.scss', filters='pyscss, cssmin', output='css/all.css')
	assets.register('scss_all', scss)

	# DB initialization
	db.init_app(app)
	with app.app_context():
		db.drop_all()
		db.create_all()

		if test_config is None:
			# Fill database with initial data
			with open('init.sql') as f:
				for line in f:
					db.session.execute(text(line))
			db.session.commit()

	# Blueprints Registration (Endpoints)
	from user.endpoint import user_blueprint
	from project.endpoint import project_blueprint
	from log.endpoint import log_blueprint

	app.register_blueprint(user_blueprint, url_prefix='/user') # User endpoints
	app.register_blueprint(project_blueprint, url_prefix='/project') # Project endpoints
	app.register_blueprint(client_blueprint, url_prefix='/client') # Client endpoints
	app.register_blueprint(vehicle_blueprint, url_prefix='/vehicle') # Vehicle endpoints
	app.register_blueprint(log_blueprint, url_prefix='/log') # Log endpoints
	app.register_blueprint(department_blueprint, url_prefix='/department') # Department endpoints

	@app.context_processor
	def inject_user_from_session():
		loggedIn = False
		user = None
			
		if 'user' in session:
			loggedIn = True
			user = session['user']
			
		return dict(user=user, loggedIn=loggedIn)
	
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

	return app


# Runner
if __name__ == '__main__':
	app = create_app()
	app.run()