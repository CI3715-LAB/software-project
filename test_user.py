import unittest
from flask import session
from BaseTestCase import BaseTestCase, db, User
from user.model import Role

from werkzeug.security import generate_password_hash

import functools
def login_user(fun):
	@functools.wraps(fun)
	def wrapper(*args, **kwargs):
		with args[0].client.session_transaction() as sess:
			sess['user_id'] = 1
			sess['user'] = {'id': 1, 'username': 'testUser', 'admin': True}
		return fun(*args, **kwargs)
	return wrapper

class TestUser(BaseTestCase):
	# def test_user_login(self):
	# 	response = self.client.post('/user/login', data=dict(
	# 			id=1,
	# 			username='testUser',
	# 			password='test',
	# 		), follow_redirects=True)
	# 	with self.client.session_transaction() as sess:
	# 		self.assert200(response)
	# 		self.assertIn('user_id', sess)

	def test_redirect_to_login(self):
		response = self.client.get('/user/')
		# assert redirected to login page
		self.assertRedirects(response, '/user/login')


	def test_user_login_invalid(self):
		response = self.client.post('/user/login', data=dict(
				id=1,
				username='testUser',
				password='wrongPassword',
			), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Las credenciales suministradas no son validas', response.data)
		
		response = self.client.post('/user/login', data=dict(
				id=1,
				username='testUserNotExists',
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
		self.assertIn(b'testUser', response.data)

	@login_user
	def test_user_list_empty(self):
		# delete all users
		db.session.query(User).delete()
		# db.session.commit()

		# show empty list
		response = self.client.get('/user/')
		self.assert200(response)
		self.assertIn(b'No hay usuarios', response.data)
		# self.assertIsNone(User.query.first())

	@login_user
	def test_user_register(self):
		response = self.client.post('/user/register', data=dict(
			username='testUser2',
			password='test2',
			name='testName2',
			lastname='testLastName2',
			role='admin',
			project='Test Project',
		), follow_redirects=True)
		self.assert200(response)
		# self.assertIn(b'testUser2', response.data)
		self.assertIsNotNone(User.query.filter_by(username='testUser2').first())

	@login_user
	def test_user_register_invalid(self):
		response = self.client.post('/user/register', data=dict(
			username='testUser',
			name='testName',
			password='test',
			lastname='testLastName',
			role='admin',
			project='Test Project',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Este nombre se usuario ya se encuentra registrado', response.data)

		response = self.client.post('/user/register', data=dict(
			username='testUser2',
			name='testName',
			password='test',
			lastname='testLastName',
			role='admin',
			project='Wrong',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El proyecto suministrado no existe en la base de datos', response.data)

		response = self.client.post('/user/register', data=dict(
			username='testUser2',
			name='testName',
			password='test',
			lastname='testLastName',
			role='Wrong Role',
			project='Test Project',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El rol suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_update(self):
		# create new role
		db.session.add(Role('testRole'))
		db.session.commit()
		response = self.client.post('/user/update', data=dict(
			id=1,
			username='testUser',
			name='testName',
			lastname='testLastName',
			role='testRole',
			project='Test Project',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'testRole', response.data)

	@login_user
	def test_user_update_invalid(self):
		response = self.client.post('/user/update', data=dict(
			id=1,
			username='testUser',
			name='testName',
			lastname='testLastName',
			role='Wrong',
			project='Test Project',
		), follow_redirects=True)
		self.assert400(response)
		self.assertIn(b'El rol suministrado no existe en la base de datos', response.data)

		response = self.client.post('/user/update', data=dict(
			id=1,
			username='testUser',
			name='testName',
			lastname='testLastName',
			role='admin',
			project='Wrong',
		), follow_redirects=True)
		self.assert400(response)
		self.assertIn(b'El proyecto suministrado no existe en la base de datos', response.data)

		response = self.client.post('/user/update', data=dict(
			id=2,
			username='testUserNonExistent',
			name='testName',
			lastname='testLastName',
			role='admin',
			project='Test Project',
		), follow_redirects=True)
		self.assert400(response)
		self.assertIn(b'El usuario suministrado no existe en la base de datos', response.data)

	@login_user
	def test_user_delete(self):
		response = self.client.post('/user/delete', data=dict(
			id=1
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'No hay usuarios', response.data)

	@login_user
	def test_user_search(self):
		response = self.client.get('/user/search?phrase=testUser')
		self.assert200(response)
		self.assertIn(b'testUser', response.data)

	# @login_user
	# def test_user_reset(self):
	# 	response = self.client.post('/user/reset', data=dict(
	# 		username='testUser',
	# 		password_prev='test',
	# 		password_next='test2',
	# 	), follow_redirects=True)
	# 	self.assert200(response)
	# 	self.assertEqual(User.query.get(1).password, generate_password_hash('test2'))

	@login_user
	def test_user_reset_invalid(self):
		response = self.client.post('/user/reset', data=dict(
			username='testUser',
			password_prev='wrongPassword',
			password_next='test2',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Las credenciales suministradas no son validas', response.data)

		response = self.client.post('/user/reset', data=dict(
			username='testUserNonExistent',
			password_prev='test',
			password_next='test2',
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El nombre de usuario suministrado no existe', response.data)

if __name__ == '__main__':
	unittest.main()