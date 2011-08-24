#!/usr/bin/python

import sys, os
import asterisk.manager
import simplejson as json
from stompy.simple import Client
import ConfigParser

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from channel.channel_message import ChannelMessage

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='/tmp/ucall-pbx-listener.log',
                    filemode='a+')

def queue_add(manager, request):
    cdict = {'Action':'QueueAdd'}
    cdict['Interface'] = request['agent']
    cdict['Queue'] = request['queue']
    cdict['Penalty'] = 1
    cdict['Paused'] = False

    return manager.send_action(cdict)

def queue_remove(manager, request):
    cdict = {'Action':'QueueRemove'}
    cdict['Interface'] = request['agent']
    cdict['Queue'] = request['queue']

    return manager.send_action(cdict)

def queue_pause(manager, request, paused = True):
    cdict = {'Action':'QueuePause'}
    cdict['Interface'] = request['agent']
    cdict['Queue'] = request['queue']
    cdict['Paused'] = paused

    return manager.send_action(cdict)

def queue_unpause(manager, request):
    return queue_pause(manager, request, False)

def queue_status(manager, request):
    cdict = {'Action':'QueueStatus'}
    cdict['Queue'] = request['queue']
    cdict['Member'] = request['agent']

    return manager.send_action(cdict)

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

config.read('/opt/ucall/etc/config.ini')

stomp_host = config.get('STOMP', 'host')
stomp_username = config.get('STOMP', 'username')
stomp_password = config.get('STOMP', 'password')
stomp_queue = config.get('STOMP', 'ctrl_channel')


print '='*80
print 'Stomp host:', stomp_host
print 'Stomp username:', stomp_username
print 'Stomp password:', stomp_password
print 'Stomp queue:', stomp_queue
print '='*80


ami_host = config.get('AMI', 'host')
ami_username = config.get('AMI', 'username')
ami_password = config.get('AMI', 'password')

stomp = Client(stomp_host)
stomp.connect(stomp_username, stomp_password)
stomp.subscribe(stomp_queue)

while True:
    message = stomp.get()

    channel_message = ChannelMessage()

    logging.debug(message.body)

    data = channel_message.load_data_json(message.body)

    if data['type'] == channel_message.TYPE_AGENT_STATUS:
        manager = asterisk.manager.Manager()
        manager.connect(ami_host)
        manager.login(ami_username, ami_password)

        if data['statusId'] == 'available':
            response = queue_add(manager, data)
        elif data['statusId'] == 'offline':
            response = queue_remove(manager, data)
        elif data['statusId'] == 'away':
            response = queue_pause(manager, data)

        print response.headers['Message']

        manager.logoff()

    elif data['type'] == channel_message.TYPE_PING:
	#logging.info('ping at %s from %s', (data['id'], data['agent']))
	#TODO hardcoded value
	stomp.put('{"type":"pong"}', destination="jms.queue.msg." + str(data['agent']), persistent=False, conf={})

    elif data['type'] == channel_message.TYPE_CHECK_CURRENT_STATUS:
        manager = asterisk.manager.Manager()
        manager.connect(ami_host)
        manager.login(ami_username, ami_password)

        response = queue_status(manager, data)

        print response.headers

        manager.logoff()


