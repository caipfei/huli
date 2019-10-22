#!/usr/bin/env python
#coding:utf-8

from flask import Blueprint, render_template, jsonify, url_for, redirect, request, make_response, \
    current_app
from ..models import Dept, Leave
from .. import db
from ..decorators import login_required
from datetime import datetime, timedelta
import json
import time
import xlrd
import math

leave = Blueprint('leave', __name__)

@leave.route('/', methods=['GET'])
@login_required
def home():
    return redirect(url_for('.index'))

@leave.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('leave/index.html')

@leave.route('/get_list', methods=['GET'])
@login_required
def get_list():
    args = request.args
    page = args.get('page', 1, type=int)
    if page <= 0:
        page = 1
    size = args.get('size', 20, type=int)
    search = args.get('search', None)
    data = []
    if search:
        pagination = Leave.query.filter(Leave.name.like('%%%s%%' % search)).order_by(Leave.id.desc()).paginate(page, size)
    else:
        pagination = Leave.query.order_by(Leave.id.desc()).paginate(page, size)

    total = pagination.total
    total_page = pagination.pages
    for item in pagination.items:
        id = item.id
        emp_sn = item.emp_sn
        name = item.name
        dept_id = item.dept_id
        time_start = item.time_start.strftime('%Y-%m-%d %H:%M:%S')
        time_end = item.time_end.strftime('%Y-%m-%d %H:%M:%S')
        days = item.days
        leave_type = item.leave_type
        remark = item.remark
        data.append({'id': id, 'emp_sn': emp_sn, 'name': name, 'dept_id': dept_id, 'time_start': time_start,
                     'time_end': time_end, 'days':days, 'leave_type': leave_type, 'remark': remark})
    return jsonify({'code': 0, 'total': total, 'total_page': total_page, 'currentPage': page, 'pageSize': size, 'data': data})

