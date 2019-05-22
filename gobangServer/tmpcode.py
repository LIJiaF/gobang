# coding=utf-8

def install(self):
    clsNames = dir(lobbyDeal_room)
    print(clsNames)
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

class gamePlayer(WebSocketHandler):

    def check_origin(self, origin):
        '''是否允许跨域'''
        return True

    def open(self, sid=None, *args):
        if not sid:
            sid = self.get_argument('sid')
        self.send_msg({'msg': '欢迎[%s]' % sid})

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