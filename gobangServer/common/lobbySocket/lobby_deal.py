# coding=utf-8

# tornado
# 标准库
import logging
# 项目引用
from common.lobbySocket.lobby_deal_handler import lobbyDeal_chat, lobbyDeal_rooms, lobbyDeal_users


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
        logging.info(u'注册基础路由[%s] => %s' % (mgrRoute, newActionMap))
        # pprint(u'注册基础路由[%s] => %s' % (mgrRoute, newActionMap))

    def doing(self, player, msgData, *args, **kwargs):
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
            if mgrRoute == 'game':
                self.lobbyServer.gameServer.dealMessage(player, msgData)
            else:
                player.send_msg('指令无效!')
            return
        func, backCode = self.allAction_Deal_Map[mgrRoute][bodyRoute]
        func(backCode=backCode, player=player, params=msgData.get('params', {}), msgData=msgData)
