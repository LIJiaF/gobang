# coding=utf-8

import random
import logging
from pprint import pprint

from .game_center import gameCenter, baseGameCenter
from .game_logger import s_logger
from common.basics.baseFunc import *
from common.lobbySocket.lobby_player import lobbyPlayer


class baseGameServer(object):
    lobbyServer = None
    games = []
    roomIdMaps = {}  # 房间号:房间类
    gameingPlayer = {}  # 玩家accountNo:当前的玩家类
    allAction_Deal_Map = {}

    def __init__(self, lobbyServer, *args, **kwargs):
        self.lobbyServer = lobbyServer
        self.setActionMap()
        self.lobbyServer.gameServer = self

    def getGameCenter(self, roomId):
        return baseGameCenter(game_server=self, roomId=roomId)

    def setActionMap(self):
        self.allAction_Deal_Map.setdefault('game', {})
        self.allAction_Deal_Map['game'].update({'C_S_exitGame': [self.C_S_exitGame, 'S_C_exitGame']})

    def logger(self, msg, level='info'):
        logging.info('[%s] %s' % (get_nowtime(), msg))

    def getRoomId(self, tryCount=100):
        UsedRoomId = self.roomIdMaps.keys()
        while tryCount:
            roomId = str(random.randint(100000, 999999))
            if roomId not in UsedRoomId:
                return roomId
        return None

    def ifPlayerInGame(self, player):
        accountNo = player.accountNo
        if accountNo in self.gameingPlayer:
            return True
        return False

    def getGamePlayerByLobbyPlayer(self, newGamePlayer, lobbyPlayer):
        newGamePlayer.accountNo = lobbyPlayer.accountNo
        newGamePlayer.ip = lobbyPlayer.ip
        newGamePlayer.port = lobbyPlayer.port
        newGamePlayer.loginTime = lobbyPlayer.loginTime
        return newGamePlayer

    def dealMessage(self, player, msgData, *args, **kwargs):
        routeUrl = msgData.get('url')
        if not routeUrl:
            player.send_msg('指令无效!')
            return
        urlsList = list(filter(None, routeUrl.split('/')))
        if len(urlsList) < 2:
            player.send_msg('指令无效!')
            return
        mgrRoute = urlsList[0]
        bodyRoute = '/'.join(urlsList[1:])
        if mgrRoute not in self.allAction_Deal_Map or bodyRoute not in self.allAction_Deal_Map[mgrRoute]:
            player.send_msg('指令无效!')
            return
        func, backCode = self.allAction_Deal_Map[mgrRoute][bodyRoute]
        func(backCode=backCode, player=player, params=msgData.get('params', {}), msgData=msgData)

    def createGame(self, player, roomId=None, isJoinIn=False):
        assert isinstance(player, lobbyPlayer)
        if roomId and roomId in self.roomIdMaps.keys():
            player.send_msg('房间号已被使用!')
            return False, {'reason': '房间号已被使用!'}
        roomId = self.getRoomId()
        if not roomId:
            player.send_msg('房间号获取失败!')
            return False, {'reason': '房间号获取失败!'}
        game = self.getGameCenter(roomId=roomId)
        self.roomIdMaps[roomId] = game
        if isJoinIn:
            newGamePlayer = game.getNewPlayer(player)
            newGamePlayer = self.getGamePlayerByLobbyPlayer(newGamePlayer, player)
            game.onjoinGame(newGamePlayer)
        return True, {'roomId': roomId, 'wsAddress': self.getCurWsAddress(player=player)}

    def joinGame(self, player, roomId, isRandomRoom=False):
        assert isinstance(player, lobbyPlayer)
        if not roomId and not isRandomRoom:
            player.send_msg('未选择房间!')
            return False, {'reason': '未选择房间!'}

        if self.ifPlayerInGame(player):
            player.send_msg('你已在游戏中!')
            return False, {'reason': '你已在游戏中!'}

        if not roomId and isRandomRoom:
            notFullGames = self.getCurNotFullGame()
            if not notFullGames:
                return False, {'reason': '当前可用房间已全满!'}
            game = random.choice(notFullGames)
            roomId = game.roomId
        else:
            game = self.roomIdMaps.get(roomId)
        if not game:
            player.send_msg('房间不存在!')
            return False, {'reason': '房间不存在!'}
        newGamePlayer = game.getNewPlayer(player)
        newGamePlayer = self.getGamePlayerByLobbyPlayer(newGamePlayer, player)
        game.onjoinGame(newGamePlayer)
        return True, {'roomId': roomId, 'wsAddress': self.getCurWsAddress(player=newGamePlayer)}

    def getCurNotFullGame(self):
        notFullGames = []
        for _roomId, _game in self.roomIdMaps.items():
            if _game.playerCount < _game.maxPlayerCount:
                notFullGames.append(_game)
        return notFullGames

    def C_S_exitGame(self, backCode, player, msgData, params, *args, **kwargs):
        if not player.game:
            player.send_msg('你不在游戏中')
            return
        player.game.tryExitGame(player)

    def getCurWsAddress(self, player):
        return '/game/gobang?accountNo=%s' % player.accountNo

    def login(self, player):
        if player.accountNo in self.gameingPlayer:
            oldPlayer = self.gameingPlayer[player.accountNo]
            oldGame = oldPlayer.game
            oldGame.copyOldPlayer(player, oldPlayer)
            player.send_msg('您还有未继续的游戏,重连房间[%s]' % oldGame.roomId)
            oldGame.doRefreshData(player)


class gameServer(baseGameServer):

    def __init__(self, *args, **kwargs):
        super(gameServer, self).__init__(*args, **kwargs)

    def logger(self, msg, level='info'):
        s_logger.info('[%s] %s' % (get_nowtime(), msg))

    def setActionMap(self):
        super(gameServer, self).setActionMap()
        self.allAction_Deal_Map.setdefault('game', {})
        self.allAction_Deal_Map['game'].update({'C_S_playChess': [self.C_S_playChess, None], 'C_S_nextGame': [self.C_S_nextGame, None]})
        pprint(self.allAction_Deal_Map)

    def getGameCenter(self, roomId):
        return gameCenter(game_server=self, roomId=roomId)

    def C_S_playChess(self, backCode, player, msgData, params, *args, **kwargs):
        if not player.game:
            player.send_msg('你不在游戏中')
            return
        player.game.playChess(backCode, player, msgData, params, *args, **kwargs)

    def C_S_nextGame(self, backCode, player, msgData, params, *args, **kwargs):
        if not player.game:
            player.send_msg('你不在游戏中')
            return
        player.game.nextGame(player, msgData, params, *args, **kwargs)
