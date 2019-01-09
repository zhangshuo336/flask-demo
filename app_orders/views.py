#coding=utf-8
from . import orders

@orders.route("/orderss")
def orderss():
    return u'这是蓝图函数'