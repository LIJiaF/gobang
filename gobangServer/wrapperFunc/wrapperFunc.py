# coding=utf-8

###支持跨域
def wrapper_allowOrigin(object):
    class __wrapper__(object):
        def __init__(self, *args, **kwargs):
            super(__wrapper__, self).__init__(*args, **kwargs)
            self.set_header("Access-Control-Allow-Origin", '*')
            self.set_header("Access-Control-Allow-Headers", "x-requested-with")
            self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    return __wrapper__
