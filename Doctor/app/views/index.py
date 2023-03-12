from functools import wraps
from flask import request, render_template, redirect, url_for, flash, session, Blueprint, Response
from sqlalchemy import and_, or_
from Patient.app.models import db, Doctor, DoctorInfo, PatientInfo, Order, HealthRecords, HomeVisit, HealthEvaluation
from Patient.app.utils.qrcode import Code
from datetime import datetime

index_blueprint = Blueprint('index', __name__)
graph_code = ''  # 全局变量验证码


############################################
# 辅助函数、装饰器
############################################


# 登录检验（用户名、密码验证）
def valid_login(username, password):
    user = Doctor.query.filter(and_(Doctor.username == username, Doctor.password == password)).first()
    if user:
        return True
    else:
        return False


# 注册检验（用户名、邮箱验证）
def valid_regist(username, doctorName, phoneNum):
    user = Doctor.query.filter(or_(Doctor.doctorName == doctorName, Doctor.phoneNum == phoneNum)).first()
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
    print('lo:', graph_code)
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']) and request.form[
            'qrcode'].lower() == graph_code.lower():
            flash("成功登录！")
            session['username'] = request.form.get('username')
            return redirect(url_for('page.page'))
        else:
            error = '错误的用户名或密码！'

    return render_template('logindoc.html', error=error)


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
        elif valid_regist(request.form['username'], request.form['doctorName'], request.form['phoneNum']):
            user = Doctor(username=request.form['username'], password=request.form['password1'],
                          doctorName=request.form['doctorName'], phoneNum=request.form['phoneNum'])
            db.session.add(user)
            db.session.commit()

            flash("成功注册！")
            return redirect(url_for('index.login'))
        else:
            error = '该用户名或邮箱已被注册！'

    return render_template('registdoc.html', error=error)


# 5.个人中心
@index_blueprint.route('/page')
@login_required
def panel():
    username = session.get('username')
    user = Doctor.query.filter(Doctor.username == username).first()
    doctorinfo = DoctorInfo.query.filter(DoctorInfo.username == username).first()

    allPatient = PatientInfo.query.filter(PatientInfo.doctorNum == doctorinfo.doctorNum).all()
    signed = 0
    signing = 0
    if allPatient is not None:
        for i in allPatient:
            # 已签约用户
            if i.status == "已签约":
                signed += 1
            # 待签约用户
            if i.status == "待签约":
                signing += 1

    allOrder = Order.query.filter(Order.doctorNum == doctorinfo.doctorNum).all()
    ordered = 0
    ordering = 0
    if allOrder is not None:
        for i in allOrder:
            # 已审批预约
            if i.ok == "已确认":
                ordered += 1
            # 待审批预约
            if i.ok == "待确认":
                ordering += 1

    return render_template("page.html", doctorInfo=doctorinfo, signed=signed, signing=signing, ordered=ordered,
                           ordering=ordering)


@index_blueprint.route('/personal', methods=['post', 'get'])
@login_required
def personal():
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()

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

    return render_template("personal.html", doctorInfo=user)


@index_blueprint.route('/contractAudit', methods=['post', 'get'])
@login_required
def contractAudit():
    contractInfo = []
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()

    # 审批签约
    doctorInfo = DoctorInfo.query.filter(DoctorInfo.doctorName == user.doctorName).first()
    if doctorInfo is not None:
        patientInfo = PatientInfo.query.filter(PatientInfo.doctorNum == doctorInfo.doctorNum).all()
        if patientInfo is not None:
            for i in patientInfo:
                if i.status == "待签约":
                    temp = {"patientName": i.patientName, "phoneNum": i.phoneNum, "status": i.status}
                    contractInfo.append(temp)

    return render_template("contractAudit.html", doctorInfo=user, contractInfo=contractInfo)


@index_blueprint.route('/contractPatient', methods=['post', 'get'])
@login_required
def contractPatient():
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()
    # 签约审核
    if request.method == "POST":
        get_json = request.get_json()
        phoneNum = get_json["phoneNum"]
        temp = PatientInfo.query.filter(PatientInfo.phoneNum == phoneNum).first()
        temp.status = "已签约"
        db.session.commit()

    return None


@index_blueprint.route('/orderAudit', methods=['post', 'get'])
@login_required
def orderAudit():
    orderAuditInfo = []
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()
    # 审批预约
    doctorInfo = DoctorInfo.query.filter(DoctorInfo.doctorName == user.doctorName).first()
    if doctorInfo is not None:
        orderInfo = Order.query.filter(Order.doctorNum == doctorInfo.doctorNum).all()
        if orderInfo is not None:
            for i in orderInfo:
                if i.ok == "待确认":
                    temp = {"orderType": i.orderType, "orderDate": i.orderDate, "patientName": i.patientName,
                            "phoneNum": i.phoneNum, "ok": i.ok}
                    orderAuditInfo.append(temp)

    return render_template("orderAudit.html", doctorInfo=user, orderAuditInfo=orderAuditInfo)


@index_blueprint.route('/orderAuditOk', methods=['post', 'get'])
@login_required
def orderAuditOk():
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()
    # 预约审核
    if request.method == "POST":
        get_json = request.get_json()
        orderDate = get_json["orderDate"]
        patientName = get_json["patientName"]
        temp = Order.query.filter(and_(Order.orderDate == orderDate, Order.patientName == patientName)).first()
        temp.ok = "已确认"
        db.session.commit()

    return None


@index_blueprint.route('/doctorRegist', methods=['post', 'get'])
@login_required
def doctorRegist():
    doctor_RegInfo = []
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()
    # 医生信息获取
    doctorRegInfo = DoctorInfo.query.filter(DoctorInfo.username == username).first()
    if doctorRegInfo is not None:
        doctor_RegInfo.append(doctorRegInfo)
    # 医生信息注册
    if request.method == "POST":
        doctor_name = request.form.get("doctor_name")
        phone_num = request.form.get("phone_num")
        hospital_name = request.form.get("hospital_name")
        department = request.form.get("department")
        specialty = request.form.get("specialty")
        doctor_num = "FD" + str(phone_num)
        doctor_info = DoctorInfo(doctorName=doctor_name, doctorNum=doctor_num, phoneNum=phone_num,
                                 hospitalName=hospital_name, department=department, specialty=specialty,
                                 username=username)
        db.session.add(doctor_info)
        db.session.commit()

    return render_template("doctorRegist.html", doctorInfo=user, doctor_RegInfo=doctor_RegInfo)


@index_blueprint.route('/signPatient', methods=['post', 'get'])
@login_required
def signPatient():
    all_sign_info = []
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()
    # 已签约信息
    doctorNum = DoctorInfo.query.filter(DoctorInfo.username == username).first().doctorNum
    if doctorNum is not None:
        allSignInfo = PatientInfo.query.filter(PatientInfo.doctorNum == doctorNum).all()
        if allSignInfo is not None:
            for i in allSignInfo:
                if i.status == "已签约":
                    temp = {"patientName": i.patientName, "phoneNum": i.phoneNum, "status": i.status}
                    all_sign_info.append(temp)

    return render_template("signPatient.html", doctorInfo=user, all_sign_info=all_sign_info)


@index_blueprint.route('/lookRecord', methods=['post', 'get'])
@login_required
def lookRecord():
    lookRecord = []
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()
    # 签约用户档案
    doctorNum = DoctorInfo.query.filter(DoctorInfo.username == username).first().doctorNum
    if doctorNum is not None:
        allSignInfo = PatientInfo.query.filter(PatientInfo.doctorNum == doctorNum).all()
        if allSignInfo is not None:
            for i in allSignInfo:
                if i.status == "已签约":
                    patientusername = i.username
                    patientname = i.patientName
                    record = HealthRecords.query.filter(HealthRecords.username == patientusername).first()
                    temp = {"patientname": patientname, "record": record}
                    lookRecord.append(temp)

    return render_template("lookRecord.html", doctorInfo=user, lookRecord=lookRecord)


@index_blueprint.route('/homeVisit', methods=['post', 'get'])
@login_required
def homeVisit():
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()
    doctor = DoctorInfo.query.filter(DoctorInfo.username == username).first()
    # 添加随访记录
    patient_name = str(request.form.get("patient_name"))
    visit_way = str(request.form.get("visit_way"))
    visit_date = str(request.form.get("visit_date"))
    disease = str(request.form.get("disease"))
    blood_pressure = str(request.form.get("blood_pressure"))
    blood_sugar = str(request.form.get("blood_sugar"))
    salt_uptake = str(request.form.get("salt_uptake"))
    sport = str(request.form.get("sport"))
    psychological = str(request.form.get("psychological"))
    follow_doctor = str(request.form.get("follow_doctor"))
    doctor_guidance = str(request.form.get("doctor_guidance"))
    doctor_name = doctor.doctorName
    doctor_num = doctor.doctorNum

    if visit_way == "上门服务" or visit_way == "电话服务":
        home = HomeVisit(patientName=patient_name, visitWay=visit_way, visitDate=visit_date, disease=disease,
                         bloodPressure=blood_pressure, bloodSugar=blood_sugar, saltUptake=salt_uptake, sport=sport,
                         psychological=psychological, followDoctor=follow_doctor, doctorGuidance=doctor_guidance,
                         doctorName=doctor_name, doctorNum=doctor_num)
        db.session.add(home)
        db.session.commit()

    # 随访历史记录
    allVisit = HomeVisit.query.filter(HomeVisit.doctorNum == doctor_num).all()

    return render_template("homeVisit.html", doctorInfo=user, allVisit=allVisit)


@index_blueprint.route('/healthEvaluation', methods=['post', 'get'])
@login_required
def healthEvaluation():
    username = session.get('username')
    # 个人中心信息
    user = Doctor.query.filter(Doctor.username == username).first()
    doctor = DoctorInfo.query.filter(DoctorInfo.username == username).first()
    # 添加健康评估
    evaDocNum = doctor.doctorNum
    evaTime = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    evaName = str(request.form.get("evaName"))
    evaStatus = str(request.form.get("evaStatus"))
    evaSuggest = str(request.form.get("evaSuggest"))
    if evaStatus == "健康状态" or evaStatus == "亚健康状态" or evaStatus == "患病状态":
        eva = HealthEvaluation(evaTime=evaTime, evaDocNum=evaDocNum, evaName=evaName, evaStatus=evaStatus,
                               evaSuggest=evaSuggest)
        db.session.add(eva)
        db.session.commit()

    # 评估记录
    allEva = HealthEvaluation.query.filter(HealthEvaluation.evaDocNum == evaDocNum).all()

    return render_template("healthEvaluation.html", doctorInfo=user, allEva=allEva)


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
