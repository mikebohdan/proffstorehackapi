from flask_restful import Resource
from functools import wraps
from flask import redirect, url_for, request


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


class Auth(Resource):

    def get(self):
        pass
