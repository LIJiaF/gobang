# coding=utf-8

from datetime import datetime
import time
import uuid
from tornado.ioloop import IOLoop


def get_nowtime():
    return datetime.now()


def get_timeStamp(double=1000):
    '''
    获取当前时间戳(默认:毫秒)
    :param double:倍数,默认1000,代表毫秒,可传入1代替为秒
    :return:当前时间戳
    '''
    return int(time.time() * double)


def strpDataTime(strTime):
    return datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")


def strfDataTime(dt=None):
    if not dt: dt = get_nowtime()
    assert isinstance(dt, datetime)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def createSid(accountNo):
    _uuid = uuid.uuid1()
    sid = str(_uuid).replace('-', '')
    return sid


def doLater(delaySec, callback, *args, **kwargs):
    IOLoop.current().call_later(delay=delaySec, callback=callback, *args, **kwargs)
