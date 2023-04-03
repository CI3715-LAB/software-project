import unittest
from BaseTestCase import BaseTestCase, db, Project

from helpers.login_user_back import login_user

class TestClient(BaseTestCase):
	@login_user
	def test_client_list(self):
		response = self.client.get('/client/')
		self.assert200(response)

	@login_user
	def test_client_create(self):
		response = self.client.post('/project/add', data=dict(
			description='Test Project 2',
			open_date='2023-01-01',
			close_date='2023-01-01',
			enabled=True
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Test Project 2', response.data)
		self.assertIsNotNone(Project.query.filter_by(description='Test Project 2').first())

	@login_user
	def test_client_edit(self):
		response = self.client.post('/project/update', data=dict(
			id=1,
			description='Test Project Modified',
			open_date='2023-01-01',
			close_date='2023-01-01',
			enabled=True
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Test Project Modified', response.data)

	@login_user
	def test_client_delete(self):
		response = self.client.post('/project/delete', data=dict(id=1),
			follow_redirects=True
		)
		self.assert200(response)
		self.assertNotIn(b'Test Project', response.data)
		self.assertIsNone(Project.query.filter_by(description='Test Project').first())
