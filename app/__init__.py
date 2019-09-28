#!/usr/bin/env python
#coding:utf-8

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    from .nursing.views import huli
    app.register_blueprint(huli, url_prefix='/huli')

    return app


