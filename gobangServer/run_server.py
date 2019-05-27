# coding=utf-8

from common.server import HttpServerMgr
import tornado.options
from tornado.options import define, options

define("address", default='0.0.0.0', type=str, help="run server on the given address.")
define("port", default=5007, type=int, help="run server on the given port.")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = HttpServerMgr(address=options.address, port=options.port)
    http_server.run()
