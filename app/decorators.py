from flask import url_for, redirect, session, make_response,flash
from functools import wraps, update_wrapper
from datetime import datetime
import views

def require_login(func):
    def wrapper(*args, **kwargs):
        if not views.is_logged_in_bool():
            return views.unauthorized()
        return func(*args, **kwargs)
    wrapper.func_name = func.func_name
    return wrapper

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)
