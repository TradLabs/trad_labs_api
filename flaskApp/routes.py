#!flask/bin/python
from flaskApp import application

@application.route('/')
def index():
    return "Hello, World!"

@application.route('/tradlabs/v1/health')
def health():
    return "OK"


