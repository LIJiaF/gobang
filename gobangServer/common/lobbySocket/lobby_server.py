# coding=utf-8

# 标准库
import logging
# 项目引用
from .lobby_deal import lobbyDeal
from common.ws_code import *
from common.basics.baseFunc import *


class lobbyServer(object):
    application = None
    gameServer = None

    def __init__(self, *args, **kwargs):
        self.logger('初始化lobbyServer')
        self.onlinePlayers = {}  # 在线玩家
        self.unlinePlayers = {}  # 离线玩家,(无游戏中)
        # SessionId
        self.sid_account_map = {}
        self.account_sid_map = {}
        # 个人信息
        self.accountInfo_map = {}
        # 前端接口处理类
        self.lobbyDealMgr = lobbyDeal(lobbyServer=self)

    def logger(self, msg, level='info'):
        logging.info('[%s] %s' % (get_nowtime(), msg))

    def resetSid(self, sid):
        self.logger('[resetSid] 开始重置 sid[%s]' % sid)
        if sid in self.sid_account_map:
            accountNo = self.sid_account_map[sid]
            if accountNo in self.account_sid_map and self.account_sid_map[accountNo] == sid:
                del self.account_sid_map[accountNo]
            del self.sid_account_map[sid]

    def getSidAccount(self, sid=None, *args, **kwargs):
        # self.logger('[getSidAccount] sid => %s' % sid)
        # self.logger('[getSidAccount] sid_account_map => %s' % pformat(self.sid_account_map))
        # self.logger('[getSidAccount] account_sid_map => %s' % pformat(self.account_sid_map))
        # self.logger('[getSidAccount] accountInfo_map => %s' % pformat(self.accountInfo_map))
        accountNo = self.sid_account_map.get(sid, '')
        if not accountNo:
            self.logger('[getSidAccount] Error [not accountNo !]')
            return {}
        curSid = self.account_sid_map.get(accountNo, '')
        if curSid != sid:
            self.logger('[getSidAccount] Error [different sid !]')
            return {}
        userInfo = self.accountInfo_map.get(accountNo, {})
        if not userInfo:
            self.logger('[getSidAccount] Error [not userInfo !]')
            return {}
        return userInfo

    def setSid(self, datas, delaySec=0):
        sid = datas['sid']
        accountNo = datas['accountNo']
        self.sid_account_map[sid] = accountNo
        self.account_sid_map[accountNo] = sid
        self.accountInfo_map[accountNo] = datas
        if delaySec:
            doLater(delaySec=delaySec, callback=self.resetSid, sid=sid)

    def playerLogin(self, player, *args, **kwargs):
        '''大厅用户登录'''
        accountNo = player.accountNo
        if accountNo in self.onlinePlayers:
            oldPlayer = self.onlinePlayers[accountNo]
            oldPlayer.send_msg(msg_data='您的账号已在其他地方登录,若操作异常,请重新登录!')
            oldPlayer.logger(msg='[playerLogin] 玩家被挤离线')
            oldPlayer.close(code=WS_Err_Code_Login_byOther, reason='异地登录')
        self.onlinePlayers[accountNo] = player
        player.logger(msg='[playerLogin] 玩家登录')

    def playerLogout(self, player, *args, **kwargs):
        '''大厅用户离线'''
        accountNo = player.accountNo
        if accountNo in self.onlinePlayers:
            if player == self.onlinePlayers[accountNo]:
                del self.onlinePlayers[accountNo]
                self.unlinePlayers[accountNo] = player
        player.logger(msg='[playerLogout] 玩家离线')

    def dealMessage(self, player, msgData):
        return self.lobbyDealMgr.doing(player=player, msgData=msgData)
