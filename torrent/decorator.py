from functools import wraps
from flask import session, redirect, url_for

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'userName' not in session:
            return redirect(url_for('login_view'))
        return func(*args, **kwargs)
    return decorated_function
