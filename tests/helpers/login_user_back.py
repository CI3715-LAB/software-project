import functools
def login_user(fun):
	@functools.wraps(fun)
	def wrapper(*args, **kwargs):
		with args[0].client.session_transaction() as sess:
			sess['user_id'] = 1
			sess['user'] = {'id': 1, 'username': 'testUser', 'admin': True}
		return fun(*args, **kwargs)
	return wrapper