from functools import wraps
from flask import request, Response
import logging

log = logging.getLogger('simple_example')

password = None
gm_password = None

def check_auth(try_password):
    """This function is called to check if a password is valid.
    """
    return try_password == password or try_password == gm_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

