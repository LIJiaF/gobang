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
import tornado.escape
from tornado.escape import json_decode, json_encode
import logging
from datetime import datetime
import traceback
import time


def get_nowtime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


class gamePlayer(WebSocketHandler):

    def check_origin(self, origin):
        '''是否允许跨域'''
        return True

    def open(self, sid=None, *args):
        if not sid:
            sid = self.get_argument('sid')
        self.send_msg({'msg': u'欢迎[%s]' % sid})

    def on_message(self, message):
        logging.info("got message %r", message)
        print(type(message))
        print(message)
        try:
            parsed = tornado.escape.json_decode(message)
        except:
            parsed = message
            traceback.print_exc()
        print(parsed)
        try:
            if parsed.get('action') == 'Robot_Play_Chess':
                time.sleep(1)
        except:
            traceback.print_exc()
        self.send_msg(parsed)

    def send_msg(self, msg_data):
        self.write_message(json_encode(msg_data))

    def on_close(self):
        code = self.close_code
        reason = self.close_reason
        print('%s 连接已关闭 code[%s] reason[%s]' % (get_nowtime(), code, reason))

    def write_message(self, message, binary=False):
        super(gamePlayer, self).write_message(message, binary)

    def close(self, code=None, reason=None):
        super(gamePlayer, self).close(code=code, reason=reason)


app = webApplication(handlers=[
    (r"/", IndexHandler),
    (r"/game/(.*)", gamePlayer),
    (r"/game", gamePlayer),
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
