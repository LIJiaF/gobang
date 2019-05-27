# coding=utf-8

from common.basics.baseFunc import *


class lobbyDeal_base(object):
    mgrRoute = ''
    actionmMap = {}

    def __init__(self, dealMgr, *args, **kwargs):
        self.dealMgr = dealMgr
        self.actionmMap = self.setActionMap()
        self.__install__()

    def __install__(self, *args, **kwargs):
        if not self.mgrRoute or not self.actionmMap:
            raise Exception("基础路由与路由映射都不能为空!")
        self.dealMgr.installActionMap(self.mgrRoute, self.actionmMap)

    def setActionMap(self):
        return {}

    def getbackUrl(self, backCode):
        return '/%s/%s' % (self.mgrRoute, backCode)


class lobbyDeal_rooms(lobbyDeal_base):
    mgrRoute = 'room'

    def getGameServer(self):
        return self.dealMgr.lobbyServer.gameServer

    def setActionMap(self):
        return {'C_S_getRoomList': [self.C_S_getRoomList, 'S_C_getRoomList'], 'C_S_createGame': [self.C_S_createGame, 'S_C_createGame'],
                'C_S_joinGame': [self.C_S_joinGame, 'S_C_joinGame']}

    def C_S_getRoomList(self, backCode, player, msgData, params, *args, **kwargs):
        data = []
        gameServer = self.getGameServer()
        if not gameServer:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg='获取失败,游戏服务未启动')
            return

        for _roomId, _game in gameServer.roomIdMaps.items():
            data.append({'roomId': _roomId, 'owner': _game.owner.accountNo if _game.owner else '未知', 'playerCount': _game.playerCount, })
        player.send_Datas(url=self.getbackUrl(backCode), data=data, msg='获取成功')

    def C_S_joinGame(self, backCode, player, msgData, params, *args, **kwargs):
        gameServer = self.getGameServer()
        if not gameServer:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg='获取失败,游戏服务未启动')
            return
        roomId = params.get('roomId')
        isRandomRoom = params.get('isRandomRoom', False)
        if not roomId and not isRandomRoom:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg='未选择房间')
            return
        result, backData = gameServer.joinGame(player=player, roomId=roomId, isRandomRoom=isRandomRoom)
        if not result:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg=backData.get('reason', '未知原因'))
            return
        player.send_Datas(url=self.getbackUrl(backCode), data=backData, msg='加入房间成功.')

    def C_S_createGame(self, backCode, player, msgData, params, *args, **kwargs):
        gameServer = self.getGameServer()
        if not gameServer:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg='获取失败,游戏服务未启动')
            return
        roomId = params.get('roomId')
        isJoinIn = params.get('isJoinIn')
        result, backData = gameServer.createGame(player=player, roomId=roomId, isJoinIn=isJoinIn)
        if not result:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg=backData.get('reason', '未知原因'))
            return
        player.send_Datas(url=self.getbackUrl(backCode), data=backData, msg='创建房间成功.')


class lobbyDeal_users(lobbyDeal_base):
    mgrRoute = 'user'

    def setActionMap(self):
        return {'C_S_getOnlineUserList': [self.C_S_getOnlineUserList, 'S_C_getOnlineUserList'], }

    def C_S_getOnlineUserList(self, backCode, player, msgData, params, *args, **kwargs):
        onlinePlayers = self.dealMgr.lobbyServer.onlinePlayers
        data = []
        for _accountNo, _onlinePlayer in onlinePlayers.items():
            data.append(_onlinePlayer.getInfo())
        player.send_Datas(url=self.getbackUrl(backCode), data=data)

    def sendMsgAllOnline(self, sendDatas):
        onlinePlayers = self.dealMgr.lobbyServer.onlinePlayers
        for _accountNo, _onlinePlayer in onlinePlayers.items():
            _onlinePlayer.send_msg(sendDatas)


class lobbyDeal_chat(lobbyDeal_base):
    mgrRoute = 'chat'

    def setActionMap(self):
        return {'C_S_sendMsg_allOnline': [self.C_S_sendMsg_allOnline, 'S_C_sendMsg_allOnline'],
                'C_S_sendMsg_other': [self.C_S_sendMsg_other, 'S_C_sendMsg_other'], }

    def C_S_sendMsg_allOnline(self, backCode, player, msgData, params, *args, **kwargs):
        msg = params.get('msg', '')
        if not msg:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg='需要发送的信息不能为空!')
            return
        player.send_Datas(url=self.getbackUrl(backCode), msg='发送成功.')

        sendDatas = player.send_Datas(url=self.getbackUrl('S_R_sendMsg'), data={'sender': player.getInfo(), 'msg': msg, 'senderTime': strfDataTime()},
                                      isSend=False)
        self.dealMgr.usersMgr.sendMsgAllOnline(sendDatas)

    def C_S_sendMsg_other(self, backCode, player, msgData, params, *args, **kwargs):
        msg = params.get('msg', '')
        otherAccount = params.get('otherAccount', '')
        if not msg:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg='需要发送的信息不能为空!')
            return
        otherPlayer = self.dealMgr.lobbyServer.onlinePlayers.get(otherAccount)
        if not otherPlayer:
            player.send_Datas(url=self.getbackUrl(backCode), code=-1, msg='接收方不存在或不在线!')
            return
        sendDatas = player.send_Datas(url=self.getbackUrl('S_R_sendMsg'),
                                      data={'sender': player.getInfo(), 'receiver': otherPlayer.getInfo(), 'msg': msg}, isSend=False)
        player.send_msg(sendDatas)
        otherPlayer.send_msg(sendDatas)
