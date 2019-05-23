# coding=utf-8

from .game_deal import gameDeal
import random
from .game_logger import g_logger, e_logger
import traceback
from basics.baseFunc import *
from tornado import gen
from tornado.ioloop import Future, IOLoop

gameStage_WaitStart = 0
gameStage_Gaming = 1
gameStage_Balance = 2
gameStage_End = 2


class gameCenter:
    '''游戏流程控制中心'''

    def __init__(self, game_server, roomId, *args, **kwargs):
        self.maxPlayerCount = self.getMaxPlayerCount()
        self.players = [None] * self.maxPlayerCount
        self.game_server = game_server
        self.roomId = roomId
        self.owner = None  # 房主(创建者)
        self.curGameCount = 0  # 当前局数
        self.exitPlayers = []  # 掉线玩家的位置列表
        self.playerCount = 0  # 当前房间的人数
        self.resetData()

    def resetData(self):
        '''每局初始化参数'''
        self.dealMgr = self.getDealMgr()
        # 时间记录
        self.gameStartTime = 0
        self.gameEndTime = 0
        self.bankerChair = -1  # 庄家位置
        self.winChair = -1  # 当前赢家
        self.curActionChair = None  # 当前操作玩家位置
        self.stage = gameStage_WaitStart  # 当前游戏状态
        self.actionNum = 0  # 当前操作编号

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
        player.send_msg('您加入房间[%s]成功' % (self.roomId))
        for _player in self.getPlayers(excludePlayers=player):
            _player.send_msg('玩家[%s]加入房间[%s]' % (player.accountNo, self.roomId))
            player.send_msg('玩家[%s]已在房间内' % (player.accountNo))

        self.logger('[onjoinGame] 玩家[%s]加入房间' % (player.accountNo))
        self.afterJoinGame(player=player)

    def afterJoinGame(self, player):
        '''加入房间后续操作'''
        self.game_server.gameingPlayer[player.accountNo] = player

        if self.isCanStartGame():
            self.logger('[afterJoinGame] 可以开始啦')
            self.onGameStart(self.players[0])

    def getOwner(self):
        try:
            return self.players[0]
        except:
            traceback.print_exc()
            return None

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
        self.stage = gameStage_Gaming
        self.curGameCount += 1
        self.sendAll('游戏开始')
        self.sendAll({'url': '/game/gameStart'})
        self.gameStartTime = get_timeStamp()
        self.bankerChair = self.getBanker()
        self.sendAll('庄家位为[%s]' % (self.bankerChair))
        self.afterGameStart()

    def afterGameStart(self, *args, **kwargs):
        firstPlayer = self.players[self.bankerChair]
        self.sendCurAction(firstPlayer)

    def sleepSec(self, sec):
        f = Future()

        def call(*args, **kwargs):
            print('[%s] [call]' % (get_nowtime()))
            f.set_result(None)

        IOLoop.instance().call_later(sec, call)
        return f

    # @gen.coroutine
    def sendCurAction(self, curPlayer):
        self.sendAll('轮到玩家[%s]操作' % curPlayer.accountNo)
        self.curActionChair = curPlayer.chair
        # yield self.sleepSec(3)
        # nexter = self.getNexter(curPlayer)
        # self.sendCurAction(nexter)

    def getNexter(self, curPlayer):
        """
        返回curPlayer的下一家
        """
        for x in range(1, self.maxPlayerCount):
            next_player = self.players[(curPlayer.chair + x) % self.maxPlayerCount]
            if next_player:
                return next_player
        return None

    def sendAll(self, msgData):
        for _player in self.getPlayers():
            _player.send_msg(msgData)

    def getBanker(self):
        '''获取庄家位(即为第一行动位)'''
        chairs = [_player.chair for _player in self.getPlayers()]
        bankerChair = random.choice(chairs)
        self.logger('[getBanker] chairs=>[%s] bankerChair[%s]' % (chairs, bankerChair))
        return random.choice(chairs)

    def getPlayers(self, excludePlayers=()):
        if not isinstance(excludePlayers, (list, set)):
            excludePlayers = (excludePlayers,)

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

    def playChess(self, player, msgData, params, *args, **kwargs):
        if self.stage == gameStage_End:
            player.send_msg('游戏已结束,请继续下局')
            return
        if player.chair != self.curActionChair:
            player.send_msg('当前不是你行动')
            return
        x = params.get('x', None)
        y = params.get('y', None)
        if x == None or y == None:
            player.send_msg('棋子坐标不能为空')
            return
        play_type = player.chair + 1
        msgData['params']['type'] = player.chair + 1
        self.sendAll(msgData)
        if not self.dealMgr.play_chess((x, y), play_type):
            player.send_msg('下棋点(%s,%s)操作无效,不是有效点' % (x, y))
            return
        else:
            if self.dealMgr.checkIsWinResult_One(x, y, play_type):
                self.sendAll('玩家[%s] 胜利' % (player.accountNo))
                self.curActionChair = None
                self.stage = gameStage_Balance
                self.stage = gameStage_End
                self.winChair = player.chair
                self.sendAll({'url': '/game/alertMsg', 'params': {'msg': '游戏已结束,玩家[%s]胜利' % (player.accountNo)}})
                return

        nexter = self.getNexter(player)
        self.sendCurAction(nexter)

    def nextGame(self, player, msgData, params, *args, **kwargs):
        if self.stage != gameStage_End:
            player.send_msg('当前游戏未开始,或未结束,不可继续下局!')
            return
        if player != self.owner:
            player.send_msg('你不是房主,不能继续下局!')
            return
        if not self.isCanStartGame():
            player.send_msg('当前人数不满足开始条件!')
            return
        self.resetData()
        self.onGameStart(player)

    def copyOldPlayer(self, player, oldPlayer):
        player.game = oldPlayer.game
        player.chair = oldPlayer.chair
        self.players[player.chair] = player
        if self.owner == oldPlayer:
            self.owner = player
        self.game_server.gameingPlayer[player.accountNo] = player

    def doRefreshData(self, player):
        if self.stage in [gameStage_Gaming, gameStage_Balance, gameStage_End]:
            if self.curActionChair != None:
                curPlayer = self.players[self.curActionChair]
                player.send_msg('[重连] 当前轮到玩家[%s]操作' % (curPlayer.accountNo))
            chessBoard = self.dealMgr.get_chessBoard()
            msg_data = {'url'   : '/game/refreshChessBoard',
                        'params': {'chessBoard': chessBoard.tolist(), 'curGameCount': self.curGameCount}}
            player.send_msg(msg_data)
            if self.stage in [gameStage_Balance, gameStage_End]:
                winner = self.players[self.winChair]
                player.send_msg('[重连] 当前游戏已结束,赢家是[%s]' % (winner.accountNo))
                player.send_msg({'url': '/game/alertMsg', 'params': {'msg': '游戏已结束,房主可点击继续下局游戏按钮'}})
        elif self.stage == gameStage_WaitStart:
            player.send_msg('[重连] 游戏未开始,请等待')
        else:
            pass
