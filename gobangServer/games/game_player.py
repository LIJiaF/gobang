# coding=utf-8
from tornado.websocket import WebSocketHandler
# 项目引用
from basics.baseFunc import *
from lobby.lobby_server import lobbyServer
from lobby.lobby_player import *
from .game_server import gameServer


class gamePlayer(lobbyPlayer):
    gameServer = gameServer.instance()

    def __init__(self, *args, **kwargs):
        super(gamePlayer, self).__init__(*args, **kwargs)
        self.chair = -1
        self.game = None

    def open(self, *args):
        sid = self.get_argument('sid')
        # roomId = self.get_argument('roomId')
        # if not sid or not roomId:
        if not sid:
            self.send_msg('参数错误,请重新登录')
            self.close(reason='参数错误')
            return
        UserInfo = self.lobbyServer.getSidAccount(sid)
        accountNo = UserInfo.get('accountNo')
        self.accountNo = accountNo
        self.logger(msg="[open] %s" % self)
        if accountNo:
            self.send_msg('%s, 欢迎您' % accountNo)
            self.loginTime = get_nowtime()
        else:
            self.send_msg('sid已过期,请重新登录')
            self.close(code=WS_Err_Code_Login_failed, reason='sid过期')

    def on_message(self, message):
        self.logger(msg="[on_message] %s" % message)
        print('[on_message]', type(message), message)
        try:
            msgData = json_decode(message)
            if not isinstance(msgData, dict):
                self.send_msg('指令无效')
            else:
                self.gameServer.dealMessage(self, msgData)
        except:
            traceback.print_exc()
            self.send_msg('指令无效')
