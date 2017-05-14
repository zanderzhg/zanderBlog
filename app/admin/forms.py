# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, BooleanField, \
    SelectField
from wtforms.validators import DataRequired
from ..models import Menus, Category
from flask_pagedown.fields import PageDownField


class AddMenuForm(FlaskForm):
    menuname = StringField(u'导航名称',
                           validators=[DataRequired(message=u'导航名称不能为空')])
    submit = SubmitField(u'确定')


class EditMenuForm(AddMenuForm):
    id = HiddenField(u'ID')
    visibled = BooleanField(u'是否隐藏')


class AddCategoryForm(FlaskForm):
    categoryname = StringField(u'分类名称',
                               validators=[DataRequired(message=u'分类名称不能为空')])
    menuselect = SelectField(u'所属菜单', coerce=int)
    submit = SubmitField(u'确定')

    #  这段是在网上看到的,
    # super还不理解,要好好学学
    def __init__(self, *args, **kwargs):
        super(AddCategoryForm, self).__init__(*args, **kwargs)
        self.menuselect.choices = [(menu.id, menu.menuName) for menu in
                                   Menus.query.all()]
        self.menuselect.choices.insert(0, (-1, '未分类'))


class EditCategoryForm(AddCategoryForm):
    id = HiddenField(u'ID')
    pass


class PostsForm(FlaskForm):
    title = StringField(u'博客标题', validators=[DataRequired()])
    poststype = SelectField(u'所属分类', coerce=int)
    body = PageDownField(u'博客正文', validators=[DataRequired()])
    submit = SubmitField(u'提交')

    def __init__(self, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        self.poststype.choices = [(c.id, c.categoryName) for c in
                                  Category.query.all()]
        self.poststype.choices.insert(0, (-1, '未分类'))


class EditPostForm(PostsForm):
    id = HiddenField(u'ID')
    pass
