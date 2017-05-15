# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask import render_template, url_for, request, flash
from . import main
from .. import db
from ..models import *


# 前台首页
@main.route('/')
@main.route('/<int:page>/')
def index(page=1):
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=10,
                                                              error_out=False)
    return render_template('main/index.html', posts=posts)


# 前台文章页面
@main.route('/category/<int:menuID>/')
def category(menuID=None):
    categorys = db.session.query(Post.posttype.categoryName,
                                 db.func.count(Post.id)).group_by(
        Post.category_id).all()
    return render_template('main/category.html', categorys=categorys)
