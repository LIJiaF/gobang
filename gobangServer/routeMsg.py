# coding=utf-8

class room_Example(object):
    '''房间api'''
    mgrRoute = 'room'

    def C_S_getRoomList(self):
        '''获取房间列表'''
        caseData = {"url": "/room/C_S_getRoomList"}
        actionBack = self.S_C_getRoomList
        broadcast = None

    def S_C_getRoomList(self):
        '''返回房间列表'''
        caseData = {"url": "/room/S_C_getRoomList"}

    def C_S_joinGame(self):
        '''加入特定房间'''
        caseData1 = {"url": "/room/C_S_joinGame", "params": {"roomId": "123456"}}
        caseData2 = {"url": "/room/C_S_joinGame", "params": {"isRandomRoom": True}}
        params = {'roomId': '房间ID', 'isRandomRoom': '是否随机加入未满房间(roomId为空是检测)', }
        actionBack = self.S_C_getRoomList
        broadcast = None

    def S_C_joinGame(self):
        '''返回房间列表'''
        caseData = {"url": "/room/S_C_joinGame", "code": 0, "msg": "加入成功"}
        errData1 = {"url": "/room/S_C_joinGame", "code": -1, "msg": "未选择房间!"}
        errData2 = {"url": "/room/S_C_joinGame", "code": -1, "msg": "你已在游戏中!"}

    def C_S_createGame(self):
        caseData = {"url": "/room/C_S_createGame", "params": {"isJoinIn": False}}
        params = {'isJoinIn': '创建成功后是否自动加入'}
        actionBack = self.S_C_createGame
        broadcast = None

    def S_C_createGame(self):
        caseData = {"url": "/room/S_C_createGame", "code": 0, "msg": "创建房间成功."}

class user_Example(object):
    '''玩家api'''
    mgrRoute = 'user'

    def C_S_getOnlineUserList(self):
        '''发送信息给大厅在线玩家'''
        caseData = {"url": "/user/C_S_getOnlineUserList"}
        actionBack = self.S_C_sendMsg_allOnline
        broadcast = None

    def S_C_sendMsg_allOnline(self):
        '''返回操作结果'''
        caseData = {"url": "/user/S_C_getOnlineUserList",
                    "data": [{"accountNo": "winslen", "loginTime": "2019-05-27 21:57:10", "ip": "192.168.199.66"}], "dataType": "list", "code": 0,
                    "msg": ""}


class chat_Example(object):
    '''聊天api'''
    mgrRoute = 'chat'

    def C_S_sendMsg_allOnline(self):
        '''发送信息给大厅在线玩家'''
        caseData = {"url": "/chat/C_S_sendMsg_allOnline", "params": {"msg": "你们好"}}
        actionBack = self.S_C_sendMsg_allOnline
        broadcast = self.S_R_sendMsg

    def S_C_sendMsg_allOnline(self):
        '''返回操作结果'''
        caseData = {"url": "/chat/S_C_sendMsg_allOnline", "code": 0, "msg": "发送成功."}
        errData = {"url": "/chat/S_C_sendMsg_allOnline", "code": -1, "msg": "需要发送的信息不能为空!"}

    def C_S_sendMsg_other(self):
        '''发送信息给某个在线玩家'''
        caseData = {"url": "/chat/C_S_sendMsg_other", "params": {"msg": "你们好", "otherAccount": "winslen1"}}
        actionBack = self.S_C_sendMsg_other
        broadcast = self.S_R_sendMsg

    def S_C_sendMsg_other(self):
        caseData = {"url": "/chat/S_C_sendMsg_other", "code": 0, "msg": "发送成功."}
        errData = [{"url": "/chat/S_C_sendMsg_other", "code": -1, "msg": "需要发送的信息不能为空!"},
                   {"url": "/chat/S_C_sendMsg_other", "code": -1, "msg": " 接收方不存在或不在线!"}]

    def S_R_sendMsg(self):
        '''广播聊天信息'''
        caseData1 = {"url": "/chat/S_R_sendMsg",
                     "data": {"sender": {"accountNo": "winslen", "loginTime": "2019-05-27 21:57:10", "ip": "192.168.199.66"}, "msg": "你们好",
                              "senderTime": "2019-05-27 21:57:13"}, "dataType": "dict", "code": 0, "msg": ""}
        caseData2 = {"url": "/chat/S_R_sendMsg",
                     "data": {"sender": {"accountNo": "winslen", "loginTime": "2019-05-27 21:57:10", "ip": "192.168.199.66"},
                              "receiver": {"accountNo": "winslen1", "loginTime": "2019-05-27 22:19:31", "ip": "192.168.199.66"}, "msg": "你们好"},
                     "dataType": "dict", "code": 0, "msg": ""}
