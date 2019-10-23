#!/usr/bin/env python
#coding:utf-8

class BaseConfig(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:root@localhost/nursing'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '4166a10a6f50db381db5acfd13a251d8'
    COOKIE_EXPIRES = 60 * 60                #cookie过期时间

class DevConfig(BaseConfig):
    pass

class TestConfig(BaseConfig):
    pass

class ProductConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:Admin@1234@192.168.100.221/nursing'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'develop': DevConfig,
    'test': TestConfig,
    'product': ProductConfig,
    'default': DevConfig
}
