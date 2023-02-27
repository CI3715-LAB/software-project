import unittest
from BaseTestCase import BaseTestCase, db, User
from user.model import Role

class TestUserEdnpoints(BaseTestCase):
	def test_user_list(self):
		response = self.client.get('/user/', follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'testUser', response.data)

	def test_user_list_empty(self):
		# delete all users
		db.session.query(User).delete()
		# db.session.commit()

		# show empty list
		response = self.client.get('/user/')
		self.assert200(response)
		self.assertIn(b'No hay usuarios', response.data)
		# self.assertIsNone(User.query.first())

	def test_user_register(self):
		response = self.client.post('/user/register', data=dict(
			username='testUser2',
			name='testName2',
			lastname='testLastName2',
			role=1,
			project=1,
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'testUser2', response.data)
		self.assertIsNotNone(User.query.filter_by(username='testUser2').first())

	def test_user_register_invalid(self):
		response = self.client.post('/user/register', data=dict(
			username='testUser',
			name='testName',
			lastname='testLastName',
			role=1,
			project=1,
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Este nombre se usuario ya se encuentra registrado', response.data)

		response = self.client.post('/user/add', data=dict(
			username='testUser2',
			name='testName',
			lastname='testLastName',
			role=1,
			project=2,
		), follow_redirects=True)
		self.assert200(response)
		self.asserIn(b'El proyecto suministrado no existe en la base de datos', response.data)

		response = self.client.post('/user/add', data=dict(
			username='testUser2',
			name='testName',
			lastname='testLastName',
			role=2,
			project=1,
		), follow_redirects=True)
		self.assert200(response)
		self.asserIn(b'El rol suministrado no existe en la base de datos', response.data)

	def test_user_update(self):
		# create new role
		db.session.add(Role('testRole'))
		db.session.commit()
		response = self.client.post('/user/update', data=dict(
			id=1,
			username='testUser',
			name='testName',
			lastname='testLastName',
			role=2,
			project=1,
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'testRole', response.data)

	def test_user_update_invalid(self):
		response = self.client.post('/user/update', data=dict(
			id=1,
			username='testUser',
			name='testName',
			lastname='testLastName',
			role=2,
			project=1,
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El rol suministrado no existe en la base de datos', response.data)

		response = self.client.post('/user/update', data=dict(
			id=1,
			username='testUser',
			name='testName',
			lastname='testLastName',
			role=1,
			project=2,
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El proyecto suministrado no existe en la base de datos', response.data)

		response = self.client.post('/user/update', data=dict(
			id=2,
			username='testUserModified',
			name='testName',
			lastname='testLastName',
			role=1,
			project=1,
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'El usuario suministrado no existe en la base de datos', response.data)

	def test_user_delete(self):
		# add new user
		# db.session.add(User('testUser3', 'testName3', 'testLastName3', 1, 1))
		# db.session.commit()

		response = self.client.post('/user/delete', data=dict(
			id=1
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'No hay usuarios', response.data)

	def test_user_search(self):
		response = self.client.get('/user/search?phrase=testUser')
		self.assert200(response)
		self.assertIn(b'testUser', response.data)

if __name__ == '__main__':
	unittest.main()