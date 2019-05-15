# coding=utf-8

import os

webApplicationSetting = {
    'autoreload'             : False,
    'debug'                  : True,
    'serve_traceback'        : True,
    # 跨站请求伪造(防护)
    'xsrf_cookies'           : True,
    # 如果是 False 模板将会在每次请求重新编译
    'compiled_template_cache': False,
    'static_path'            : os.path.join(os.path.dirname(__file__), ".\\static"),
    'template_path'          : os.path.join(os.path.dirname(__file__), ".\\template"),
    # 如果是 False 静态url将会在每次请求重新计算
    'static_hash_cache'      : True,
    # 静态文件的Url前缀
    'static_url_prefix'      : '/static/',
    # authenticated 装饰器将会重定向到这个url 如果该用户没有登陆
    'login_url'              : '/login',
    # 给cookies签名
    'cookie_secret'          : 'bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=',
}

Configs = {
    'redis'   : {
        'host'    : '127.0.0.1',
        'port'    : 6379,
        'password': '',
        'dbNum'   : 1,
    },
    'language': {
        'default': 'zh_CN',
    }
}
