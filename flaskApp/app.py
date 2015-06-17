#!flask/bin/python
from flask import Flask

application = app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/tradlabs/v1/health')
def health():
    return "OK"

if __name__ == '__main__':
    application.run(debug=True)
