from . import db
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
#
#
# class Config(object):
#     # sqlalchemy的配置参数
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/test'
#     # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://Client:b2pemXdyE3AeS5jY@124.220.193.237:3306/test'
#     SQLALCHEMY_TRACK_MODIFICATIONS = True
#     SECRET_KEY = 'random string'
#
#
# app.config.from_object(Config)
# db = SQLAlchemy(app)


# 用户类
class User(db.Model):
    """
    患者账户表
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    username = db.Column(db.String(80), unique=True)  # 账户名
    password = db.Column(db.String(80))  # 密码
    phoneNum = db.Column(db.String(120), unique=True)  # 电话
    patientName = db.Column(db.String(80))  # 姓名


    def __repr__(self):
        return '<User %r>' % self.username


# 患者信息
class PatientInfo(db.Model):
    """
    患者信息表
    """
    __tablename__ = "patient_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    patientName = db.Column(db.String(80))  # 患者姓名
    phoneNum = db.Column(db.String(20))  # 电话号码
    doctorNum = db.Column(db.String(80))  # 签约医生编号
    username = db.Column(db.String(80), unique=True)  # 用户名
    status = db.Column(db.String(20))  # 状态（已签约/未签约）


# 健康档案
class HealthRecords(db.Model):
    """
    健康档案表
    """
    __tablename__ = "health_records"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    username = db.Column(db.String(80), unique=True)  # 用户名
    patientName = db.Column(db.String(80))  # 患者姓名
    patientSex = db.Column(db.String(10))  # 患者性别
    patientBirth = db.Column(db.String(80))  # 出生日期
    nativePlace = db.Column(db.String(30))  # 籍贯
    patientNation = db.Column(db.String(20))  # 民族
    patientHeight = db.Column(db.String(20))  # 身高
    patientWeight = db.Column(db.String(20))  # 体重
    patientProfession = db.Column(db.String(80))  # 从事职业
    maritalStatus = db.Column(db.String(20))  # 婚姻状况
    degreeEducation = db.Column(db.String(80))  # 文化程度
    phoneNum = db.Column(db.String(20))  # 电话号码
    idNum = db.Column(db.String(30), unique=True)  # 身份证号
    contactAddress = db.Column(db.String(120))  # 联系地址
    bloodType = db.Column(db.String(20))  # 血型
    bloodPressure = db.Column(db.String(80))  # 血压
    patientVaccination = db.Column(db.String(120))  # 疫苗接种情况
    historyDrugAllergy = db.Column(db.String(120))  # 药物过敏史
    historyDisease = db.Column(db.String(120))  # 疾病史
    historyFamily = db.Column(db.String(120))  # 家族史
    historyOccupation = db.Column(db.String(120))  # 职业病危害接触史
    lifeStyle = db.Column(db.String(120))  # 生活方式
    recordNum = db.Column(db.String(120), unique=True)  # 档案编号
    updateDate = db.Column(db.TIMESTAMP(80))  # 档案更新日期


# 医生类
class Doctor(db.Model):
    """
    医生账户表
    """
    __tablename__ = "doctor"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    username = db.Column(db.String(80), unique=True)  # 账户名
    password = db.Column(db.String(80))  # 密码
    phoneNum = db.Column(db.String(120), unique=True)  # 电话
    doctorName = db.Column(db.String(80))  # 姓名

    def __repr__(self):
        return '<Doctor %r>' % self.username


# 医生信息类
class DoctorInfo(db.Model):
    """
    医生信息表
    """
    __tablename__ = "doctor_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    doctorName = db.Column(db.String(80))  # 医生姓名
    doctorNum = db.Column(db.String(80), unique=True)  # 医生编号
    phoneNum = db.Column(db.String(20))  # 电话号码
    hospitalName = db.Column(db.String(120))  # 所属医院
    department = db.Column(db.String(120))  # 所在科室
    specialty = db.Column(db.String(120))  # 擅长方面
    username = db.Column(db.String(80), unique=True)  # 用户名


# 随访记录类
class HomeVisit(db.Model):
    """
    随访记录表
    """
    __tablename__ = "home_visit"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    patientName = db.Column(db.String(80))  # 患者姓名
    visitWay = db.Column(db.String(20))  # 随访方式
    visitDate = db.Column(db.String(80))  # 随访日期
    disease = db.Column(db.String(80))  # 症状
    bloodPressure = db.Column(db.String(80))  # 血压
    bloodSugar = db.Column(db.String(80))  # 血糖
    saltUptake = db.Column(db.String(20))  # 摄盐情况
    sport = db.Column(db.String(20))  # 运动情况
    psychological = db.Column(db.String(20))  # 心理状况
    followDoctor = db.Column(db.String(80))  # 遵医行为
    doctorGuidance = db.Column(db.String(80))  # 医生指导
    doctorName = db.Column(db.String(80))  # 医生姓名
    doctorNum = db.Column(db.String(80))  # 医生编号


# 评估类
class HealthEvaluation(db.Model):
    """
    健康评估表
    """
    __tablename__ = "health_evaluation"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    evaTime = db.Column(db.String(80))  # 评估时间
    evaDocNum = db.Column(db.String(80))  # 医生编号
    evaName = db.Column(db.String(80))  # 患者姓名
    evaStatus = db.Column(db.String(20))  # 健康状况(健康状态、亚健康状态、患病状态)
    evaSuggest = db.Column(db.String(120))  # 医生评估建议


# 预约类
class Order(db.Model):
    """
    预约记录表(挂号预约、上门服务预约)
    """
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    orderType = db.Column(db.String(20))  # 预约类型
    nowDate = db.Column(db.String(80))  # 预约时间
    orderDate = db.Column(db.String(80))  # 就诊时间
    patientName = db.Column(db.String(80))  # 患者姓名
    phoneNum = db.Column(db.String(20))  # 患者电话
    doctorName = db.Column(db.String(80))  # 医生姓名
    doctorNum = db.Column(db.String(80))  # 医生编号
    department = db.Column(db.String(120))  # 预约科室
    status = db.Column(db.String(20))  # 状态（已完成/待完成）
    ok = db.Column(db.String(20))  # 医生确认否（已确认/待确认）


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    user1 = User(username="user1", password="123456a", phoneNum="13797782374", patientName="张三")
    user2 = User(username="user2", password="123esa1", phoneNum="18207481624", patientName="李四")
    user3 = User(username="user3", password="qwe12q932e", phoneNum="19935902270", patientName="王五")
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    patientInfo1 = PatientInfo(patientName="张三", phoneNum="13797782374", doctorNum="FD000001", username="user1", status="已签约")
    patientInfo2 = PatientInfo(patientName="李四", phoneNum="18207481624", doctorNum="FD000002", username="user2", status="已签约")
    patientInfo3 = PatientInfo(patientName="王五", phoneNum="19734782270", doctorNum="FD000003", username="user3", status="已签约")
    db.session.add_all([patientInfo1, patientInfo2, patientInfo3])
    db.session.commit()

    healthRecords1 = HealthRecords(username="user1", patientName="张三", patientSex="男", patientBirth="1985年09月13日",
                                   nativePlace="湖北武汉", patientNation="汉", patientHeight="180", patientWeight="80",
                                   patientProfession="教师", maritalStatus="已婚", degreeEducation="本科",
                                   phoneNum="13797782374", idNum="420621198509137236", contactAddress="湖北省武汉市洪山区鲁磨路12号",
                                   bloodType="A", bloodPressure="113/67", patientVaccination="已接种：乙肝疫苗、甲肝疫苗",
                                   historyDrugAllergy="无", historyDisease="无", historyFamily="无", historyOccupation="无",
                                   lifeStyle="压力大时喜欢抽烟喝酒，偶尔会运动，主要是跑步和游泳", recordNum="DA420621198509137206",
                                   updateDate="2022-02-24 13:45:23")
    healthRecords2 = HealthRecords(username="user2", patientName="李四", patientSex="男", patientBirth="1989年12月13日",
                                   nativePlace="湖北武汉", patientNation="汉", patientHeight="173", patientWeight="67",
                                   patientProfession="司机", maritalStatus="已婚", degreeEducation="高中",
                                   phoneNum="18207481624", idNum="420621198912135214", contactAddress="湖北省武汉市洪山区鲁磨路102号",
                                   bloodType="B", bloodPressure="118/69", patientVaccination="已接种：乙肝疫苗、甲肝疫苗",
                                   historyDrugAllergy="无", historyDisease="患有脂肪肝", historyFamily="无", historyOccupation="无",
                                   lifeStyle="烟龄20年，戒不掉，睡眠不太好，总是容易醒", recordNum="DA420621198912135214",
                                   updateDate="2022-02-11 19:15:20")
    healthRecords3 = HealthRecords(username="user3", patientName="王五", patientSex="男", patientBirth="1992年02月09日",
                                   nativePlace="湖北武汉", patientNation="汉", patientHeight="176", patientWeight="72",
                                   patientProfession="程序员", maritalStatus="已婚", degreeEducation="研究生",
                                   phoneNum="19734782270", idNum="420621199202092210", contactAddress="湖北省武汉市江岸区胜利路花园小区5栋1单元",
                                   bloodType="B", bloodPressure="123/71", patientVaccination="已接种：乙肝疫苗、甲肝疫苗",
                                   historyDrugAllergy="无", historyDisease="哮喘", historyFamily="高度近视", historyOccupation="无",
                                   lifeStyle="爱喝咖啡，经常熬夜，老是掉头发", recordNum="DA420621199202092210",
                                   updateDate="2022-1-21 09:47:03")
    db.session.add_all([healthRecords1, healthRecords2, healthRecords3])
    db.session.commit()

    doctor1 = Doctor(username="doctor1", password="123456a", phoneNum="17204839460", doctorName="李建华")
    doctor2 = Doctor(username="doctor2", password="123esa1", phoneNum="19684829502", doctorName="张成明")
    doctor3 = Doctor(username="doctor3", password="qwe12q932e", phoneNum="12244833461", doctorName="赵建伟")
    db.session.add_all([doctor1, doctor2, doctor3])
    db.session.commit()

    doctorInfo1 = DoctorInfo(doctorName="李建华", doctorNum="FD000001", phoneNum="17204839460",
                             hospitalName="武汉市第一人民医院", department="皮肤科", specialty="皮肤疾病预防及诊疗", username='doctor1')
    doctorInfo2 = DoctorInfo(doctorName="张成明", doctorNum="FD000002", phoneNum="19684829502",
                             hospitalName="武汉市第二人民医院", department="口腔科", specialty="口腔疾病预防及诊疗", username='doctor2')
    doctorInfo3 = DoctorInfo(doctorName="赵建伟", doctorNum="FD000003", phoneNum="12244833461",
                             hospitalName="武汉市第三人民医院", department="消化内科", specialty="消化道疾病预防及诊疗", username='doctor3')
    db.session.add_all([doctorInfo1, doctorInfo2, doctorInfo3])
    db.session.commit()

    homeVisit1 = HomeVisit(patientName="张三", visitWay="上门服务", visitDate="2022-5-6 19:05:23", disease="胸闷",
                           bloodPressure="正常，115/69", bloodSugar="正常，5.2", saltUptake="中量", sport="适度，一周2-4次，以跑步为主",
                           psychological="正常，心态无较大波动", followDoctor="一般，抽烟频率不能很好克制",
                           doctorGuidance="最近胸闷可能跟天气变化有关，再加上烟瘾较大，造成感官比较强烈。建议提前关注天气状况，做好相关预防，尽量少抽烟",
                           doctorName="张成明", doctorNum="FD000001")
    homeVisit2 = HomeVisit(patientName="李四", visitWay="电话服务", visitDate="2022-5-6 10:17:26", disease="头晕",
                           bloodPressure="正常，118/71", bloodSugar="正常，5.1", saltUptake="中量", sport="适度，一周3次，喜欢打篮球",
                           psychological="正常，心态无较大波动", followDoctor="一般，抽烟频率不能很好克制",
                           doctorGuidance="最近头晕可能跟天气变化有关，再加上烟瘾较大，造成感官比较强烈。建议提前关注天气状况，做好相关预防，尽量少抽烟",
                           doctorName="李建华", doctorNum="FD000002")
    homeVisit3 = HomeVisit(patientName="王五", visitWay="上门服务", visitDate="2022-5-6 16:25:23", disease="胸闷",
                           bloodPressure="正常，120/75", bloodSugar="正常，5.2", saltUptake="中量", sport="偏低，一周0或1次，以快步走为主",
                           psychological="正常，心态无较大波动", followDoctor="一般，抽烟频率不能很好克制",
                           doctorGuidance="最近胸闷可能跟天气变化有关，再加上烟瘾较大，造成感官比较强烈。建议提前关注天气状况，做好相关预防，尽量少抽烟",
                           doctorName="赵建伟", doctorNum="FD000003")
    db.session.add_all([homeVisit1, homeVisit2, homeVisit3])
    db.session.commit()

    order1 = Order(orderType="挂号", nowDate="2022-05-16 12:23:43", orderDate="2022-05-18 14:23:43", patientName="张三",
                   phoneNum="13797782374", doctorName="李建华", doctorNum="FD000001", department="皮肤科", status="已完成", ok="已确认")
    order2 = Order(orderType="上门服务", nowDate="2022-05-19 08:24:12", orderDate="2022-06-30 18:23:43", patientName="李四",
                   phoneNum="18207481624", doctorName="张成明", doctorNum="FD000002", department="口腔科", status="待完成", ok="已确认")
    order3 = Order(orderType="挂号", nowDate="2022-05-20 10:23:43", orderDate="2022-05-25 16:20:13", patientName="王五",
                   phoneNum="19734782270", doctorName="李建华", doctorNum="FD000001", department="皮肤科", status="已完成", ok="已确认")
    db.session.add_all([order1, order2, order3])
    db.session.commit()

    healthEvaluation1 = HealthEvaluation(evaTime="2022-06-13 15:22:12", evaStatus="亚健康状态", evaDocNum="FD000001", evaName="张三",
                                        evaSuggest="最近胸闷可能跟天气变化有关，再加上烟瘾较大，造成感官比较强烈。建议提前关注天气状况，做好相关预防，尽量少抽烟")
    healthEvaluation2 = HealthEvaluation(evaTime="2022-06-15 18:34:42", evaStatus="亚健康状态", evaDocNum="FD000002", evaName="李四",
                                        evaSuggest="最近胸闷可能跟天气变化有关，再加上烟瘾较大，造成感官比较强烈。建议提前关注天气状况，做好相关预防，尽量少抽烟")
    healthEvaluation3 = HealthEvaluation(evaTime="2022-06-18 12:37:57", evaStatus="亚健康状态", evaDocNum="FD000003", evaName="王五",
                                        evaSuggest="最近胸闷可能跟天气变化有关，再加上烟瘾较大，造成感官比较强烈。建议提前关注天气状况，做好相关预防，尽量少抽烟")
    db.session.add_all([healthEvaluation1, healthEvaluation2, healthEvaluation3])
    db.session.commit()

    # app.run()
