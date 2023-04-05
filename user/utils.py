import functools
from flask import redirect, session, url_for

from .model import Role

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'user_id' in session:
            return redirect(url_for('user.user_login'))

        return view(**kwargs)

    return wrapped_view

def check_permission(role_name, module, permission):
    role = Role.query.filter_by(name = role_name).first()
    role_permissions = role.permissions

    for p in role_permissions:
        if p.module.name == module and p.type == permission: return True

    return False