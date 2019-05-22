# coding=utf-8

# tornado
from tornado.websocket import WebSocketHandler
from tornado.escape import json_decode, json_encode
# 标准库
import logging
import traceback
import time

# 项目引用
from basics.baseFunc import *
from .lobby_server import lobbyServer
from .lobby_code import *
from datetime import datetime


class lobbyPlayer(WebSocketHandler):
    lobbyServer = lobbyServer.instance()
    accountNo = ''
    ip = ''
    port = ''
    loginTime = ''

    def __init__(self, *args, **kwargs):
        super(lobbyPlayer, self).__init__(*args, **kwargs)
        host = self.request.headers.get("Host").split(':')
        self.ip = self.request.remote_ip
        # self.ip = host[0]
        self.port = host[1]

    def __str__(self):
        return '%s [%s:%s]' % (self.accountNo, self.ip, self.port)

    def logger(self, msg, level='info'):
        logging.info('[%s] [%s:%s] %s' % (get_nowtime(), self.accountNo, id(self), msg))

    def getInfo(self):
        return {
            'accountNo': self.accountNo,
            'loginTime': strfDataTime(self.loginTime),
            'ip'       : self.ip,
        }

    def check_origin(self, origin):
        '''是否允许跨域'''
        return True

    def open(self, accountNo=None, sid=None, *args):
        # if not accountNo:
        #     accountNo = self.get_argument('accountNo')
        if not sid:
            sid = self.get_argument('sid')

        UserInfo = self.lobbyServer.getSidAccount(sid)
        accountNo = UserInfo.get('accountNo')
        self.accountNo = accountNo
        self.logger(msg="[open] %s" % self)
        if accountNo:
            self.send_msg('%s, 欢迎您' % accountNo)
            self.lobbyServer.playerLogin(self)
            self.loginTime = get_nowtime()
        else:
            self.send_msg('sid已过期,请重新登录')
            self.close(code=WS_Err_Code_Login_failed, reason='sid过期')

    def on_message(self, message):
        self.logger(msg="[on_message] %s" % message)
        print('[on_message]',type(message), message)
        try:
            parsed = json_decode(message)
            # self.send_msg(parsed)
            if not isinstance(parsed, dict):
                self.send_msg('指令无效')
            else:
                self.lobbyServer.dealMessage(self, parsed)
        except:
            parsed = message
            traceback.print_exc()
            self.send_msg('指令无效')

    def send_Datas(self, code=0, data='', url='', msg='',isSend=True):
        dataType = 'none'
        if data:
            if isinstance(data, dict):
                dataType = 'dict'
            elif isinstance(data, (list, set)):
                dataType = 'list'
            elif isinstance(data, (str,)):
                dataType = 'string'
        resultData = {
            'url'     : url or '',
            'data'    : data or '',
            'dataType': dataType or '',
            'code'    : code,
            'msg'     : msg or msg,
        }
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

        if code == WS_Err_Code_Login_failed:
            pass
        if code == WS_Err_Code_Login_byOther:
            pass
        else:
            self.lobbyServer.playerLogout(self, code=code, reason=reason)

    def write_message(self, message, binary=False):
        super(lobbyPlayer, self).write_message(message, binary)

    def close(self, code=None, reason=None):
        super(lobbyPlayer, self).close(code=code, reason=reason)
