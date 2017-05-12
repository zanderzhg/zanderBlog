# -*- coding:utf-8 -*-
# Zander学Python
'''
QQ:867662267
'''
from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


# 导航表
class Menus(db.Model):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    menucategory = db.relationship('Category', backref='menus', lazy='dynamic')
    menuName = db.Column(db.String(24), unique=True, index=True, nullable=False)
    orderNo = db.Column(db.Integer)
    visible = db.Column(db.Boolean, default=False)

    def to_json(self):
        json_menu = {
            'id': self.id,
            'menuname': self.menuName,
            'visibled': self.visible
        }
        return json_menu

    # 上移导航位置
    @staticmethod
    def up_menus(menu_id):
        upmenu = Menus.query.filter_by(menu_id).first()
        if upmenu is not None:
            pass

        # 插入测试数据

    @staticmethod
    def insert_test_menus():
        menuslst = [
            '学习',
            '生活',
            '随笔'
        ]
        for title in menuslst:
            menu = Menus(menuName=title)
            db.session.add(menu)
            db.session.commit()
            menu.orderNo = menu.id
            db.session.add(menu)
            db.session.commit()

        # 新增导航菜单

    @staticmethod
    def insert_menus(menuname):
        tempmenu = Menus.query.filter_by(menuName=menuname).first()
        if tempmenu is not None:
            return False
        else:
            menu = Menus(menuName=menuname)
            db.session.add(menu)
            db.session.commit()
            menu.orderNo = menu.id
            db.session.add(menu)
            db.session.commit()
            return True


# 分类表
class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    menuid = db.Column(db.Integer, db.ForeignKey('menus.id'))
    categoryName = db.Column(db.String(32), unique=True, index=True)
    orderNo = db.Column(db.Integer)
    visibled = db.Column(db.Boolean, default=False)

    def to_json(self):
        json_category = {
            "id": self.id,
            "categoryname": self.categoryName,
            "menuid": self.menuid
        }
        return json_category

    # 新增分类
    @staticmethod
    def insert_category(categoryname, id=None):
        tempcategory = Category.query.filter_by(
            categoryName=categoryname).first()
        if tempcategory is not None:
            return False
        else:
            category = Category(categoryName=categoryname, menuid=id)
            db.session.add(category)
            db.session.commit()
            category.orderNo = category.id
            db.session.add(category)
            db.session.commit()
            return True


# 用户表
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(32))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError(u'该属性只读')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 插入用户数据
    @staticmethod
    def insert_user():
        user = User(userName='admin', email='admin@admin.com', password='admin')
        db.session.add(user)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
