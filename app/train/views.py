#!/usr/bin/env python
#coding:utf-8

from flask import Blueprint, render_template, jsonify, url_for, redirect, request
from ..models import Train
from .. import db
from ..decorators import login_required, login_required_ajax


train = Blueprint('train', __name__)

@train.route('/')
@login_required
def home():
    pass

@train.route('/index')
@login_required
def index():
    return render_template('train/index.html')

@train.route('/get_list', methods=['GET'])
@login_required_ajax
def get_list():
    args = request.args
    page = args.get('page', 1, type=int)
    if page <= 0:
        page = 1
    size = args.get('size', 20, type=int)
    search = args.get('search', None)
    data = []
    if search:
        pagination = Train.query.filter(Train.name.like('%%%s%%' % search)).order_by(Train.id.desc()).paginate(page, size)
    else:
        pagination = Train.query.order_by(Train.id.desc()).paginate(page, size)

    total = pagination.total
    total_page = pagination.pages
    for item in pagination.items:
        id = item.id
        emp_sn = item.emp_sn
        name = item.name
        dept = item.dept.dept_name
        date_start = item.date_start.strftime('%Y-%m-%d')
        date_end = item.date_end.strftime('%Y-%m-%d')
        train_name = item.train_name
        place = item.place
        fee = item.fee
        remark = item.remark
        data.append({'id': id, 'emp_sn': emp_sn, 'name': name, 'dept': dept, 'date_start': date_start,
                     'date_end': date_end, 'train_name':train_name, 'place': place, 'fee': fee, 'remark': remark})
    return jsonify({'code': 0, 'total': total, 'total_page': total_page, 'currentPage': page, 'pageSize': size, 'data': data})


@train.route('/add', methods=['POST'])
@login_required_ajax
def add():
    data = request.get_json()
    print(data)
    train = Train(**data)
    try:
        db.session.add(train)
        db.session.commit()
        return jsonify({'code': 0})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'code': 10008, 'msg': str(e)})


@train.route('/del', methods=['POST'])
@login_required_ajax
def delete():
    data = request.get_json()
    ids = data['ids']
    try:
        Train.query.filter(Train.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'code': 0})
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'code': 10005, 'msg': str(e)})
