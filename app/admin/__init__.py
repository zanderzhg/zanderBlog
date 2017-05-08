# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask import Blueprint

admin = Blueprint('admin',__name__)

from . import views