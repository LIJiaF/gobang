# coding=utf-8

# tornado
# 标准库
import logging
import functools
# 项目引用
from basics.baseObj import Singleton


class lobbyDeal(object):
    Mgr_Deal_Map = {}
    allAction_Deal_Map = {}

    def __init__(self, lobbyServer, *args, **kwargs):
        self.lobbyServer = lobbyServer
        self.roomsMgr = lobbyDeal_rooms(dealMgr=self)
        self.usersMgr = lobbyDeal_users(dealMgr=self)
        self.chatMgr = lobbyDeal_chat(dealMgr=self)

    def installActionMap(self, mgrRoute, newActionMap):
        if mgrRoute in self.allAction_Deal_Map:
            raise Exception("基础路由[%s]已被注册!" % (mgrRoute))
        self.allAction_Deal_Map[mgrRoute] = newActionMap
        logging.info(u'注册基础路由[%s]' % mgrRoute)

    def doing(self, player, msgData, *args, **kwargs):
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
        if bodyRoute not in self.allAction_Deal_Map[mgrRoute]:
            player.send_msg('指令无效')
            return
        func = self.allAction_Deal_Map[mgrRoute][bodyRoute]
        func(player=player, routeUrl=routeUrl, params=msgData.get('data', {}), msgData=msgData)


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


class lobbyDeal_users(lobbyDeal_base):
    mgrRoute = 'user'

    def setActionMap(self):
        return {
            'getOnlineUserList': self.getOnlineUserList,
        }

    def getOnlineUserList(self, player, routeUrl, msgData, *args, **kwargs):
        onlinePlayers = self.dealMgr.lobbyServer.onlinePlayers
        data = []
        for _accountNo, _onlinePlayer in onlinePlayers.items():
            data.append(_onlinePlayer.getInfo())
        player.send_Datas(
                url=routeUrl,
                data=data)

    def sendMsgAllOnline(self, sendDatas):
        onlinePlayers = self.dealMgr.lobbyServer.onlinePlayers
        for _accountNo, _onlinePlayer in onlinePlayers.items():
            _onlinePlayer.send_msg(sendDatas)


class lobbyDeal_chat(lobbyDeal_base):
    mgrRoute = 'chat'

    def setActionMap(self):
        return {
            'sendMsg_allOnline': self.sendMsg_allOnline,
            'sendMsg_other'    : self.sendMsg_other,
        }

    def sendMsg_allOnline(self, player, routeUrl, msgData, *args, **kwargs):
        params = msgData.get('params', {})
        msg = params.get('msg', '')
        if not msg:
            player.send_Datas(
                    url=routeUrl,
                    code=-1,
                    msg='需要发送的信息不能为空')
            return
        sendDatas = player.send_Datas(
                url=routeUrl,
                data={'sender': player.getInfo(), 'msg': msg},
                isSend=False)
        self.dealMgr.usersMgr.sendMsgAllOnline(sendDatas)

    def sendMsg_other(self, player, routeUrl, msgData, *args, **kwargs):
        params = msgData.get('params', {})
        msg = params.get('msg', '')
        otherAccount = params.get('otherAccount', '')
        if not msg:
            player.send_Datas(
                    url=routeUrl,
                    code=-1,
                    msg='需要发送的信息不能为空')
            return
        otherPlayer = self.dealMgr.lobbyServer.onlinePlayers.get(otherAccount)
        if not otherPlayer:
            player.send_Datas(
                    url=routeUrl,
                    code=-1,
                    msg='接收方不存在或不在线')
            return
        sendDatas = player.send_Datas(
                url=routeUrl,
                data={'sender': player.getInfo(), 'receiver': otherPlayer.getInfo(), 'msg': msg},
                isSend=False)
        player.send_msg(sendDatas)
        otherPlayer.send_msg(sendDatas)


class lobbyDeal_rooms(lobbyDeal_base):
    mgrRoute = 'room'

    def __init__(self, *args, **kwargs):
        self.rooms = []
        self.roomsDict = {}
        super(lobbyDeal_rooms, self).__init__(*args, **kwargs)

    def setActionMap(self):
        return {
            'getRoomList': self.getRoomList,
        }

    def getRoomList(self, player, routeUrl, msgData, *args, **kwargs):
        print(player)
        print(msgData)
        print(args)
        print(kwargs)
        player.send_Datas(url=routeUrl, data=[])
