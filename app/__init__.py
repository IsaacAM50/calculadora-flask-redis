from flask import Flask
from redis import Redis

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    redis = Redis(host='localhost', port=6379, db=0)

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app