# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask import Blueprint

main = Blueprint('main',__name__)

from . import views
