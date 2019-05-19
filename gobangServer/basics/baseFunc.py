# coding=utf-8

from datetime import datetime
import time
import uuid
from tornado.ioloop import IOLoop


def get_nowtime():
    return datetime.now()


def get_timeStamp():
    return time.time()


def strpDataTime(strTime):
    return datetime.strptime(strTime, "%Y-%m-%d %H:%M:%S")


def strfDataTime(dt):
    assert isinstance(dt, datetime)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def createSid(accountNo):
    _uuid = uuid.uuid1()
    sid = str(_uuid).replace('-', '')
    return sid


def doLater(delaySec, callback, *args, **kwargs):
    IOLoop.current().call_later(delay=delaySec, callback=callback, *args, **kwargs)
