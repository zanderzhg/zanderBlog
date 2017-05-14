# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask import render_template,url_for,request,flash
from . import main

@main.route('/')
def index():
    return render_template('main/index.html')
