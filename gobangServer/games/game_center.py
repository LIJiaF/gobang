# coding=utf-8

from .game_deal import gameDeal
import random
from .game_logger import g_logger, e_logger
import traceback
from basics.baseFunc import *


class gameCenter:
    '''游戏流程控制中心'''

    def __init__(self, game_server, roomId, *args, **kwargs):
        self.maxPlayerCount = self.getMaxPlayerCount()
        self.players = [None] * self.maxPlayerCount
        self.game_server = game_server
        self.roomId = roomId
        self.owner = None  # 房主(创建者)
        self.curGameCount = 0  # 当前局数
        self.stage = 0  # 当前游戏状态
        self.exitPlayers = []  # 掉线玩家的位置列表
        self.curActionChair = None  # 当前操作玩家位置
        self.actionNum = 0  # 当前操作编号
        self.playerCount = 0  # 当前房间的人数
        self.resetData()

    def resetData(self):
        '''每局初始化参数'''
        self.dealMgr = self.getDealMgr()
        # 时间记录
        self.gameStartTime = 0
        self.gameEndTime = 0
        self.bankerChair = -1  # 庄家位置

    def getMaxPlayerCount(self):
        '''获取最大玩家数'''
        return 2

    def getDealMgr(self):
        '''牌局数据控制类'''
        return gameDeal()

    def getEmptyChair(self):
        """获取当前房间剩余位置,无则返回-1"""
        for chair, player in enumerate(self.players):
            if not player:
                return chair
        return -1

    def onjoinGame(self, player):
        '''加入房间'''
        chair = self.getEmptyChair()
        assert chair != -1
        player.chair = chair
        player.game = self
        self.playerCount += 1
        self.players[chair] = player
        for _player in self.getPlayers():
            _player.send_msg('玩家[%s]加入房间[%s]' % (player.accountNo, self.roomId))
        self.logger('[onjoinGame] 玩家[%s]加入房间' % (player.accountNo))
        self.afterJoinGame(player=player)

    def afterJoinGame(self, player):
        '''加入房间后续操作'''
        if self.isCanStartGame():
            self.logger('[afterJoinGame] 可以开始啦')

    def isCanStartGame(self):
        '''当前是否满足开始条件'''
        allPlayers = self.getPlayers()
        if len(allPlayers) == self.maxPlayerCount:
            return True
        return False

    def onGameStart(self, player):
        '''游戏开始'''
        if player != self.owner:
            player.send_msg('你不是房主,不能开始游戏!')
            return
        if not self.isCanStartGame():
            player.send_msg('人数不足,请等齐人员再开始!')
            return
        self.gameStartTime = get_timeStamp()
        self.bankerChair = self.getBanker()

    def getBanker(self):
        '''获取庄家位(即为第一行动位)'''
        chairs = [_player.chair for _player in self.getPlayers()]
        bankerChair = random.choice(chairs)
        self.logger('[getBanker] chairs=>[%s] bankerChair[%s]' % (chairs, bankerChair))
        return random.choice(chairs)

    def getPlayers(self, excludePlayers=()):
        '''获取当前房间所有非空玩家'''
        return [player for player in self.players if (player and player not in excludePlayers)]

    def logger(self, str, level='info'):
        try:
            if level == 'info':
                g_logger.info(u'[%s] %s' % (self.roomId, str))
            elif level == 'error':
                e_logger.info(u'[%s] %s' % (self.roomId, str))
            else:
                print(u'[%s] %s' % (self.roomId, str))
        except:
            traceback.print_exc()
            print(u'[%s] %s' % (self.roomId, str))
