"""
注册、登录及个人中心
"""

from functools import wraps
from flask import request, render_template, redirect, url_for, flash, session, Blueprint, Response
from sqlalchemy import and_, or_
from Patient.app.models import db, User
from ..utils.qrcode import Code


index_blueprint = Blueprint('index', __name__)
graph_code = ''  # 全局变量验证码

############################################
# 辅助函数、装饰器
############################################


# 登录检验（用户名、密码验证）
def valid_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False


# 注册检验（用户名、邮箱验证）
def valid_regist(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user:
        return False
    else:
        return True


# 登录
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('username'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index.login', next=request.url))

    return wrapper


############################################
# 路由
############################################

# 1.主页
@index_blueprint.route('/')
def home():
    return render_template('home.html', username=session.get('username'))


# 2.登录
@index_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    global graph_code
    print('lo:', graph_code)
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']) and request.form['qrcode'].lower() == graph_code.lower():
            flash("成功登录！")
            session['username'] = request.form.get('username')
            return redirect(url_for('index.home'))
        else:
            error = '错误的用户名或密码！'

    return render_template('login.html', error=error)


# 3.注销
@index_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index.home'))


# 4.注册
@index_blueprint.route('/regist', methods=['GET', 'POST'])
def regist():
    error = None
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            error = '两次密码不相同！'
        elif valid_regist(request.form['username'], request.form['email']):
            user = User(username=request.form['username'], password=request.form['password1'],
                        email=request.form['email'])
            db.session.add(user)
            db.session.commit()

            flash("成功注册！")
            return redirect(url_for('index.login'))
        else:
            error = '该用户名或邮箱已被注册！'

    return render_template('regist.html', error=error)


# 5.个人中心
@index_blueprint.route('/panel')
@login_required
def panel():
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    return render_template("panel.html", user=user)


# 6.验证码生成
@index_blueprint.route('/codes/')
def code():
    infor = Code().creat_code()
    image_file = infor["image_file"]
    global graph_code
    graph_code = infor['code']
    # print(graph_code)
    image_content = image_file.getvalue()
    image_file.close()
    return Response(image_content, mimetype='jpeg')
