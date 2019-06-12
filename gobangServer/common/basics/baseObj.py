# coding=utf-8

from tornado.websocket import WebSocketHandler
from tornado.escape import json_encode
import threading
import logging
from common.basics.baseFunc import *
from pprint import pprint, pformat


class Singleton(object):
    _instance_lock = threading.Lock()
    _instance = {}

    @classmethod
    def instance(cls):
        className = getattr(cls, '__name__')
        if className not in Singleton._instance:
            with Singleton._instance_lock:
                if className not in Singleton._instance:
                    Singleton._instance[className] = object.__new__(cls)
                    Singleton._instance[className].__init__()
                    pprint('Singleton._instance => ', Singleton._instance)
        return Singleton._instance[className]


class basePlayer(WebSocketHandler):
    accountNo = ''
    ip = ''
    port = ''
    loginTime = ''
    isClose = True

    def __init__(self, *args, **kwargs):
        super(basePlayer, self).__init__(*args, **kwargs)
        host = self.request.headers.get("Host").split(':')
        self.ip = self.request.remote_ip
        # self.ip = host[0]
        self.port = host[1]

    def __str__(self):
        return '[%s:%s:%s]' % (self.accountNo, self.ip, self.port)

    def logger(self, msg, level='info'):
        logging.info('[%s] [%s:%s] %s' % (get_nowtime(), self.accountNo, id(self), msg))

    def getInfo(self):
        return {'accountNo': self.accountNo, 'loginTime': strfDataTime(self.loginTime), 'ip': self.ip, }

    def check_origin(self, origin):
        '''是否允许跨域'''
        return True

    def open(self, *args):
        pass

    def on_message(self, message):
        pass

    def send_Datas(self, code=0, data='', url='', msg='', isSend=True):
        dataType = 'none'
        if data != '':
            if isinstance(data, dict):
                dataType = 'dict'
            elif isinstance(data, (list, set, tuple)):
                dataType = 'list'
            elif isinstance(data, (str,)):
                dataType = 'string'
        resultData = {'url': url or '', 'data': data, 'dataType': dataType or '', 'code': code, 'msg': msg or msg, }
        resultData = json_encode(resultData)
        if isSend:
            self.send_msg(resultData)
        return resultData

    def send_msg(self, msg_data):
        self.logger(msg='[send_msg] %s' % (msg_data))
        self.write_message(msg_data)

    def on_close(self, isLogout=True):
        code = self.close_code
        reason = self.close_reason
        self.logger(msg='[on_close] 连接已关闭 code[%s] reason[%s]' % (code, reason))

    def write_message(self, message, binary=False):
        if self.isClose:
            self.logger(msg='[write_message] 玩家已离线 不发送信息 %s' % (message))
            return
        super(basePlayer, self).write_message(message, binary)

    def close(self, code=None, reason=None):
        self.isClose = True
        super(basePlayer, self).close(code=code, reason=reason)
