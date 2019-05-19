# coding=utf-8

import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    init_flag = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
        return Singleton._instance

    @classmethod
    def instance(cls):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)
                    Singleton._instance.__init__()
        return Singleton._instance
