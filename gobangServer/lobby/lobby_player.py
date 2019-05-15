# coding=utf-8

# tornado
from tornado.websocket import WebSocketHandler
from tornado.escape import json_decode, json_encode
# 标准库
import logging
import traceback
import time

# 项目引用
from basics.baseFunc import get_nowtime
from .lobby_server import lobbyServer


class lobbyPlayer(WebSocketHandler):
    lobbyServer = lobbyServer()
    accountNo = ''
    ip = ''
    port = ''

    def __init__(self, *args, **kwargs):
        super(lobbyPlayer, self).__init__(*args, **kwargs)
        host = self.request.headers.get("Host").split(':')
        self.ip = self.request.remote_ip
        # self.ip = host[0]
        self.port = host[1]

    def __str__(self):
        return u'%s [%s:%s]' % (self.accountNo, self.ip, self.port)

    def check_origin(self, origin):
        '''是否允许跨域'''
        return True

    def open(self, accountNo=None, *args):
        if not accountNo:
            accountNo = self.get_argument('accountNo')
        self.accountNo = accountNo
        logging.info("[open] %s" % self)
        if accountNo:
            self.send_msg(u'%s, 欢迎您' % accountNo)
            self.lobbyServer.playerLogin(self)
        else:
            self.send_msg(u'accountNo不能为空')
            self.close()

    def on_message(self, message):
        logging.info("[on_message] %s", message)
        print(type(message),message)
        try:
            parsed = json_decode(message)
            # self.send_msg(parsed)
            self.lobbyServer.dealMessage(self,parsed)
        except:
            parsed = message
            traceback.print_exc()
            self.send_msg(parsed)

    def send_msg(self, msg_data):
        self.write_message(msg_data)

    def on_close(self):
        code = self.close_code
        reason = self.close_reason
        print('%s 连接已关闭 code[%s] reason[%s]' % (get_nowtime(), code, reason))
        self.lobbyServer.playerLogout(self, code=code, reason=reason)

    def write_message(self, message, binary=False):
        super(lobbyPlayer, self).write_message(message, binary)

    def close(self, code=None, reason=None):
        super(lobbyPlayer, self).close(code=code, reason=reason)
