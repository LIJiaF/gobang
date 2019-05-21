# coding=utf-8

from datetime import datetime
from functools import wraps


###支持跨域
def wrapper_allowOrigin(object):
    class __wrapper__(object):
        def __init__(self, *args, **kwargs):
            super(__wrapper__, self).__init__(*args, **kwargs)
            self.set_header("Access-Control-Allow-Origin", '*')
            self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    return __wrapper__


def wrapper_allowOrigin_func(func):
    wraps(func)

    def __wrapper__(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", '*')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        return func(self, *args, **kwargs)

    return __wrapper__
