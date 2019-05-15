# coding=utf-8

from tornado.web import Application, url
import copy


class webApplication(Application):
    def route(self, routeUrl, initDatas=None, name=None):
        """
        路由注册装饰器
        :param routeUrl: 路由地址
        :param initDatas: 数据会传入到对应的RequestHandler的initialize()方法中
        :param name: 此路由的命名,RequestHandler类可以通过reverse_url(name) 获取路由地址
        :return: 被装饰的函数
        """
        if not initDatas:
            initDatas = {}

        def register(handler):
            """
            :param handler: URL对应的Handler
            :return: Handler
            """
            handler.initDatas = copy.deepcopy(initDatas)
            if name:
                self.add_handlers(".*$", [url(routeUrl, handler, initDatas, name=name)])  # URL和Handler对应关系添加到路由表中
            else:
                self.add_handlers(".*$", [(routeUrl, handler, initDatas)])  # URL和Handler对应关系添加到路由表中
            return handler

        return register
