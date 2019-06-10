# coding=utf-8

import logging.handlers

fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)


class close_log(object):
    def info(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass


g_logger = None
s_logger = None
e_logger = None

if not g_logger:
    LOG_FILE = 'logs/game.log'
    g_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 8192, encoding='utf-8', backupCount=5)
    g_handler.setFormatter(formatter)
    g_logger = logging.getLogger('game')
    g_logger.addHandler(g_handler)
    g_logger.setLevel(logging.DEBUG)

if not s_logger:
    LOG_FILE = 'logs/server.log'
    s_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 8192, encoding='utf-8', backupCount=5)
    s_handler.setFormatter(formatter)
    s_logger = logging.getLogger('server')
    s_logger.addHandler(s_handler)
    s_logger.setLevel(logging.DEBUG)

if not e_logger:
    LOG_FILE = 'logs/error.log'
    e_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 8192, encoding='utf-8', backupCount=5)
    e_handler.setFormatter(formatter)
    e_logger = logging.getLogger('error')
    e_logger.addHandler(e_handler)
    e_logger.setLevel(logging.DEBUG)
