from . import db
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
#
#
# class Config(object):
#     # sqlalchemy的配置参数
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:379658yjw251023@localhost:3306/test'
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
    email = db.Column(db.String(120), unique=True)  # 邮箱

    def __repr__(self):
        return '<User %r>' % self.username


# 患者信息
class PatientInfo(db.Model):
    """
    患者信息表
    """
    __tablename__ = "patientInfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    patientName = db.Column(db.String(80))  # 患者姓名
    phoneNum = db.Column(db.String(20))  # 电话号码
    doctorNum = db.Column(db.String(80), unique=True)  # 签约医生编号
    username = db.Column(db.String(80), unique=True)  # 用户名


# 健康档案
class HealthRecords(db.Model):
    """
    健康档案表
    """
    __tablename__ = "healthRecords"
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
    email = db.Column(db.String(120), unique=True)  # 邮箱

    def __repr__(self):
        return '<Doctor %r>' % self.username


# 医生信息类
class DoctorInfo(db.Model):
    """
    医生信息表
    """
    __tablename__ = "doctorInfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    doctorName = db.Column(db.String(80))  # 医生姓名
    doctorNum = db.Column(db.String(80), unique=True)  # 医生编号
    phoneNum = db.Column(db.String(20))  # 电话号码
    hospitalName = db.Column(db.String(120))  # 所属医院
    department = db.Column(db.String(120))  # 所在科室
    specialty = db.Column(db.String(120))  # 擅长方面


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    user1 = User(username="user1", password="123456a", email="user1@163.com")
    user2 = User(username="user2", password="123esa1", email="user2@163.com")
    user3 = User(username="user3", password="qwe12q932e", email="user3@163.com")
    db.session.add_all([user1, user2, user3])
    db.session.commit()

    patientInfo1 = PatientInfo(patientName="张三", phoneNum="13797782374", doctorNum="FD000001", username="user1")
    patientInfo2 = PatientInfo(patientName="李四", phoneNum="18207481624", doctorNum="FD000002", username="user2")
    patientInfo3 = PatientInfo(patientName="王五", phoneNum="19734782270", doctorNum="FD000003", username="user3")
    db.session.add_all([patientInfo1, patientInfo2, patientInfo3])
    db.session.commit()

    # healthRecords1 = HealthRecords(username="user1", patientName="张三", patientSex="男", patientBirth="1985年9月13日",
    #                                nativePlace="湖北武汉", patientNation="汉", patientHeight="180", patientWeight="80",
    #                                patientProfession="教师", maritalStatus="已婚", degreeEducation="本科",
    #                                phoneNum="13797782374", idNum="420621198509137206", contactAddress="湖北省武汉市洪山区鲁磨路12号",
    #                                bloodType="A", bloodPressure="113/67", patientVaccination="已接种：乙肝疫苗、甲肝疫苗",
    #                                historyDrugAllergy="")

    doctor1 = Doctor(username="doctor1", password="123456a", email="doctor1@163.com")
    doctor2 = Doctor(username="doctor2", password="123esa1", email="doctor2@163.com")
    doctor3 = Doctor(username="doctor3", password="qwe12q932e", email="doctor3@163.com")
    db.session.add_all([doctor1, doctor2, doctor3])
    db.session.commit()

    doctorInfo1 = DoctorInfo(doctorName="李建华", doctorNum="FD000001", phoneNum="17204839460",
                             hospitalName="武汉市第一人民医院", department="皮肤科", specialty="皮肤疾病预防及诊疗")
    doctorInfo2 = DoctorInfo(doctorName="张成明", doctorNum="FD000002", phoneNum="19684829502",
                             hospitalName="武汉市第二人民医院", department="口腔科", specialty="口腔疾病预防及诊疗")
    doctorInfo3 = DoctorInfo(doctorName="赵建伟", doctorNum="FD000003", phoneNum="12244833461",
                             hospitalName="武汉市第三人民医院", department="消化内科", specialty="消化道疾病预防及诊疗")
    db.session.add_all([doctorInfo1, doctorInfo2, doctorInfo3])
    db.session.commit()

    # app.run()
