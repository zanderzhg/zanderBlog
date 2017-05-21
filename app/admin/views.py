# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import admin
from ..models import Menus, Category, Post
from .. import db
from .forms import AddMenuForm, EditMenuForm, AddCategoryForm, EditCategoryForm, \
    PostsForm, EditPostForm
from datetime import datetime


@admin.route('/')
@login_required
def index():
    return render_template('admin/admin-base.html')


# 访问导航页
@admin.route('/menu/')
@admin.route('/menu/<int:page>')
@login_required
def menu_list(page=1):
    menulst = Menus.query.order_by(Menus.orderNo).paginate(page, per_page=10)
    addmenuform = AddMenuForm()
    return render_template('admin/menu.html', menulst=menulst,
                           addmenuform=addmenuform)


# 新增导航
@admin.route('/menus/add/', methods=['POST'])
@login_required
def menu_add():
    menuaddform = AddMenuForm()
    if menuaddform.validate_on_submit():
        if Menus.insert_menus(menuaddform.menuname.data):
            flash(u'新增导航 <{}> 成功'.format(menuaddform.menuname.data), 'success')
        else:
            flash(u'导航 <{}> 已存在'.format(menuaddform.menuname.data), 'warning')
    return redirect(url_for('admin.menu_list'))


# 获取导航
@admin.route('/get-menus/<int:id>')
@login_required
def menu_get_info(id=None):
    menu = Menus.query.filter_by(id=id).first_or_404()
    return jsonify(menu.to_json())


# 修改导航
@admin.route('/menus/edit/<int:id>', methods=['POST','GET'])
@login_required
def menu_edit(id=None):
    form = EditMenuForm()
    menu = Menus.query.filter_by(id=id).first()
    form.menuname.data = menu.menuName
    form.visibled.data = menu.visible
    if form.validate_on_submit():
        reqform = EditMenuForm(request.form)
        (menu.menuName, menu.visible) = (reqform.menuname.data, reqform.visibled.data)
        db.session.add(menu)
        db.session.commit()
        flash(u'修改成功', 'success')
        return redirect(url_for('admin.menu_list'))
    return render_template('admin/menu-add.html',form=form)


# 隐藏或显示导航菜单
@admin.route('/menus/setvisible/<int:id>/')
@login_required
def menus_setvisible(id=None):
    menu = Menus.query.filter_by(id=id).first()
    if menu.visible:
        menu.visible = False
        flash(u'显示成功', 'success')
    else:
        menu.visible = True
        flash(u'隐藏成功', 'success')
    db.session.add(menu)
    db.session.commit()
    return redirect(url_for('admin.menus'))


# 删除导航页
@admin.route('/menus/del/<int:id>')
@login_required
def menu_del(id=None):
    delmenu = Menus.query.filter_by(id=id).first()
    if delmenu is not None:
        categorys = Category.query.filter_by(menuid=id).all()
        for c in categorys:
            c.menuid = -1
            db.session.add(c)
            db.session.commit()
        db.session.delete(delmenu)
        db.session.commit()
        flash(u'删除成功', 'success')
    else:
        flash(u'删除失败', 'warning')
    return redirect(url_for('admin.menu_list'))


# 分类列表
@admin.route('/category/list/')
@admin.route('/category/list/<int:page>')
@login_required
def category_list(page=1):
    categories = Category.query.order_by(Category.orderNo).paginate(page,
                                                                    per_page=10,
                                                                    error_out=False)
    addcategoryform = AddCategoryForm()
    editcategoryform = EditCategoryForm()
    return render_template('admin/category.html', categories=categories,
                           addcategoryform=addcategoryform,
                           editcategoryform=editcategoryform)


# 获取分类
@admin.route('/get-category/<int:id>')
@login_required
def get_category_info(id=None):
    category = Category.query.filter_by(id=id).first_or_404()
    return jsonify(category.to_json())


# 修改分类
@admin.route('/category/edit/<int:id>', methods=['POST','GET'])
@login_required
def category_edit(id=None):
    form = EditCategoryForm()
    category = Category.query.filter_by(id=id).first()
    form.categoryname.data = category.categoryName
    form.menuselect.data = category.menuid
    form.visibled.data = category.visibled
    if form.validate_on_submit():
        reqform = EditCategoryForm(request.form)
        (category.categoryName, category.menuid) = (
            reqform.categoryname.data, reqform.menuselect.data)
        db.session.add(category)
        db.session.commit()
        flash(u'修改分类成功', 'success')
        return redirect(url_for('admin.category_list'))
    return render_template('admin/category-add.html',form=form)


# 新增分类
@admin.route('/category/add/', methods=['POST'])
@login_required
def category_add():
    categoryform = AddCategoryForm()
    if categoryform.validate_on_submit():
        if Category.insert_category(categoryform.categoryname.data,
                                    categoryform.menuselect.data,categoryform.visibled.data):
            flash(u'新增成功', 'success')
        else:
            flash(u'新增失败', 'warning')
    return redirect(url_for('admin.category_list'))


# 删除分类
@admin.route('/category/del/<int:id>')
@login_required
def category_del(id=None):
    delcategory = Category.query.filter_by(id=id).first()
    if delcategory is not None:
        db.session.delete(delcategory)
        db.session.commit()
        flash(u'删除成功', 'success')
    else:
        flash(u'删除失败', 'warning')
    return redirect(url_for('admin.category_list'))


# 博文列表
@admin.route('/post/list/')
@admin.route('/post/list/<int:page>/')
@login_required
def post_list(page=1):
    posts = Post.query.order_by(Post.timestamp).paginate(page, per_page=10,
                                                         error_out=False)
    return render_template('admin/post.html', posts=posts)


# 新增博文章
@admin.route('/posts/add/', methods=['POST', 'GET'])
@login_required
def post_add():
    postaddform = PostsForm()
    if postaddform.validate_on_submit():
        post = Post(title=postaddform.title.data, body=postaddform.body.data,
                    author_id=current_user.id,
                    category_id=postaddform.poststype.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('admin.post_list'))
    return render_template('admin/post-add.html', postaddform=postaddform)


# 博文JSON信息
@admin.route('/posts/get-post-info/<int:id>')
@login_required
def get_post_info(id=None):
    post = Post.query.filter_by(id=id).first_or_404()
    return jsonify(post.to_json())


# 修改文章
@admin.route('/posts/edit/<int:id>', methods=['POST', 'GET'])
@login_required
def post_edit(id=None):
    editpostform = EditPostForm()
    post = Post.query.filter_by(id=id).first()
    editpostform.id.data = post.id
    editpostform.title.data = post.title
    editpostform.body.data = post.body
    editpostform.poststype.data = post.category_id
    if editpostform.validate_on_submit():
        form = EditPostForm(request.form)
        posts = Post.query.filter_by(id=id).first_or_404()
        post.title = form.title.data
        post.body = form.body.data
        post.category_id = form.poststype.data
        post.timestamp = datetime.utcnow()
        db.session.add(posts)
        db.session.commit()
        flash(u'文章修改成功','success')
        return redirect(url_for('admin.post_list'))
    return render_template('admin/post-edit.html', editpostform=editpostform)


# 删除文章
@admin.route('/post/del/<int:id>')
@login_required
def post_del(id=None):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    flash(u'删除成功', 'success')
    return redirect(url_for('admin.post_list'))


@admin.route('/test/')
@login_required
def text():
    return str(current_user.userName)
