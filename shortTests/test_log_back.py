import unittest
from BaseTestCase import BaseTestCase, db
from user.model import User
from log.model import Log

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
	def test_log_user_search(self):
		response = self.client.get("/user/search?phrase=testUser")
		self.assert200(response)

		# check logs
		log = db.session.query(Log).order_by(Log.id.desc()).first()
		self.assertEqual(log.description, 'Busqueda de usuarios por frase "testUser"')
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


if __name__ == '__main__':
	unittest.main()