"""
查看我的签约医生信息
"""

from flask import render_template, session, Blueprint
from Patient.app.models import PatientInfo, DoctorInfo
from Patient.app.views.index import login_required

doctor_info_blueprint = Blueprint('doctor_info', __name__)


@doctor_info_blueprint.route('/myDoctorInfo')
@login_required
def display_doctor_info():
    username = session.get('username')
    doctorNum = PatientInfo.query.filter(PatientInfo.username == username).first().doctorNum
    doctor_info = DoctorInfo.query.filter(DoctorInfo.doctorNum == doctorNum).first()
    doctorInfo = {'doctorName': doctor_info.doctorName, 'doctorNum': doctor_info.doctorNum,
                  'phoneNum': doctor_info.phoneNum, 'hospitalName': doctor_info.hospitalName,
                  'department': doctor_info.department, 'specialty': doctor_info.specialty}

    return render_template('myDoctorInfo.html', doctorInfo=doctorInfo)

