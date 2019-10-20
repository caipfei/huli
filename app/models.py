#!/usr/bin/env python
#coding:utf-8

from . import db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Nurse(db.Model):
    __tablename___ = 'nurse'
    emp_sn = db.Column(db.String(8), primary_key=True)  #工号
    name = db.Column(db.String(32), nullable=False)     #姓名
    sex = db.Column(db.Integer)                         #性别,男1女0
    id_card = db.Column(db.String(18))                  #身份证号码
    dept_id = db.Column(db.Integer, db.ForeignKey('dept.id'))    #科室id
    level = db.Column(db.String(16))                    #层级
    birth_date = db.Column(db.Date)                     #出生日期
    age = db.Column(db.Float)                           #年龄
    native = db.Column(db.String(64))                   #籍贯
    nation = db.Column(db.String(64))                   #民族
    pre_education = db.Column(db.String(32))             #职前学历
    pre_school = db.Column(db.String(128))              #职前毕业学校
    pre_graduate_day = db.Column(db.Date)               #职前毕业时间
    pre_professional = db.Column(db.String(128))         #专业
    top_education = db.Column(db.String(64))            #最高学历
    post_school = db.Column(db.String(128))              #职后毕业学校
    post_graduate_day = db.Column(db.Date)              #职后毕业时间
    post_professional = db.Column(db.String(128))        #职后专业
    firstjob_day = db.Column(db.Date)                   #参加工作时间
    enter_hospital_day = db.Column(db.Date)             #调入医院时间
    top_title = db.Column(db.String(32))                #最高职称
    get_date = db.Column(db.Date)                       #获得日期
    end_season = db.Column(db.Date)                     #季末
    work_time = db.Column(db.Float)                     #工作年限
    work_time_divide = db.Column(db.String(32))         #工作年限分界
    area = db.Column(db.String(32))                     #片区
    post1 = db.Column(db.String(32))                    #岗位1
    post2 = db.Column(db.String(32))                    #岗位2
    status = db.Column(db.String(32))                   #身份

    def to_dict(self):
        birth_date = self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None
        pre_graduate_day = self.pre_graduate_day.strftime('%Y-%m-%d') if self.pre_graduate_day else None
        post_graduate_day = self.post_graduate_day.strftime('%Y-%m-%d') if self.post_graduate_day else None
        firstjob_day = self.firstjob_day.strftime('%Y-%m-%d') if self.firstjob_day else None
        enter_hospital_day = self.enter_hospital_day.strftime('%Y-%m-%d') if self.enter_hospital_day else None
        get_date = self.get_date.strftime('%Y-%m-%d') if self.get_date else None
        end_season = self.end_season.strftime('%Y-%m-%d') if self.end_season else None
        return {'emp_sn': self.emp_sn, 'name': self.name, 'sex': self.sex, 'id_card': self.id_card, 'dept_id': self.dept_id,
                'level': self.level, 'birth_date': birth_date, 'age': self.age, 'native': self.native,
                'nation': self.nation,'pre_education': self.pre_education, 'pre_school': self.pre_school,
                'pre_graduate_day': pre_graduate_day, 'pre_professional': self.pre_professional,
                'top_education': self.top_education, 'post_school': self.post_school,'post_graduate_day': post_graduate_day,
                'post_professional': self.post_professional, 'firstjob_day': firstjob_day,
                'enter_hospital_day': enter_hospital_day, 'top_title': self.top_title, 'get_date': get_date,
                'end_season': end_season, 'work_time': self.work_time, 'work_time_divide': self.work_time_divide, 'area': self.area,
                'post1': self.post1, 'post2': self.post2, 'status': self.status}


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(8), nullable=False, unique=True)     #登录名
    password = db.Column(db.String(64), nullable=False)                 #登陆密码
    nickname = db.Column(db.String(32), nullable=False)                 #昵称
    enable = db.Column(db.Integer, default=1)                           #是否可用

    def generate_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['COOKIE_EXPIRES'])
        return s.dumps({'username': self.username})

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            user = User.query.filter_by(username=data['username']).first()
            return user if user else None
        except Exception:
            return None

'''调动记录模型'''
class Transfer(db.Model):
    __tablename__ = 'transfer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    outdept_id = db.Column(db.Integer, db.ForeignKey('dept.id'), nullable=False)
    indept_id = db.Column(db.Integer, db.ForeignKey('dept.id'), nullable=False)
    trans_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    trans_type = db.Column(db.String(64))
    remark = db.Column(db.String(255))

class Dept(db.Model):
    __tablename__ = 'dept'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 科室ID
    code = db.Column(db.String(16))  # 科室编码
    dept_name = db.Column(db.String(32), nullable=False)  # 科室名称
    nurses = db.relationship('Nurse', backref='dept')
    outdepts = db.relationship('Transfer', backref='outdept', foreign_keys=[Transfer.outdept_id])
    indepts = db.relationship('Transfer', backref='indept', foreign_keys=[Transfer.indept_id])
