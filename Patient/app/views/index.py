"""
主要功能
"""

from functools import wraps
from flask import request, render_template, redirect, url_for, flash, session, Blueprint, Response
from sqlalchemy import and_, or_
from Patient.app.models import db, User, PatientInfo, DoctorInfo, HealthRecords, HomeVisit, Order, HealthEvaluation
from ..utils.qrcode import Code
from datetime import datetime


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
def valid_regist(username, patientName, phoneNum):
    user = User.query.filter(or_(User.username == username, User.patientName == patientName, User.phoneNum == phoneNum)).first()
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
    return render_template('index.html', username=session.get('username'))


# 2.登录
@index_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    global graph_code
    # print('lo:', graph_code)
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']) and request.form['qrcode'].lower() == graph_code.lower():
            flash("成功登录！")
            session['username'] = request.form.get('username')
            return redirect(url_for('page.page'))
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
        elif valid_regist(request.form['username'], request.form['patientName'], request.form['phoneNum']):
            user = User(username=request.form['username'], password=request.form['password1'],
                        patientName=request.form['patientName'], phoneNum=request.form['phoneNum'])
            db.session.add(user)
            db.session.commit()

            flash("成功注册！")
            return redirect(url_for('index.login'))
        else:
            error = '该用户名或邮箱已被注册！'

    return render_template('regist.html', error=error)


# ************************************************************************
# 5.个人中心
# ************************************************************************

@index_blueprint.route('/page')
@login_required
def panel():
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    # patientInfo = PatientInfo.query.filter(PatientInfo.username == username).first()
    # 预约记录
    allOrder = Order.query.filter(Order.patientName == user.patientName).all()
    completedOrder = 0
    outstandingOrder = 0
    for i in allOrder:
        if i.status == "已完成":
            completedOrder += 1
        if i.status == "待完成":
            outstandingOrder += 1

    return render_template("page.html", patientInfo=user, completedOrder=completedOrder, outstandingOrder=outstandingOrder)


@index_blueprint.route('/healthRecord')
@login_required
def healthRecord():
    # 个人中心信息
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    # patientInfo = PatientInfo.query.filter(PatientInfo.username == username).first()
    # 健康档案信息
    healthRecord = HealthRecords.query.filter(HealthRecords.username == username).first()
    if healthRecord is not None:
        healthRecord = {'patientName': healthRecord.patientName, 'patientSex': healthRecord.patientSex,
                        'patientBirth': healthRecord.patientBirth, 'nativePlace': healthRecord.nativePlace,
                        'patientNation': healthRecord.patientNation, 'patientHeight': healthRecord.patientHeight,
                        'patientWeight': healthRecord.patientWeight, 'patientProfession': healthRecord.patientProfession,
                        'maritalStatus': healthRecord.maritalStatus, 'degreeEducation': healthRecord.degreeEducation,
                        'phoneNum': healthRecord.phoneNum, 'idNum': healthRecord.idNum,
                        'contactAddress': healthRecord.contactAddress, 'bloodType': healthRecord.bloodType,
                        'bloodPressure': healthRecord.bloodPressure, 'patientVaccination': healthRecord.patientVaccination,
                        'historyDrugAllergy': healthRecord.historyDrugAllergy, 'historyDisease': healthRecord.historyDisease,
                        'historyFamily': healthRecord.historyFamily, 'historyOccupation': healthRecord.historyOccupation,
                        'lifeStyle': healthRecord.lifeStyle, 'recordNum': healthRecord.recordNum,
                        'updateDate': healthRecord.updateDate}


    return render_template("healthRecord.html", patientInfo=user, healthRecord=healthRecord)


@index_blueprint.route('/homeVisit')
@login_required
def homeVisit():
    # 个人中心信息
    username = session.get('username')
    user = User.query.filter(User.username == username).first()
    # patientInfo = PatientInfo.query.filter(PatientInfo.username == username).first()
    # 家访信息
    homeVist = HomeVisit.query.filter(HomeVisit.patientName == user.patientName).first()
    if homeVist is not None:
        homeVist = {'patientName': homeVist.patientName, 'visitWay': homeVist.visitWay, 'visitDate': homeVist.visitDate,
                    'disease': homeVist.disease, 'bloodPressure': homeVist.bloodPressure, 'bloodSugar': homeVist.bloodSugar,
                    'saltUptake': homeVist.saltUptake, 'sport': homeVist.sport, 'psychological': homeVist.psychological,
                    'followDoctor': homeVist.followDoctor, 'doctorGuidance': homeVist.doctorGuidance,
                    'doctorName': homeVist.doctorName, 'doctorNum': homeVist.doctorNum}

    return render_template("homeVisit.html", patientInfo=user, homeVist=homeVist)


@index_blueprint.route('/myDoctorInfo')
@login_required
def myDoctorInfo():
    doctorInfo = None
    username = session.get('username')

    # 个人中心信息
    user = User.query.filter(User.username == username).first()
    # if PatientInfo.query.filter(PatientInfo.username == username).first() is not None:
    patientInfo = PatientInfo.query.filter(PatientInfo.username == username).first()
    if patientInfo is not None:
        if patientInfo.status == "已签约":
            # 我的医生信息
            doctorNum = patientInfo.doctorNum
            doctor_info = DoctorInfo.query.filter(DoctorInfo.doctorNum == doctorNum).first()
            doctorInfo = {"doctorName": doctor_info.doctorName, "doctorNum": doctor_info.doctorNum,
                          "phoneNum": doctor_info.phoneNum, "hospitalName": doctor_info.hospitalName,
                          "department": doctor_info.department, "specialty": doctor_info.specialty}

    return render_template("myDoctorInfo.html", patientInfo=user, doctorInfo=doctorInfo)


@index_blueprint.route('/doctorDatabase', methods=['post', 'get'])
@login_required
def doctorDatabase():
    username = session.get('username')
    # 个人中心信息
    user = User.query.filter(User.username == username).first()
    # patientInfo = PatientInfo.query.filter(PatientInfo.username == username).first()

    # 医生数据库
    form_get_doctorName = str(request.form.get('doctorName'))
    form_get_doctorNum = str(request.form.get('doctorNum'))
    form_get_hospitalName = str(request.form.get('hospitalName'))
    form_get_department = str(request.form.get('department'))
    form_get_specialty = str(request.form.get('specialty'))

    filterList = []
    tag = 0
    if form_get_doctorName != '':
        filterList.append(DoctorInfo.doctorName.like('%' + form_get_doctorName + '%'))
        tag += 1
    if form_get_doctorNum != '':
        filterList.append(DoctorInfo.doctorNum == form_get_doctorNum)
        tag += 1
    if form_get_hospitalName != '':
        filterList.append(DoctorInfo.hospitalName.like('%' + form_get_hospitalName + '%'))
        tag += 1
    if form_get_department != '':
        filterList.append(DoctorInfo.department.like('%' + form_get_department + '%'))
        tag += 1
    if form_get_specialty != '':
        filterList.append(DoctorInfo.specialty.like('%' + form_get_specialty + '%'))
        tag += 1

    th_tag = 0
    if tag != 0:
        search_result = DoctorInfo.query.filter(*filterList)
        if search_result.count() != 0:
            th_tag = 1
    else:
        search_result = []
    searchResult = {'data': search_result, 'tag': th_tag}

    return render_template("doctorDatabase.html", patientInfo=user, searchResult=searchResult)


@index_blueprint.route('/signDoctor', methods=['post', 'get'])
@login_required
def signDoctor():
    username = session.get('username')
    # 个人中心信息
    user = User.query.filter(User.username == username).first()
    # patientInfo = PatientInfo.query.filter(PatientInfo.username == username).first()
    # 签约申请
    if request.method == "POST":
        get_json = request.get_json()
        # temp = HealthRecords.query.filter(HealthRecords.username == username).first()
        patientName = get_json["patient_name"]
        doctorNum = get_json["doctor_num"]
        phoneNum = user.phoneNum
        patient_info = PatientInfo(patientName=patientName, phoneNum=phoneNum, doctorNum=doctorNum, username=username, status="待签约")
        db.session.add(patient_info)
        db.session.commit()
        print("申请请求成功。。")

    return None


@index_blueprint.route('/myOrder', methods=['post', 'get'])
@login_required
def myOrder():
    username = session.get('username')
    # 个人中心信息
    user = User.query.filter(User.username == username).first()
    # patientInfo = PatientInfo.query.filter(PatientInfo.username == username).first()

    # 预约记录
    allOrder = Order.query.filter(Order.patientName == user.patientName).all()
    completedOrder = []
    outstandingOrder = []
    for i in allOrder:
        if i.status == "已完成":
            temp = {"orderType": i.orderType, "nowDate": i.nowDate, "orderDate": i.orderDate,
                    "patientName": i.patientName, "phoneNum": i.phoneNum, "doctorName": i.doctorName,
                    "doctorNum": i.doctorNum, "department": i.department, "status": i.status, "ok": i.ok}
            completedOrder.append(temp)
        if i.status == "待完成":
            temp = {"orderType": i.orderType, "nowDate": i.nowDate, "orderDate": i.orderDate,
                    "patientName": i.patientName, "phoneNum": i.phoneNum, "doctorName": i.doctorName,
                    "doctorNum": i.doctorNum, "department": i.department, "status": i.status, "ok": i.ok}
            outstandingOrder.append(temp)

    # 设置预约状态
    res = 0
    if request.method == "POST":
        get_json = request.get_json()
        for i in outstandingOrder:
            if get_json["ok"] == "已确认":
                temp = Order.query.filter(Order.nowDate == get_json["nowDate"]).first()
                temp.status = "已完成"
                db.session.commit()
                res = 1
                print("已确认")
            if get_json["ok"] == "待确认":
                res = 0
                print("待确认")

    return render_template("myOrder.html", patientInfo=user, completedOrder=completedOrder, outstandingOrder=outstandingOrder)


@index_blueprint.route('/orderDoctor', methods=['post', 'get'])
@login_required
def orderDoctor():
    username = session.get('username')
    # 个人中心信息
    user = User.query.filter(User.username == username).first()
    # patientInfo = PatientInfo.query.filter(PatientInfo.username == username).first()
    # 预约医生
    form_get_orderType = str(request.form.get('orderType'))
    form_get_nowDate = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    form_get_orderDate = str(request.form.get('orderDate'))
    form_get_patientName = str(request.form.get('patientName'))
    form_get_phoneNum = str(request.form.get('phoneNum'))
    form_get_doctorName = str(request.form.get('doctorName'))
    form_get_doctorNum = str(request.form.get('doctorNum'))
    form_get_department = str(request.form.get('department'))

    status = 0
    if form_get_orderType == "挂号" or form_get_orderType == "上门服务":
        OrderInfo = Order(orderType=form_get_orderType, nowDate=form_get_nowDate, orderDate=form_get_orderDate,
                          patientName=form_get_patientName, phoneNum=form_get_phoneNum, doctorName=form_get_doctorName,
                          doctorNum=form_get_doctorNum, department=form_get_department, status="待完成", ok="待确认")
        db.session.add_all([OrderInfo])
        db.session.commit()
        status += 1

    return render_template("orderDoctor.html", patientInfo=user, status=status)


@index_blueprint.route('/personal', methods=['post', 'get'])
@login_required
def personal():
    username = session.get('username')
    # 个人中心信息
    user = User.query.filter(User.username == username).first()

    if request.method == "POST":
        newusername = request.form.get("newusername")
        newpassword = request.form.get("newpassword")
        newphoneNum = request.form.get("newphoneNum")
        if len(newusername) > 0:
            user.username = newusername
        if len(newpassword) > 0:
            user.password = newpassword
        if len(newphoneNum) > 0:
            user.phoneNum = newphoneNum
        db.session.commit()

    return render_template("personal.html", patientInfo=user)


@index_blueprint.route('/healthEvaluation', methods=['post', 'get'])
@login_required
def healthEvaluation():
    username = session.get('username')
    # 个人中心信息
    user = User.query.filter(User.username == username).first()
    # 健康评估
    evaName = user.patientName
    healthEvaluation = HealthEvaluation.query.filter(HealthEvaluation.evaName == evaName).all()

    return render_template("healthEvaluation.html", patientInfo=user, healthEvaluation=healthEvaluation)


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
