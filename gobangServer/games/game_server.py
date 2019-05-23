# coding=utf-8

# 项目引用
from basics.baseObj import Singleton
from lobby.lobby_server import lobbyServer
from games.game_center import gameCenter
# 标准库
import random


class gameServer(Singleton):
    lobbyServer = lobbyServer.instance()
    games = []
    roomIdMaps = {}  # 房间号:房间类
    gameingPlayer = {}  # 玩家No:上次的玩家类

    def __init__(self, *args, **kwargs):
        self.setActionMap()

        self.lobbyServer.gameServer = self

    def setActionMap(self):
        self.allAction_Deal_Map = {
            'game': {
                'joinGame'      : self.joinGame,
                'joinRandomGame': self.joinRandomGame,
                'createGame'    : self.createGame,
                'playChess'     : self.playChess,
                'nextGame'      : self.nextGame,
            }
        }

    def getGameMgr(self):
        return gameCenter

    def getRoomId(self, tryCount=100):
        UsedRoomId = self.roomIdMaps.keys()
        while tryCount:
            roomId = str(random.randint(100000, 999999))
            if roomId not in UsedRoomId:
                return roomId
        return None

    def createNewGame(self):
        roomId = self.getRoomId()
        if not roomId:
            print('[createNewGame] 房间号获取失败')
            return
        # game = self.getGameMgr()
        game = gameCenter(game_server=self, roomId=roomId)
        self.roomIdMaps[roomId] = game
        return game

    def dealMessage(self, player, msgData):
        routeUrl = msgData.get('url')
        if not routeUrl:
            player.send_msg('指令无效')
            return
        urlsList = list(filter(None, routeUrl.split('/')))
        if len(urlsList) < 2:
            player.send_msg('指令无效')
            return
        mgrRoute = urlsList[0]
        bodyRoute = '/'.join(urlsList[1:])
        if mgrRoute not in self.allAction_Deal_Map or bodyRoute not in self.allAction_Deal_Map[mgrRoute]:
            player.send_msg('指令无效')
            return
        func = self.allAction_Deal_Map[mgrRoute][bodyRoute]
        return func(player=player, routeUrl=routeUrl, params=msgData.get('params', {}), msgData=msgData)

    def joinGame(self, player, msgData, params, *args, **kwargs):
        if player.game:
            player.send_msg('你已在游戏中')
            return
        roomId = params.get('roomId')
        if not roomId:
            player.send_msg('未选择房间')
            return

        game = self.roomIdMaps.get(roomId)
        if not game:
            player.send_msg('房间不存在')
            return
        game.onjoinGame(player)

    def joinRandomGame(self, player, msgData, params, *args, **kwargs):
        if player.game:
            player.send_msg('你已在游戏中')
            return
        readyGame = None
        for _roomId, _game in self.roomIdMaps.items():
            if _game.playerCount < _game.maxPlayerCount:
                readyGame = _game
                break
        if not readyGame:
            player.send_msg('暂无空房间,可选择创建房间')
            return
        readyGame.onjoinGame(player)

    def createGame(self, player, msgData, params, *args, **kwargs):
        if player.game:
            player.send_msg('你已在游戏中')
            return
        roomId = self.getRoomId()
        if not roomId:
            print('[createGame] 房间号获取失败')
            return
        # game = self.getGameMgr()
        game = gameCenter(game_server=self, roomId=roomId)
        self.roomIdMaps[roomId] = game
        player.send_msg('您创建房间[%s]成功' % (roomId))
        game.onjoinGame(player)
        game.owner = player
        return game

    def playChess(self, player, msgData, params, *args, **kwargs):
        if not player.game:
            player.send_msg('你不在游戏中')
            return
        player.game.playChess(player, msgData, params, *args, **kwargs)

    def nextGame(self, player, msgData, params, *args, **kwargs):
        if not player.game:
            player.send_msg('你不在游戏中')
            return
        player.game.nextGame(player, msgData, params, *args, **kwargs)

    def login(self, player):
        if player.accountNo in self.gameingPlayer:
            oldPlayer = self.gameingPlayer[player.accountNo]
            oldGame = oldPlayer.game
            oldGame.copyOldPlayer(player, oldPlayer)
            player.send_msg('您还有未继续的游戏,重连房间[%s]' % oldGame.roomId)
            oldGame.doRefreshData(player)


if __name__ == '__main__':
    server = gameServer.instance()
    print(server.createNewGame())
