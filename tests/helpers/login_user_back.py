from .init_database import USER_LOGIN_DATA
import functools
def login_user(fun):
	@functools.wraps(fun)
	def wrapper(*args, **kwargs):
		with args[0].client.session_transaction() as sess:
			sess['user_id'] = USER_LOGIN_DATA['id']
			sess['user'] = USER_LOGIN_DATA
		return fun(*args, **kwargs)
	return wrapper