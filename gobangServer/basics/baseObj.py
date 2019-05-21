# coding=utf-8

import threading


class Singleton(object):
    _instance_lock = threading.Lock()
    _instance = {}

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(Singleton, "_instance"):
    #         with Singleton._instance_lock:
    #             if not hasattr(Singleton, "_instance"):
    #                 Singleton._instance = object.__new__(cls)
    #     return Singleton._instance

    # @classmethod
    # def instance(cls):
    #     if not hasattr(Singleton, "_instance"):
    #         with Singleton._instance_lock:
    #             if not hasattr(Singleton, "_instance"):
    #                 Singleton._instance = object.__new__(cls)
    #                 Singleton._instance.__init__()
    #     return Singleton._instance

    @classmethod
    def instance(cls):
        className = getattr(cls, '__name__')
        if className not in Singleton._instance:
            with Singleton._instance_lock:
                if className not in Singleton._instance:
                    Singleton._instance[className] = object.__new__(cls)
                    Singleton._instance[className].__init__()
                    print('Singleton._instance => ', Singleton._instance)
        return Singleton._instance[className]
