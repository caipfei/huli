from flask import Blueprint, render_template, jsonify, url_for, redirect, request, make_response, \
    current_app
from ..models import User, Nurse, Dept
from ..decorators import login_required, login_required_ajax
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/')
def index():
    cookie = request.cookies
    sessionid = cookie.get('sessionid', '')
    user = User.verify_token(sessionid)
    if user:
        return redirect(url_for('nurse.index'))
    return redirect(url_for('.login'))

'''用户登录'''
@main.route('/login', methods=['GET', 'POST'])
def login():
    print(request.args)
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
                    response = make_response(
                        jsonify({'code': 0, 'data': {'username': username, 'nickname': user.nickname}}))
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

'''登出'''
@main.route('/logout')
def logout():
    response = make_response(redirect(url_for('.index')))
    response.delete_cookie('sessionid')
    return response

'''获取科室列表'''
@main.route('/get_dept', methods=['GET'])
@login_required_ajax
def get_dept():
    depts = Dept.query.all()
    data = []
    for item in depts:
        id = item.id
        name = item.dept_name
        data.append({'id': id, 'name': name})
    return jsonify({'code': 0, 'data': data})