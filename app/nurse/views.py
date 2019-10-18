#!/usr/bin/env python
#coding:utf-8

from flask import Blueprint, render_template, jsonify, url_for, redirect, request, make_response, \
    current_app
from ..models import User, Nurse, Dept
from .. import db
from ..decorators import login_required
from datetime import datetime, timedelta
import json
import time
import xlrd


nurse = Blueprint('nurse', __name__)

# @nurse.route('/', methods=['GET'])
# def home():
#     return redirect(url_for('.index'))

'''登陆'''
# @nurse.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         arg = request.args
#         if 'alert_msg' in arg:
#             alert_msg = arg['alert_msg']
#             alert_show = 'true'
#         else:
#             alert_msg = ''
#             alert_show = 'false'
#         return render_template('login.html', alert_msg=alert_msg, alert_show=alert_show)
#     else:
#         data = request.get_json()
#         username = data['username']
#         password = data['password']
#         user = User.query.filter_by(username=username).first()
#         if user:
#             if user.password == password:
#                 if user.enable:
#                     response = make_response(jsonify({'code': 0, 'data': {'username': username, 'nickname': user.nickname}}))
#                     sessionid = user.generate_token()
#                     outtime = datetime.today() + timedelta(seconds=current_app.config.get('COOKIE_EXPIRES', 3600))
#                     response.set_cookie('sessionid', sessionid, expires=outtime)
#                     return response
#                 else:
#                     return jsonify({'code': 10001, 'msg': '该用户已被禁用'})
#             else:
#                 return jsonify({'code': 10000, 'msg': '用户名或密码错误'})
#         else:
#             return jsonify({'code': 10002, 'msg': '用户不存在'})

@nurse.route('/index', methods=['Get'])
@login_required
def index():
    return render_template('nurse/index.html')


'''获取护士列表'''
@nurse.route('/all', methods=['GET'])
@login_required
def get_all():
    nurses = Nurse.query.all()
    data = []
    for item in nurses:
        emp_sn = item.emp_sn
        name = item.name
        sex = '' if item.sex == None else ('男' if item.sex == 1 else '女')
        dept = item.dept.dept_name if item.dept else None
        data.append({'emp_sn': emp_sn, 'name': name, 'sex': sex, 'dept': dept})
    return jsonify({'code': 0, 'data': data})


'''获取护士详细信息'''
@nurse.route('/get/<emp_sn>', methods=['GET', 'POST'])
@login_required
def get_nurse(emp_sn):
    nurse = Nurse.query.filter_by(emp_sn=emp_sn).first()
    if nurse:
        return jsonify({'code': 0, 'data': nurse.to_dict()})
    else:
        return jsonify({'code': 10006, 'msg': '未查到工号为%s的护士' % emp_sn})

'''添加护士'''
@nurse.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return render_template('nurse/addNurse.html')
    data = request.get_json()
    emp_sn = data['emp_sn']
    if Nurse.query.filter_by(emp_sn=emp_sn).all():
        return jsonify({'code': 10003, 'msg': '工号为%s的人员已存在' % emp_sn})
    nurse = Nurse(**data)
    try:
        db.session.add(nurse)
        db.session.commit()
        return jsonify({'code': 0})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'code': 10004, 'msg': str(e)})

'''批量导入'''
@nurse.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['file']
    f = file.read()
    data = xlrd.open_workbook(file_contents=f)
    names = data.sheet_names()
    filter_name = list(filter(lambda item : item.find('护士信息') > -1, names))
    table_index = names.index(filter_name[0]) if filter_name else 0
    table = data.sheets()[table_index]
    nrows = table.nrows
    ncols = table.ncols
    if ncols < 30:
        return jsonify({'code': 1005, 'msg': '数据表格式不正确'})
    # print(table.row_values(0))
    # print(table.row_values(1))
    # print(table.row_values(3))
    # print(table.cell(3, 7).ctype)
    # print(table.cell(3, 13).ctype)
    # d = datetime(*xlrd.xldate_as_tuple(table.cell_value(3, 13), 0))
    # print(d.strftime('%Y/%m/%d'))
    total = nrows - 2
    error_count = 0
    for i in range(2, nrows):
        try:
            row_data = table.row_values(i)
            emp_sn = row_data[2]
            nurse = Nurse.query.filter_by(emp_sn=emp_sn).first()
            if nurse:
                error_count += 1
                continue
            name = row_data[3]
            dept_name = row_data[1]
            dept = Dept.query.filter_by(dept_name=dept_name).first()
            if dept:
                dept_id = dept.id
            else:
                dept = Dept(dept_name=dept_name)
                db.session.add(dept)
                db.session.flush()
                db.session.commit()
                dept_id = dept.id
            sex = 1 if row_data[5] == '男' else 0
            level = row_data[4]
            id_card = row_data[6].strip('\u3000')
            birth_date = datetime(*xlrd.xldate_as_tuple(table.cell_value(i, 7), 0)).strftime('%Y-%m-%d') if table.cell(i, 7).ctype == 3 else row_data[7]
            age = round(row_data[8], 1) if row_data[8] else None
            native = row_data[9]
            nation = row_data[10]
            pre_education = row_data[11]
            pre_school = row_data[12]
            pre_graduate_day = datetime(*xlrd.xldate_as_tuple(table.cell_value(i, 13), 0)).strftime('%Y/%m/%d') if table.cell(i, 13).ctype == 3 else row_data[13]
            pre_professional = row_data[14]
            top_education = row_data[15]
            post_school = row_data[16]
            post_graduate_day = datetime(*xlrd.xldate_as_tuple(table.cell_value(i, 17), 0)).strftime('%Y/%m/%d') if table.cell(i, 17).ctype == 3 else row_data[17]
            post_professional = row_data[18]
            firstjob_day = row_data[19] if table.cell(i, 19).ctype != 3 else datetime(*xlrd.xldate_as_tuple(table.cell_value(i, 19), 0)).strftime('%Y/%m/%d')
            enter_hospital_day = row_data[20] if table.cell(i, 20).ctype != 3 else datetime(*xlrd.xldate_as_tuple(table.cell_value(i, 20), 0)).strftime('%Y/%m/%d')
            top_title = row_data[21]
            get_date = row_data[22] if table.cell(i, 22).ctype != 3 else datetime(*xlrd.xldate_as_tuple(table.cell_value(i, 22), 0)).strftime('%Y/%m/%d')
            end_season = row_data[23] if table.cell(i, 23).ctype != 3 else datetime(*xlrd.xldate_as_tuple(table.cell_value(i, 23), 0)).strftime('%Y/%m/%d')
            work_time = round(row_data[24], 2) if row_data[24] else None
            work_time_divide = row_data[25]
            area = row_data[26]
            post1 = row_data[27]
            post2 = row_data[28]
            status = row_data[29]
            nurse_data = {'emp_sn': emp_sn, 'name': name, 'sex': sex, 'id_card': id_card, 'dept_id': dept_id, 'level': level, 'birth_date': birth_date, 'age': age,
                          'native': native, 'nation': nation, 'pre_education': pre_education, 'pre_school': pre_school, 'pre_graduate_day': pre_graduate_day,
                          'pre_professional': pre_professional, 'top_education': top_education, 'post_school': post_school, 'post_graduate_day': post_graduate_day,
                          'post_professional': post_professional, 'firstjob_day': firstjob_day, 'enter_hospital_day': enter_hospital_day, 'top_title': top_title,
                          'get_date': get_date, 'end_season': end_season, 'work_time': work_time, 'work_time_divide': work_time_divide, 'area': area, 'post1': post1,
                          'post2': post2, 'status': status}
            nurse = Nurse(**nurse_data)
            db.session.add(nurse)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            error_count += 1
            continue
    return jsonify({'code': 0, 'total': total, 'error_count': error_count, 'success_count': total-error_count})

'''删除护士'''
@nurse.route('/delete', methods=['POST'])
@login_required
def delete():
    data = request.get_json()
    emps = data['emps']
    try:
        Nurse.query.filter(Nurse.emp_sn.in_(emps)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'code': 0})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'code': 10005, 'msg': '删除失败'})

'''获取更新护士信息'''
@nurse.route('/detail/<emp_sn>', methods=['GET', 'POST'])
@login_required
def detail(emp_sn):
    if request.method == 'GET':
        return render_template('nurse/detail.html', emp_sn=emp_sn)
    else:
        data = request.get_json()
        try:
            Nurse.query.filter_by(emp_sn=emp_sn).update(data)
            db.session.commit()
            return jsonify({'code': 0})
        except Exception as e:
            print(e)
            db.session.rollback()
            return jsonify({'code': 10007, 'msg': str(e)})





