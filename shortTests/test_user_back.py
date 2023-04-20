import unittest
from flask import url_for
from BaseTestCase import BaseTestCase, db
from user.model import User, Role

from helpers.login_user_back import login_user

class TestUser(BaseTestCase):
	def test_redirect_to_login(self):
		response = self.client.get('/user/', follow_redirects=True)
		# assert redirected to login page
		self.assertEqual(response.request.path, url_for('user.user_login'))


	def test_user_login_invalid_password(self):
		response = self.client.post('/user/login', data=dict(
				id=1,
				username='admin',
				password='wrongPassword',
			), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Las credenciales suministradas no son validas', response.data)

	def test_user_login_invalid_username(self):	
		response = self.client.post('/user/login', data=dict(
				id=1,
				username='adminNotExists',
				password='test',
			), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El nombre de usuario suministrado no existe', response.data)

	@login_user
	def test_logout(self):
		response = self.client.get('/user/logout', follow_redirects=True)
		with self.client.session_transaction() as sess:
			self.assert200(response)
			self.assertNotIn('user_id', sess)

	@login_user
	def test_user_list(self):
		response = self.client.get('/user/', follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'admin', response.data)

	@login_user
	def test_user_list_empty(self):
		# delete all users
		db.session.query(User).delete()

		# show empty list
		response = self.client.get('/user/')
		self.assert200(response)
		self.assertIn(b'No hay usuarios', response.data)

	@login_user
	def test_user_register(self):
		response = self.client.post('/user/register', data=dict(
			username='admin2',
			password='test2',
			name='testName2',
			lastname='testLastName2',
			role='admin',
			project='Proyecto 1',
			department='Undefined',
		), follow_redirects=True)
		self.assert200(response)
		
		with self.client.session_transaction() as sess:
			print("USUARIOS REGISTRADOS||||",db.session.query(User).filter_by(username='admin2').all())
			print(response.data)
			self.assertIsNotNone(db.session.query(User).filter_by(username='admin2').first())

	@login_user
	def test_user_register_invalid_username(self):
		response = self.client.post('/user/register', data=dict(
			username='admin',
			name='testName',
			password='test',
			lastname='testLastName',
			role='admin',
			project='Proyecto 1',
			department='Undefined',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Este nombre se usuario ya se encuentra registrado', response.data)

	@login_user
	def test_user_register_invalid_project(self):
		response = self.client.post('/user/register', data=dict(
			username='admin2',
			name='testName',
			password='test',
			lastname='testLastName',
			role='admin',
			project='Wrong',
			department='Undefined',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El proyecto suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_register_invalid_role(self):
		response = self.client.post('/user/register', data=dict(
			username='admin2',
			name='testName',
			password='test',
			lastname='testLastName',
			role='Wrong Role',
			project='Proyecto 1',
			department='Undefined',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El rol suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_register_invalid_department(self):
		response = self.client.post('/user/register', data=dict(
			username='admin2',
			name='testName',
			password='test',
			lastname='testLastName',
			role='admin',
			project='Proyecto 1',
			department='Wrong Department',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El departamento suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_update(self):
		# create new role
		db.session.add(Role('testRole'))
		db.session.commit()
		response = self.client.post('/user/update', data=dict(
			id=1,
			username='admin',
			name='testName',
			lastname='testLastName',
			role='testRole',
			project='Proyecto 1',
			department='Undefined',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'testRole', response.data)

	@login_user
	def test_user_update_invalid_role(self):
		response = self.client.post('/user/update', data=dict(
			id=1,
			username='admin',
			name='testName',
			lastname='testLastName',
			role='Wrong',
			project='Proyecto 1',
			department='Undefined',
		), follow_redirects=True)
		self.assert400(response)
		self.assertIn(b'El rol suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_update_invalid_project(self):
		response = self.client.post('/user/update', data=dict(
			id=1,
			username='admin',
			name='testName',
			lastname='testLastName',
			role='admin',
			project='Wrong',
			department='Undefined',
		), follow_redirects=True)
		self.assert400(response)
		self.assertIn(b'El proyecto suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_update_invalid_username(self):
		response = self.client.post('/user/update', data=dict(
			id=123,
			username='adminNonExistent',
			name='testName',
			lastname='testLastName',
			role='admin',
			project='Proyecto 1',
			department='Undefined',
		), follow_redirects=True)
		self.assert400(response)
		self.assertIn(b'El usuario suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_update_invalid_department(self):
		response = self.client.post('/user/update', data=dict(
			id=1,
			username='admin',
			name='testName',
			lastname='testLastName',
			role='admin',
			project='Proyecto 1',
			department='Wrong Department',
		), follow_redirects=True)
		self.assert400(response)
		self.assertIn(b'El departamento suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_delete(self):
		user = db.session.query(User).order_by(User.id.desc()).first()
		response = self.client.post('/user/delete', data=dict(
			id=user.id,
		), follow_redirects=True)
		self.assert200(response)
		self.assertNotIn(bytes(user.username, 'utf-8'), response.data)

	@login_user
	def test_user_search(self):
		response = self.client.get('/user/search?phrase=admin')
		self.assert200(response)
		self.assertIn(b'admin', response.data)

	@login_user
	def test_user_reset(self):
		response = self.client.post('/user/reset', data=dict(
			username='admin',
			password_prev='admin',
			password_next='testModified',
		), follow_redirects=True)
		self.assert200(response)
		user = User.query.filter_by(username='admin').first()
		self.assertTrue(user.check_password('testModified'))

	@login_user
	def test_user_reset_invalid(self):
		response = self.client.post('/user/reset', data=dict(
			username='admin',
			password_prev='wrongPassword',
			password_next='test2',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Las credenciales suministradas no son validas', response.data)

		response = self.client.post('/user/reset', data=dict(
			username='adminNonExistent',
			password_prev='test',
			password_next='test2',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El nombre de usuario suministrado no existe', response.data)

if __name__ == '__main__':
	unittest.main()