# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Email

class LoginForm(FlaskForm):
    email = StringField(u'邮箱',validators=[DataRequired(message=u'邮箱不能为空'),Email(message=u'请输入正确的邮箱格式')])
    password = PasswordField(u'密码',validators=[DataRequired(message=u'密码不能为空')])
    remeberme = BooleanField(u'保持登陆',default=False)
    submit = SubmitField(u'登陆')
