# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
