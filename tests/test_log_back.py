import unittest
from BaseTestCase import BaseTestCase, db, User
from log.model import Type, Module, Log

from helpers.login_user_back import login_user

class TestLog(BaseTestCase):
	@login_user
	def test_log_list(self):
		response = self.client.get('/log/')
		self.assert200(response)
		self.assertIn(b'Logger de Eventos', response.data)

	@login_user
	def test_log_list_empty(self):
		# delete all logs
		db.session.query(Log).filter(id != 0).delete()

		# show empty list
		response = self.client.get('/log/')
		self.assert200(response)
		self.assertIn(b'No hay eventos', response.data)

	@login_user
	def test_log_user_added(self):
		response = self.client.post('/user/register', data=dict(
			username='test_user_register',
			password='test_password',
			name='Test User',
			lastname='Test Lastname',
			role='admin',
			project='Test Project',
			enabled=True
		), follow_redirects=True)
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Registro de usuario "test_user_register"')
		response = self.client.get('/log/')
		self.assert200(response)

	@login_user
	def test_log_user_modified(self):
		user = User.query.filter_by(username='testUser').first()
		response = self.client.post('/user/update', data=dict(
			id=user.id,
			name='Test User Modified',
			lastname='Test Lastname Modified',
			role='admin',
			project='Test Project'
		), follow_redirects=True)
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Modificación de usuario "testUser"')
		response = self.client.get('/log/')
		self.assert200(response)

	@login_user
	def test_log_user_deleted(self):
		user = User.query.filter_by(username='testUser2').first()
		response = self.client.post('/user/delete', data=dict(
			id=user.id
		), follow_redirects=True)
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Eliminado usuario "testUser2"')
		response = self.client.get('/log/')
		self.assert200(response)

	@login_user
	def test_log_user_search(self):
		response = self.client.get("/user/search?phrase=testUser")
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Busqueda de usuarios por frase "testUser"')
		response = self.client.get('/log/')
		self.assert200(response)

	@login_user
	def test_log_project_added(self):
		response = self.client.post('/project/add', data=dict(
			description='Test Project Added',
			open_date='2023-01-01',
			close_date='2023-01-01',
			enabled=True
		), follow_redirects=True)
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Creación de proyecto "Test Project Added"')
		response = self.client.get('/log/')
		self.assert200(response)

	@login_user
	def test_log_project_modified(self):
		response = self.client.post('/project/update', data=dict(
			id=1,
			description='Test Project Modified',
			open_date='2023-01-01',
			close_date='2023-01-01'
		), follow_redirects=True)
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Modificación de proyecto "Test Project Modified"')
		response = self.client.get('/log/')
		self.assert200(response)

	@login_user
	def test_log_project_deleted(self):
		response = self.client.post('/project/delete', data=dict(
			id=1
		), follow_redirects=True)
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Eliminado proyecto "Test Project"')
		response = self.client.get('/log/')
		self.assert200(response)
	
	@login_user
	def test_log_project_search(self):
		response = self.client.get("/project/search?phrase=test")
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Busqueda de proyectos por frase "test"')
		response = self.client.get('/log/')
		self.assert200(response)
	