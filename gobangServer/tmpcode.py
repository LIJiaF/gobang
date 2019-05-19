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