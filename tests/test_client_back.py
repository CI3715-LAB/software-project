import unittest
from BaseTestCase import BaseTestCase, db

from helpers.login_user_back import login_user

class TestClient(BaseTestCase):
	@login_user
	def test_client_list(self):
		response = self.client.get('/client/')
		self.assert200(response)

	@login_user
	def test_client_add(self):
		response = self.client.get('/client/', follow_redirects=True)
		self.assert200(response)

	@login_user
	def test_client_update(self):
		response = self.client.get('/client/', follow_redirects=True)
		self.assert200(response)


if __name__ == "__main__":
	unittest.main()