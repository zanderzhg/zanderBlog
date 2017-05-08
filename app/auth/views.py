# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask import render_template,redirect,url_for,request,flash
from . import auth
from .forms import LoginForm
from ..models import User
from flask_login import login_user,logout_user,login_required

@auth.route('/login/',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remeberme.data)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash(u'用户名或密码错误')
    return render_template('auth/login.html',loginform=form)

@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    flash(u'你已经退出登录')
    return redirect(url_for('auth.login'))