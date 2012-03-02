#!/usr/bin/env python
# vim: set expandtab shiftwidth=4:
# http://www.voip-info.org/wiki/view/asterisk+manager+events

import asterisk.manager
import sys,time
import urllib
import ConfigParser

def getLocalNumber(channel):
    return channel.split('-')[0]

def handle_shutdown(event, manager):
    print "Recieved shutdown event"
    manager.close()
    # we could analize the event and reconnect here
      
def handle_link(event, manager):
    print "Incomming answered - %s - %s - %s" % (event.get_header('Uniqueid1'), event.get_header('CallerID1'), getLocalNumber(event.get_header('Channel2')))

    try:
	curs.execute("INSERT INTO conversation (uniqueid, caller, agent) VALUES (%s,%s,%s)", (event.get_header('Uniqueid1'), event.get_header('CallerID1'), getLocalNumber(event.get_header('Channel2'))))
    except psycopg2.IntegrityError:
	pass
     
    except Exception, err:
	sys.stderr.write('ERROR: %s\n' % str(err))
         
    conn.commit()
	
def handle_unlink(event, manager):
    print "Incomming terminated - %s - %s - %s" % (event.get_header('Uniqueid1'), event.get_header('CallerID1'), getLocalNumber(event.get_header('Channel2')))

    try:
	curs.execute("UPDATE conversation SET terminated = now() WHERE uniqueid = %s;", (event.get_header('Uniqueid1'),))
     
    except Exception, err:
	sys.stderr.write('ERROR: %s\n' % str(err))

    conn.commit()

def handle_test(event, manager):
    print event, event.headers

config = ConfigParser.ConfigParser()
config.read('/etc/ucall/config.ini')

ami_host = config.get('AMI', 'host')
ami_username = config.get('AMI', 'username')
ami_password = config.get('AMI', 'password')

print 'AMI host:', ami_host
print 'AMI username:', ami_username
print 'AMI password:', ami_password
print '='*80

manager = asterisk.manager.Manager()

manager.connect(ami_host) 
manager.login(ami_username, ami_password)

#manager.register_event('Shutdown', handle_shutdown) # shutdown
#manager.register_event('Link', handle_link)
#manager.register_event('Unlink', handle_unlink)
manager.register_event('*', handle_test)
           
manager.message_loop()

manager.logoff()
