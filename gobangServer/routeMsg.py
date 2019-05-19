# coding=utf-8

wsActionMap = {
    'mgrRoute': {
        'room': {
            'name'     : '房间api',
            'bodyRoute': {
                'getRoomList': {
                    'name': '获取房间列表'
                }
            },
        },
        'user': {
            'name'     : '玩家api',
            'bodyRoute': {
                'getOnlineUserList': {
                    'name': '获取在线玩家列表'
                }
            },
        },
    }
}

'''
{"url":"/chat/sendMsg_allOnline","params":{"msg":"你们好"}}
{"url": "/room/getRoomList"}
{"url": "/user/getOnlineUserList"}
{"url":"/chat/sendMsg_other","params":{"msg":"你们好","otherAccount":"winslen1"}}
'''