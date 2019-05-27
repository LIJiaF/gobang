# coding=utf-8

import tornado
from tornado.httpserver import HTTPServer
from tornado.web import Application
import configs
import tornado.options
import tornado.locale
import tornado.ioloop
import tornado.escape

from common.httpServer import LoginHandler, IndexHandler
from common.lobbySocket.lobby_player import lobbyPlayer
from common.gameSocket.game_player import gamePlayer
from common.lobbySocket.lobby_server import lobbyServer
from common.gameSocket.game_server import gameServer

app = Application(handlers=[(r"/", IndexHandler), (r"/lobby/login", LoginHandler), (r"/game/gobang", gamePlayer), (r"/lobby", lobbyPlayer), ],
        **configs.webApplicationSetting)
app.lobbyServer = lobbyServer()
app.lobbyServer.application = app
app.gameServer = gameServer(app.lobbyServer)
app.gameServer.application = app


class HttpServer(HTTPServer):
    def __init__(self, *args, **kwargs):
        super(HttpServer, self).__init__(*args, **kwargs)


class HttpServerMgr(object):
    def __init__(self, address, port, *args, **kwargs):
        self.address = address
        self.port = port

    def run(self, *args, **kwargs):
        self.httpServer = HTTPServer(app)
        self.httpServer.address = self.address
        self.httpServer.port = self.port
        print("http://%s:%s/" % (self.httpServer.address, self.httpServer.port))
        self.httpServer.listen(port=self.httpServer.port, address=self.httpServer.address)
        tornado.ioloop.IOLoop.current().start()
