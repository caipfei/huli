#!/usr/bin/env python
#coding:utf-8

from app import create_app, db
from app.models import *
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User, Nurse=Nurse, Dept=Dept, Transfer=Transfer, Leave=Leave, Train=Train)
manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()
