# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    SECRET_KEY = 'THIS IS A GUESS STRING'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = r'sqlite:///' + os.path.join(basedir, r'data\data.db')


config = {
    'Development' : Development
}
