#!/usr/bin/env python
# vim: set expandtab shiftwidth=4:
# http://www.voip-info.org/wiki/view/asterisk+manager+events

import asterisk.manager
import sys,os,time
import simplejson as json
from stompy.simple import Client
import ConfigParser
from sqlobject import *
from handlers.command_handler_factory import CommandHandlerFactory
from handlers.command_constants import Protocol

#sys.stdout = open("/var/log/requests/connector2.log","a")
#sys.stderr = open("/var/log/requests/connector-err2.log","a")

#import logging

#logging.basicConfig(level=logging.INFO,
#                    format='%(asctime)s %(levelname)-8s %(message)s',
#                    datefmt='%a, %d %b %Y %H:%M:%S',
#                    filename='/tmp/myapp.log',
#                    filemode='a+')


class MessageController(object):

    def start_ringing(self):
        pass

    def stop_ringing(self):
        pass

    def link(self):
        pass


import fcntl
lockfile = os.path.normpath('/tmp/' + os.path.basename(__file__) + '.lock')
exclusive_lock = open(lockfile, 'w')
try:
    fcntl.lockf(exclusive_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
except IOError:
    print "Another instance is already running, quitting."
    time.sleep(1)
    sys.exit(-1)

config = ConfigParser.ConfigParser()
config.read('/etc/ucall/config.ini')

stomp_host = config.get('STOMP', 'host')
stomp_username = config.get('STOMP', 'username')
stomp_password = config.get('STOMP', 'password')
stomp_exchange = config.get('STOMP', 'exchange')

print '='*80
print 'Stomp host:', stomp_host
print 'Stomp username:', stomp_username
print 'Stomp password:', stomp_password
print 'Stomp exchange:', stomp_exchange
print '='*80

ami_host = config.get('AMI', 'host')
ami_username = config.get('AMI', 'username')
ami_password = config.get('AMI', 'password')

print 'AMI host:', ami_host
print 'AMI username:', ami_username
print 'AMI password:', ami_password
print '='*80

sql_dsn = config.get('SQL', 'dsn')

print 'SQL:', sql_dsn
print '='*80

connection = connectionForURI(sql_dsn)
sqlhub.processConnection = connection

try:
    AsteriskEvent.createTable()

except:
    pass

from queue_clients import RabbitMqClient as Client

#stomp.agent_channel = 'jms.queue.msg.'
queue_client = Client(
    host=stomp_host,
    username=stomp_username,
    password=stomp_password,
    exchange=stomp_exchange
)

manager = asterisk.manager.Manager()

#try:
#try:
manager.connect(ami_host)
manager.login(ami_username, ami_password)
manager.destination = queue_client

asteriskProtocolVersion = None
if manager.version == '1.0':
    asteriskProtocolVersion = Protocol.ASTERISK_1_0
elif manager.version == '1.1':
    asteriskProtocolVersion = Protocol.ASTERISK_1_1
else:
    sys.exit()

#command_handler = CommandHandlerFactory.create_command_handler_by_protocol(asteriskProtocolVersion)
command_handler = CommandHandlerFactory.create_command_handler_by_key(Protocol.QUEUE_1_6)

print type(command_handler)

for command in command_handler.get_commands():
    print 'Binding', command
    manager.register_event(command, getattr(command_handler, 'handle_' + command))

manager.message_loop()

manager.logoff()

#except asterisk.manager.ManagerSocketException, (errno, reason):
#    print "Error connecting to the manager: %s" % reason

#except asterisk.manager.ManagerAuthException, reason:
#    print "Error logging in to the manager: %s" % reason

#except asterisk.manager.ManagerException, reason:
#    print "Error: %s" % reason

#except:
#    sys.exit()

#finally:
manager.close()
