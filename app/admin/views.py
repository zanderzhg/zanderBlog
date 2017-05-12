# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''

from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from . import admin
from ..models import Menus, Category
from .. import db
from .forms import AddMenuForm, EditMenuForm, AddCategoryForm,EditCategoryForm


@admin.route('/')
@login_required
def index():
    return render_template('admin/admin_base.html')


# 访问导航页
@admin.route('/menus/')
@admin.route('/menus/<int:page>')
@login_required
def menus(page=1):
    menulst = Menus.query.order_by(Menus.orderNo).paginate(page, per_page=10)
    addmenuform = AddMenuForm()
    editmenuform = EditMenuForm()
    return render_template('admin/menus.html', menulst=menulst,
                           addmenuform=addmenuform, editmenuform=editmenuform)


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
    return redirect(url_for('admin.menus'))


# 获取导航
@admin.route('/get-menus/<int:id>')
@login_required
def menu_get_info(id=None):
    menu = Menus.query.filter_by(id=id).first_or_404()
    return jsonify(menu.to_json())


# 修改导航
@admin.route('/menus/edit/', methods=['post'])
@login_required
def menus_edit():
    form = EditMenuForm(request.form)
    menu = Menus.query.filter_by(id=form.id.data).first()
    (menu.menuName, menu.visible) = (form.menuname.data, form.visibled.data)
    db.session.add(menu)
    db.session.commit()
    flash(u'修改成功', 'success')
    return redirect(url_for('admin.menus'))


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
    return redirect(url_for('admin.menus'))


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
                           addcategoryform=addcategoryform,editcategoryform=editcategoryform)


# 获取分类
@admin.route('/get-category/<int:id>')
@login_required
def get_category_info(id=None):
    category = Category.query.filter_by(id=id).first_or_404()
    return jsonify(category.to_json())

#修改分类
@admin.route('/category/edit/',methods=['POST'])
@login_required
def category_edit():
    form = EditCategoryForm(request.form)
    category = Category.query.filter_by(id=form.id.data).first()
    (category.categoryName,category.menuid) = (form.categoryname.data,form.menuselect.data)
    db.session.add(category)
    db.session.commit()
    flash(u'修改分类成功','success')
    return redirect(url_for('admin.category_list'))


# 新增分类
@admin.route('/category/add/', methods=['POST'])
@login_required
def category_add():
    categoryform = AddCategoryForm()
    if categoryform.validate_on_submit():
        if Category.insert_category(categoryform.categoryname.data,
                                    categoryform.menuselect.data):
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
