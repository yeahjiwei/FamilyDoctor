"""
医生专家库查询 [此搜索功能后续还要改进]
"""

from flask import render_template, Blueprint, request
from Patient.app.models import DoctorInfo
from Patient.app.views.index import login_required
from ..utils.cut_words import cut_words

doctorDatabase_blueprint = Blueprint('doctorDatabase', __name__)


@doctorDatabase_blueprint.route('/doctorDatabase', methods=['post', 'get'])
@login_required
def search_doctorDatabase():
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

    print(search_result)
    print(type(search_result))

    searchResult = {'data': search_result, 'tag': th_tag}

    return render_template("doctorDatabase.html", searchResult=searchResult)
