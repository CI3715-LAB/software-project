import unittest
from BaseTestCase import BaseTestCase, db

from helpers.login_user_back import login_user

class TestDepartment(BaseTestCase):
	@login_user
	def test_department_list(self):
		response = self.client.get('/department/')
		self.assert200(response)
	
	@login_user
	def test_department_list(self):
		response = self.client.get('/department/')
		self.assert200(response)

	@login_user
	def test_department_add(self):
		response = self.client.get('/department/', follow_redirects=True)
		self.assert200(response)

	@login_user
	def test_department_update(self):
		response = self.client.get('/department/', follow_redirects=True)
		self.assert200(response)

if __name__ == "__main__":
	unittest.main()