__author__ = 'mazheng'

import time

from concurrent.futures import ThreadPoolExecutor
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.web import RequestHandler
from tornado.web import asynchronous
from tornado.gen import engine
from tornado.ioloop import IOLoop
from async.core import run_on_executor, run_callback


executor = ThreadPoolExecutor(2)


class HelloHandler(RequestHandler):

    @run_on_executor(executor=executor)
    @run_callback
    def sleep(self, n):
        print 'enter sleep'
        time.sleep(n)
        print 'sleep over'
        return n

    @asynchronous
    @engine
    def get(self):
        res = yield self.sleep(5)
        print 'get res:', res
        self.write('finished')
        self.finish()


handlers = [
    (r"/", HelloHandler),
]


class Application(tornado.web.Application):

    def __init__(self):
        super(Application, self).__init__(handlers, {})


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(9999)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
