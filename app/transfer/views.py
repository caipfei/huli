#!/usr/bin/env python
#coding:utf-8

from flask import Blueprint, render_template, jsonify, url_for, redirect, request, make_response, \
    current_app
from ..models import User, Nurse, Dept, Transfer
from .. import db
from ..decorators import login_required
from datetime import datetime, timedelta
import json
import time
import xlrd
import math

transfer = Blueprint('transfer', __name__)

@transfer.route('/', methods=['GET'])
@login_required
def home():
    return redirect(url_for('.index'))

@transfer.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('transfer/index.html')

@transfer.route('/get_list', methods=['GET'])
@login_required
def get_list():
    args = request.args
    page = args.get('page', 1, type=int)
    if page <= 0:
        page = 1
    size = args.get('size', 20, type=int)
    search = args.get('search', None)
    data = []
    start = size * (page - 1)
    end = size * page
    if search:
        items = Transfer.query.filter_by(name=search).order_by(Transfer.trans_date.desc(), Transfer.id.desc()).slice(start, end).all()
    else:
        items = Transfer.query.order_by(Transfer.trans_date.desc()).slice(start, end).all()
    total = len(items)
    total_page = math.ceil(total / size)
    for item in items:
        id = item.id
        name = item.name
        outdept = item.outdept.dept_name
        indept = item.indept.dept_name
        trans_date = item.trans_date.strftime('%Y-%m-%d')
        end_date = item.end_date.strftime('%Y-%m-%d')
        trans_type = item.trans_type
        remark = item.remark
        data.append({'name': name, 'outdept': outdept, 'indept': indept, 'trans_date': trans_date, 'end_date': end_date,
                     'trans_type': trans_type, 'remark': remark, 'id': id})
    return jsonify({'code': 0, 'total': total, 'total_page': total_page, 'currentPage': page, 'pageSize': size, 'data': data})


@transfer.route('/add', methods=['POST'])
@login_required
def add():
    data = request.get_json()
    print(data)
    transfer = Transfer(**data)
    try:
        db.session.add(transfer)
        db.session.commit()
        return jsonify({'code': 0})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'code': 10008, 'msg': str(e)})


@transfer.route('/del', methods=['POST'])
@login_required
def delete():
    data = request.get_json()
    ids = data['ids']
    try:
        Transfer.query.filter(Transfer.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'code': 0})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'code': 10005, 'msg': str(e)})


