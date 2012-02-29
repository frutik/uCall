#!/usr/bin/env python
import pika
import sys

import ConfigParser

config = ConfigParser.ConfigParser()

config.read('/opt/ucall/etc/config.ini')

host = config.get('STOMP', 'host')
username = config.get('STOMP', 'username')
password = config.get('STOMP', 'password')
exchange = config.get('STOMP', 'exchange')

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.exchange_declare(exchange=exchange,
                         type='direct')

agent = sys.argv[1] if len(sys.argv) > 1 else '007'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange=exchange,
                      routing_key=agent,
                      body=message)
print " [x] Sent %r:%r" % (agent, message)
connection.close()