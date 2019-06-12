# coding=utf-8

# 标准库
from tornado.escape import json_decode
import traceback
# 公共模块
from common.basics.baseObj import basePlayer
from common.basics.baseFunc import *
# ws模块
from common.ws_code import *
from .game_logger import s_logger


class gamePlayer(basePlayer):

    def __init__(self, *args, **kwargs):
        super(gamePlayer, self).__init__(*args, **kwargs)
        self.lobbyServer = self.application.lobbyServer
        self.gameServer = self.application.gameServer
        self.chair = -1
        self.game = None
        # 是否准备开始
        self.isReadyStart = False

    def logger(self, msg, level='info'):
        s_logger.info('[%s:%s] %s' % (self.accountNo, id(self), msg))

    def open(self, *args):
        sid = self.get_argument('sid', None)
        accountNo = self.get_argument('accountNo', None)
        if not sid:
            if accountNo:
                sid = createSid(accountNo)
                self.gameServer.lobbyServer.setSid(datas={'accountNo': accountNo, 'sid': sid}, delaySec=60)
        if not sid:
            self.send_msg('参数错误,请重新登录!')
            self.close(reason='参数错误')
            return
        self.isClose = False
        UserInfo = self.lobbyServer.getSidAccount(sid)
        accountNo = UserInfo.get('accountNo')
        self.accountNo = accountNo
        self.logger(msg="[open] %s" % self)
        if accountNo:
            self.send_msg('%s, 欢迎您' % accountNo)
            self.loginTime = get_nowtime()
            self.gameServer.login(self)
        else:
            self.send_msg('sid已过期,请重新登录!')
            self.close(code=WS_Err_Code_Login_failed, reason='sid过期')

    def on_message(self, message):
        self.logger(msg="[on_message] %s" % message)
        try:
            msgData = json_decode(message)
            if not isinstance(msgData, dict):
                self.send_msg('指令无效!')
            else:
                self.gameServer.dealMessage(self, msgData)
        except:
            traceback.print_exc()
            self.send_msg('指令无效!')
