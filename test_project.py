import unittest
from BaseTestCase import BaseTestCase, db, Project

import functools
def login_user(fun):
	@functools.wraps(fun)
	def wrapper(*args, **kwargs):
		with args[0].client.session_transaction() as sess:
			sess['user_id'] = 1
			sess['user'] = {'id': 1, 'username': 'testUser', 'admin': True}
		return fun(*args, **kwargs)
	return wrapper

class TestProject(BaseTestCase):
	@login_user
	def test_project_list(self):
		response = self.client.get('/project/')
		self.assert200(response)
		self.assertIn(b'Test Project', response.data)

	@login_user
	def test_project_list_empty(self):
		# delete all projects
		db.session.query(Project).filter(id != 0).delete()

		# show empty list
		response = self.client.get('/project/')
		self.assert200(response)
		self.assertIn(b'No hay proyectos', response.data)

	@login_user
	def test_project_create(self):
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
	def test_project_create_invalid(self):
		response = self.client.post('/project/add', data=dict(
			description='Test Project 2',
			open_date='2023-01-01',
			close_date='2013-01-01',
			enabled=True
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Open date must be before close date', response.data)
		self.assertIsNone(Project.query.filter_by(description='Test Project 2').first())

	@login_user
	def test_project_edit(self):
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
	def test_project_edit_invalid(self):
		response = self.client.post('/project/update', data=dict(
			id=1,
			description='Test Project Modified',
			open_date='2023-01-01',
			close_date='2013-01-01',
			enabled=True
		), follow_redirects=True)
		self.assert200(response)
		self.assertIn(b'Open date must be before close date', response.data)

	@login_user
	def test_project_toggle(self):
		response = self.client.post('/project/toggle', data=dict(id=1),
			follow_redirects=True
		)
		self.assert200(response)
		project = db.session.query(Project).filter_by(id=1).first()
		self.assertFalse(project.enabled)

	@login_user
	def test_project_delete(self):
		response = self.client.post('/project/delete', data=dict(id=1),
			follow_redirects=True
		)
		self.assert200(response)
		self.assertNotIn(b'Test Project', response.data)
		self.assertIsNone(Project.query.filter_by(description='Test Project').first())

	@login_user
	def test_project_delete_invalid(self):
		response = self.client.post('/project/delete', data=dict(id=0),
			follow_redirects=True
		)
		self.assert400(response)

if __name__ == '__main__':
	unittest.main()