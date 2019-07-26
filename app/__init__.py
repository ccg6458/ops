from flask import Flask
from flask_restful import Api
from app.config.settings_dev import DevConfig

from app.lib.extensions import db



def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig)
    register_extensions(app)

    return app

def register_extensions(app):
    db.init_app(app)
    return app

def register_url(app):
    api=Api(app)
    api.add_resource()

    return app