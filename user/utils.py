import functools
from flask import redirect, session, url_for

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'user_id' in session:
            return redirect(url_for('user.user_login'))

        return view(**kwargs)

    return wrapped_view