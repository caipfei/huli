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

transfer = Blueprint('transfer', __name__)

@transfer.route('/gets', methods=['GET'])
@login_required
def gets():
    data = []
    items = Transfer.query.all()
    for item in items:
        name = item.name
        outdept = item.outdept.dept_name
        indept = item.indept.dept_name
        trans_date = item.trans_date.strftime('%Y-%m-%d')
        end_date = item.end_date.strftime('%Y-%m-%d')
        trans_type = item.trans_type
        remark = item.remark
        data.append({'name': name, 'outdept': outdept, 'indept': indept, 'trans_date': trans_date, 'end_date': end_date,
                     'trans_type': trans_type, 'remark': remark})
    return jsonify({'code': 0, 'data': data})

