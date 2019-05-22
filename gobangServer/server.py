# coding=utf-8

import tornado
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from tornado.httpserver import HTTPServer
from wrapperFunc.wrapperApplication import webApplication
import configs
import tornado.options
import tornado.locale
import tornado.ioloop
from tornado.ioloop import IOLoop
import tornado.escape
from tornado.escape import json_decode, json_encode
import logging
from datetime import datetime
import traceback
import time
import uuid
import base64
from lobby.lobby_player import lobbyPlayer
from lobby.lobby_server import lobbyServer
from basics.baseFunc import *
from wrapperFunc.wrapperFunc import *
from games.game_player import gamePlayer


def get_nowtime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


class LoginHandler(RequestHandler):
    lobbyServer = lobbyServer.instance()

    def laterResetSid(self, sid, delaySec=60):
        IOLoop.current().call_later(delay=delaySec, callback=self.lobbyServer.resetSid, sid=sid)

    @wrapper_allowOrigin_func
    def get(self, *args, **kwargs):
        accountNo = self.get_argument('accountNo', '').strip().replace(' ', '')
        if not accountNo:
            return self.finish({'code': -1, 'msg': '账号名不能为空！'})
        sid = createSid(accountNo)
        self.lobbyServer.setSid(datas={'accountNo': accountNo, 'sid': sid}, delaySec=60)
        return self.finish({'code': 0,
                            'msg' : '登录成功',
                            'data': {'sid': sid, 'ws_address': 'ws://192.168.199.66:5006/lobby?sid=%s' % (sid)}
                            })


app = webApplication(handlers=[
    (r"/", IndexHandler),
    (r"/lobby/login", LoginHandler),
    (r"/game/gobang", gamePlayer),
    (r"/lobby", lobbyPlayer),
], **configs.webApplicationSetting)


class HttpServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super(HttpServer, self).__init__(*args, **kwargs)


class HttpServerMgr(object):
    def __init__(self, address, port, *args, **kwargs):
        self.address = address
        self.port = port
        self.RouterHandleMap = []

    def run(self, *args, **kwargs):
        self.httpServer = HTTPServer(app)
        self.httpServer.address = self.address
        self.httpServer.port = self.port
        print("http://%s:%s/" % (self.httpServer.address, self.httpServer.port))
        self.httpServer.listen(port=self.httpServer.port, address=self.httpServer.address)
        tornado.ioloop.IOLoop.current().start()
