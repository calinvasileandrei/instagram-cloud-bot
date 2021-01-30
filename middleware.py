from werkzeug.wrappers import Request, Response, ResponseStream
import os
from dotenv import load_dotenv

class middleware():
    '''
    Simple WSGI middleware
    '''

    def __init__(self, app):
        self.app = app
        self.username = os.getenv("auth_username")
        self.password = os.getenv("auth_password")

    def __call__(self, environ, start_response):
        request = Request(environ)
        try:
            userName = request.authorization['username']
            password = request.authorization['password']
        except:
            userName = ""
            password = ""
        # these are hardcoded for demonstration
        # verify the username and password from some database or env config variable
        if userName == self.username and password == self.password:
            environ['user'] = {'name': 'Tony'}
            return self.app(environ, start_response)

        res = Response(u'Authorization failed', mimetype='text/plain', status=401)
        return res(environ, start_response)