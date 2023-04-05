from user.model import User
from sqlalchemy import text

USER_LOGIN_DATA = {
	'id': 1,
	'username': 'testUser',
	'password': 'test',
	'admin': True
}

TEST_USER_DATA = {
	'valid': {
		'test1': User(USER_LOGIN_DATA['username'], USER_LOGIN_DATA['password'], 'testName', 'testLastName', 1, 1, 1),
		'test2': User('testUser2', 'test', 'testName2', 'testLastName2', 1, 1, 1),
	},
	'invalidPassword': {
		"username": "testUser",
		"password": "invalid_password"
	},
	'invalidUsername': {
		"username": "invalid_username",
		"password": "test"
	},
	'register': {
		"username": "testUser3",
		"password": "test",
		"name": "testName3",
		"lastname": "testLastname3",
		"role": "admin",
		"department": "Test Department",
		"project": "Test Project"
	},
	'delete': {
		"id": 2,
		"username": "testUser2",
	},
}

def init_database(self, db):
	self.test_user_data = TEST_USER_DATA

	# Fill database with initial data
	with self.app.app_context():
		db.drop_all()
		db.create_all()
		db.session.commit()

		# Fill with initial data
		with open('tests/helpers/test_database.sql', 'r') as f:
			for line in f:
				if line and not line.startswith('--'):
					db.session.execute(text(line))

		# Fill with users
		for user in self.test_user_data['valid'].values():
			db.session.add(user)
		db.session.commit()