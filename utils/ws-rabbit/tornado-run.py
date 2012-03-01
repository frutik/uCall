#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.websocket as websocket

from tornado.options import define, options

import os.path
import uuid
import time

http_settings = dict(
    cookie_secret=str(uuid.uuid1()),
    xsrf_cookies=False,
    autoescape="xhtml_escape",
)

define("port", default=8888, help="run on the given port", type=int)

import logging
logging.basicConfig(level=logging.INFO)

import pika
from pika_client import PikaClient
from agent_channel_ws import AgentChannelWebSocket

import ConfigParser

config = ConfigParser.ConfigParser()

config.read('/opt/ucall/etc/config.ini')

rabbit_host = config.get('STOMP', 'host')
rabbit_username = config.get('STOMP', 'username')
rabbit_password = config.get('STOMP', 'password')
rabbit_exchange = config.get('STOMP', 'exchange')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', AgentChannelWebSocket),
        ]
        tornado.web.Application.__init__(self, handlers, http_settings)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)

    pc = PikaClient(
        username = rabbit_username,
        password = rabbit_password,
        host = rabbit_host,
        port = 5672,
        virtual_host = '/',
        exchange_name = rabbit_exchange
    )
    pika.log.setup(color=True)

    app.pika = pc

    ioloop = tornado.ioloop.IOLoop.instance()

    # Add our Pika connect to the IOLoop with a deadline in 0.1 seconds
    ioloop.add_timeout(time.time() + .1, app.pika.connect)

    # Start the IOLoop
    ioloop.start()

if __name__ == "__main__":
    main()

