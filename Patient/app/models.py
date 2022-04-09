
from . import db


# 定义用户类
class User(db.Model):
    """
    患者账户表
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


# 定义医生类
class Doctor(db.Model):
    """
    医生账户表
    """
    __tablename__ = "doctor"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<Doctor %r>' % self.username
