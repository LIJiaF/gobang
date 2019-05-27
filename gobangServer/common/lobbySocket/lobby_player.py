# coding=utf-8

# tornado
from tornado.escape import json_decode
# 标准库
import traceback

# 项目引用
from common.ws_code import *
from common.basics.baseObj import basePlayer
from common.basics.baseFunc import createSid, get_nowtime


class lobbyPlayer(basePlayer):

    def __init__(self, *args, **kwargs):
        super(lobbyPlayer, self).__init__(*args, **kwargs)
        self.lobbyServer = self.application.lobbyServer

    def open(self, *args):
        sid = self.get_argument('sid', None)
        accountNo = self.get_argument('accountNo', None)
        if not sid:
            if accountNo:
                sid = createSid(accountNo)
                self.lobbyServer.setSid(datas={'accountNo': accountNo, 'sid': sid}, delaySec=60)
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
            self.lobbyServer.playerLogin(self)
            self.loginTime = get_nowtime()
        else:
            self.send_msg('sid已过期,请重新登录!')
            self.close(code=WS_Err_Code_Login_failed, reason='sid过期')

    def on_message(self, message):
        self.logger(msg="[on_message] %s" % message)
        print('[on_message]', type(message), message)
        try:
            parsed = json_decode(message)
            if not isinstance(parsed, dict):
                self.send_msg('指令无效!')
            else:
                self.lobbyServer.dealMessage(self, parsed)
        except:
            traceback.print_exc()
            self.send_msg('指令无效!')

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
