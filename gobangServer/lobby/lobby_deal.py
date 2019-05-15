# coding=utf-8

# tornado
# 标准库
import logging
import functools
# 项目引用
from basics.baseObj import Singleton


class lobbyDeal(object):
    Action_Deal_Map = {}

    def __init__(self, *args, **kwargs):
        self.roomMgr = lobbyDeal_room(self)

    def installActionMap(self,newActionMap):
        self.Action_Deal_Map.update(newActionMap)

    @classmethod
    def route(cls,routeUrl):
        def register(handler):
            logging.info(u'[route] %s => %s'%(routeUrl,handler.__name__))
            return handler
        return register

    def doing(self, player, msgData, *args, **kwargs):
        routeUrl = msgData.get(u'url')
        if routeUrl not in self.Action_Deal_Map:
            player.send_msg(u'指令不存在')
            return
        func = self.Action_Deal_Map[routeUrl]
        func(player=player, msgData=msgData)

class lobbyDeal_room(object):

    def __init__(self, dealMgr, *args, **kwargs):
        self.dealMgr = dealMgr
        self.rooms = []
        self.roomsDict = {}
        # self.install()

    def install(self):
        clsNames = dir(lobbyDeal_room)
        for _clsName in clsNames:
            if '__' in _clsName:
                continue
            cls = getattr(lobbyDeal_room, _clsName)
            if isinstance(cls, type) and hasattr(cls, 'RouteUrl') and cls.RouteUrl:
                cls_FuncNames = dir(cls)
                for _method in ['get', 'post', 'put', 'delect', 'options']:
                    if _method in cls_FuncNames:
                        func = getattr(cls, _method)
                        print('[%s] => %s' % (_method, func.__name__))
                        print(func())
        # self.dealMgr.installActionMap()

    def __install__(self,route):
        return

    class Route_RoomList(object):
        RouteUrl = u'/room/roomList'
        def __init__(self):
            pass

        @staticmethod
        def get(*args,**kwargs):
            print('123')

    @lobbyDeal.route('/room/getRoomList')
    def getRoomList(self, player, msgData, *args, **kwargs):
        result = {'url':'/room/getRoomList','data':[]}
        player.send_msg(result)
#
# names = dir(lobbyDeal_room)
# print(names)
# for _name in names:
#     if _name in ['__class__']:
#         continue
#     cls = getattr(lobbyDeal_room, _name)
#     print(_name)
#     print(cls)
#     print(isinstance(cls, type))
#     if isinstance(cls, type) and hasattr(cls,'RouteUrl') and cls.RouteUrl:
#         print('yes')
#
#         cls_FuncNames = dir(cls)
#         for _method in ['get','post','put','delect','options']:
#             if _method in cls_FuncNames:
#                 func = getattr(cls, _method)
#                 print('[%s] => %s'%(_method,func.__name__))
#
#
#
#     print('-'*50)
