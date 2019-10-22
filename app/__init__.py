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

    from .main.views import main
    app.register_blueprint(main, url_prefix='/huli/')

    from .nurse.views import nurse
    app.register_blueprint(nurse, url_prefix='/huli/nurse')

    from .transfer.views import transfer
    app.register_blueprint(transfer, url_prefix='/huli/transfer')

    from .leave.views import leave
    app.register_blueprint(leave, url_prefix='/huli/leave')

    return app


