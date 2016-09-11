from functools import wraps
from flask import session, make_response, jsonify

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'userId' not in session or not session['userId']:
            return make_response(jsonify({'code': '401', 'message': 'unauthorized'}), 401)
        return func(*args, **kwargs)
    return decorated_function
