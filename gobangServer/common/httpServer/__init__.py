# coding=utf-8

from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from common.wrapper.wrapperFunc import wrapper_allowOrigin_func
from common.basics.baseFunc import *


class IndexHandler(RequestHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


class LoginHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(LoginHandler, self).__init__(*args, **kwargs)
        self.lobbyServer = self.application.lobbyServer

    def laterResetSid(self, sid, delaySec=60):
        IOLoop.current().call_later(delay=delaySec, callback=self.lobbyServer.resetSid, sid=sid)

    @wrapper_allowOrigin_func
    def get(self, *args, **kwargs):
        accountNo = self.get_argument('accountNo', '').strip().replace(' ', '')
        if not accountNo:
            return self.finish({'code': -1, 'msg': '账号名不能为空'})
        sid = createSid(accountNo)
        self.lobbyServer.setSid(datas={'accountNo': accountNo, 'sid': sid}, delaySec=60)
        return self.finish({'code': 0, 'msg': '登录成功', 'data': {'sid': sid, 'ws_address': '/lobby?sid=%s' % (sid)}})
