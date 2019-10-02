#!/usr/bin/env python
#coding:utf-8

from flask import Blueprint, render_template, jsonify, url_for, redirect, request, make_response, \
    current_app
from ..models import User, Nurse, Dept
from .. import db
from datetime import datetime, timedelta
import json
import time


huli = Blueprint('huli', __name__)

@huli.route('/', methods=['GET'])
def home():
    return redirect(url_for('.index'))

'''登陆'''
@huli.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        arg = request.args
        if 'alert_msg' in arg:
            alert_msg = arg['alert_msg']
            alert_show = 'true'
        else:
            alert_msg = ''
            alert_show = 'false'
        return render_template('login.html', alert_msg=alert_msg, alert_show=alert_show)
    else:
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = User.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                if user.enable:
                    response = make_response(jsonify({'code': 0, 'data': {'username': username, 'nickname': user.nickname}}))
                    sessionid = user.generate_token()
                    outtime = datetime.today() + timedelta(seconds=current_app.config.get('COOKIE_EXPIRES', 3600))
                    response.set_cookie('sessionid', sessionid, expires=outtime)
                    return response
                else:
                    return jsonify({'code': 10001, 'msg': '该用户已被禁用'})
            else:
                return jsonify({'code': 10000, 'msg': '用户名或密码错误'})
        else:
            return jsonify({'code': 10002, 'msg': '用户不存在'})


@huli.route('/index', methods=['Get'])
def index():
    return render_template('index1.html')

'''获取科室列表'''
@huli.route('/get_dept', methods=['GET'])
def get_dept():
    depts = Dept.query.all()
    data = []
    for item in depts:
        id = item.id
        name = item.dept_name
        data.append({'id': id, 'name': name})
    return jsonify({'code': 0, 'data': data})

'''获取护士基本信息列表'''
@huli.route('/get_nurses', methods=['GET'])
def get_nurses():
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
@huli.route('/get_nurse/<emp_sn>', methods=['GET', 'POST'])
def get_nurse(emp_sn):
    pass

'''添加护士'''
@huli.route('/add_nurse', methods=['GET', 'POST'])
def add_nurse():
    if request.method == 'GET':
        return render_template('addNurse.html')
    data = request.get_json()
    print(data)
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

'''删除护士'''
@huli.route('/del_nurse', methods=['POST'])
def del_nurse():
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




