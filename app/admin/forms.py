# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,HiddenField,BooleanField,SelectField
from wtforms.validators import DataRequired

class AddMenuForm(FlaskForm):
    menuname = StringField(u'导航名称',validators=[DataRequired(message=u'导航名称不能为空')])
    submit = SubmitField(u'确定')

class EditMenuForm(AddMenuForm):

    id = HiddenField(u'ID')
    visibled = BooleanField(u'是否隐藏')

class AddCategoryForm(FlaskForm):
    categoryname = SelectField()
