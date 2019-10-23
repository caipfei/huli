#!/usr/bin/env python
#coding:utf-8

from flask import request, redirect, url_for, jsonify
from .models import User
from functools import wraps

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        cookie = request.cookies
        sessionid = cookie.get('sessionid', '')
        user = User.verify_token(sessionid)
        if user:
            return func(*args, **kw)
        else:
            return redirect(url_for('main.login'))
    return wrapper


def login_required_ajax(func):
    @wraps(func)
    def wrapper(*args, **kw):
        cookie = request.cookies
        sessionid = cookie.get('sessionid', '')
        user = User.verify_token(sessionid)
        if user:
            return func(*args, **kw)
        else:
            return jsonify({'code': 10010, 'msg': '用户未登录或登陆信息已过期，请刷新登录'})
    return wrapper

