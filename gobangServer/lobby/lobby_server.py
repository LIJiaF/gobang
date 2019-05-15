# coding=utf-8

# tornado
# 标准库
import logging
# 项目引用
from basics.baseObj import Singleton
from .lobby_deal import lobbyDeal


class lobbyServer(Singleton):

    def __init__(self, *args, **kwargs):
        self.players = {}
        self.onlinePlayers = {}  # 在线玩家
        self.unlinePlayers = {}  # 离线玩家,(无游戏中)
        self.offlinePlayers = {}  # 掉线玩家,(游戏中)

        self.lobbyDealMgr = lobbyDeal()

    def playerLogin(self, player, *args, **kwargs):
        accountNo = player.accountNo
        if accountNo in self.onlinePlayers:
            oldPlayer = self.onlinePlayers[accountNo]
        self.onlinePlayers[accountNo] = player
        logging.info(msg=u'[playerLogin] 玩家 %s 登录' % (player))

    def playerLogout(self, player, *args, **kwargs):
        accountNo = player.accountNo
        if accountNo in self.onlinePlayers:
            del self.onlinePlayers[accountNo]
        self.unlinePlayers[accountNo] = player
        logging.info(msg=u'[playerLogout] 玩家 %s 离线' % (player))

    def dealMessage(self, player, msgData):
        return self.lobbyDealMgr.doing(player=player, msgData=msgData)
