# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from app import create_app, db
from app.models import *

app = create_app('Development')

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User,Menus=Menus,Category=Category)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(use_debugger=True, host='0.0.0.0'))

if __name__ == '__main__':
    manager.run()