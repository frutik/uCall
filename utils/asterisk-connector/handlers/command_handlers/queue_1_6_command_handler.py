from asterisk_event import AsteriskEvent
from asterisk_command_handler import AsteriskCommandHandler
from command_constants import Asterisk11
from channel.channel_message import ChannelMessage


from handler_utils import check_event
from handler_utils import send_message
from handler_utils import get_local_number

class Queue16CommandHandler(AsteriskCommandHandler):

    def get_commands(self):
        common = super(Queue16CommandHandler, self).get_commands()
        return common + ['Newchannel',
                'Newstate',
                'Join',
                'Bridge',
        ]

#    Join {'Count': '1', 'ConnectedLineNum': 'unknown', 'CallerIDNum': '102', 'Queue': 'test_te', 'ConnectedLineName': 'unknown', 'Uniqueid': '1330721579.24', 'CallerIDName': 'unknown', 'Privilege': 'call,all', 'Position': '1', 'Event': 'Join', 'Channel': 'SIP/102-00000018'}
#    Bridge {'Uniqueid2': '1330721579.25', 'Uniqueid1': '1330721579.24', 'CallerID2': '', 'Bridgestate': 'Link', 'CallerID1': '102', 'Channel2': 'SIP/101-00000019', 'Channel1': 'SIP/102-00000018', 'Bridgetype': 'core', 'Privilege': 'call,all', 'Event': 'Bridge'}

    @check_event
    def handle_Newchannel(self, event, manager):
#        found new caller. we know exten here. store to db
#        Newchannel {'AccountCode': '', 'Uniqueid': '1330721579.24', 'ChannelState': '0', 'Exten': '555', 'CallerIDNum': '102', 'Context': 'default', 'CallerIDName': '', 'Privilege': 'call,all', 'Event': 'Newchannel', 'Channel': 'SIP/102-00000018', 'ChannelStateDesc': 'Down'}

        AsteriskEvent(
            event = event[Asterisk11.HEADER_EVENT],
            raw = str(event),
            uniqueid = event[Asterisk11.HEADER_UNIQUEID]
        )

    @check_event
    def handle_Join(self, event, manager):
#        caller joined queue. we know queue name here. store to db
#        Join {'Count': '1', 'ConnectedLineNum': 'unknown', 'CallerIDNum': '102', 'Queue': 'test_te', 'ConnectedLineName': 'unknown', 'Uniqueid': '1330721579.24', 'CallerIDName': 'unknown', 'Privilege': 'call,all', 'Position': '1', 'Event': 'Join', 'Channel': 'SIP/102-00000018'}

        AsteriskEvent(
            event = event[Asterisk11.HEADER_EVENT],
            raw = str(event),
            uniqueid = event[Asterisk11.HEADER_UNIQUEID]
        )

    @check_event
    def handle_Bridge(self, event, manager):
        """
        Event: Bridge
        Privilege: call,all
        Bridgestate: Link
        Bridgetype: core
        Channel1: SIP/101-00000058
        Channel2: SIP/104-00000059
        Uniqueid1: 1309443548.88
        Uniqueid2: 1309443548.89
        CallerID1: 101
        CallerID2: 104

        {'Uniqueid2': '1309506586.133', 'Uniqueid1': '1309506586.132', 'CallerID2': '104', 'Bridgestate': 'Link', 'CallerID1': '101', 'Channel2': 'SIP/104-00000085', 'Channel1': 'SIP/101-00000084', 'Bridgetype': 'core', 'Privilege': 'call,all', 'Event': 'Bridge'}

        """

        message = ChannelMessage()

        message.set_event(ChannelMessage.EVENT_LINK)
        message.set_id(event[Asterisk11.HEADER_UNIQUEID2])
        message.set_extension(event[Asterisk11.HEADER_CALLERID2])
        message.set_caller(event[Asterisk11.HEADER_CALLERID1])

        send_message(manager.destination, message.dump_data_json(), get_local_number(event[Asterisk11.HEADER_CHANNEL2]))

    def handle_Shutdown(self, event, manager):
        print AsteriskCommandHandler.SHUTDOWN_MESSAGE
        manager.close()

    def _handle_newstate_ringing(self, event, destination):
        #Newstate {
        # 'ConnectedLineNum': '102',
        # 'ChannelState': '5',
        # 'CallerIDNum': '',
        # 'ConnectedLineName': '',
        # 'Uniqueid': '1330721579.25',
        # 'CallerIDName': '',
        # 'Privilege': 'call,all',
        # 'Event': 'Newstate',
        # 'Channel': 'SIP/101-00000019',
        # 'ChannelStateDesc': 'Ringing'}

        channel = event[Asterisk11.HEADER_CHANNEL]

        if channel == None:
            return None

        message = ChannelMessage()

        message.set_event(ChannelMessage.EVENT_RINGING)
        message.set_id(event[Asterisk11.HEADER_UNIQUEID])
#
#        try:
#            parent_event = AsteriskEvent.selectBy(event = Asterisk11.EVENT_DIAL, uniqueid = event[Asterisk11.HEADER_UNIQUEID])[0]
#        except Exception as e:
#            print e
#            parent_event = None
#
#        if parent_event != None:
#            raw = eval(parent_event.raw)
#        else:
#            raw = None
#
#        if raw != None:
#            caller = raw[Asterisk11.HEADER_CALLERIDNUM]
#            extension = event[Asterisk11.HEADER_CALLERIDNUM]
#        else:
#            caller = AsteriskCommandHandler.CALLERID_UNKNOWN
#            extension = AsteriskCommandHandler.CALLERID_UNKNOWN
#
#        message.set_extension(extension)
#        message.set_caller(caller)

#        queue name??? or extension???
#        caller number???

        send_message(destination, message.dump_data_json(), get_local_number(channel))

    def _handle_hangup_clearing(self, event, destination):
        pass
#        print "handle_hangup_clearing"
#        channel = event[Asterisk11.HEADER_CHANNEL]
#
#        if channel == None:
#            return None
#
#        message = ChannelMessage()
#
#        message.set_event(ChannelMessage.EVENT_HANGUP_CLEANUP)
#        message.set_id(event[Asterisk11.HEADER_UNIQUEID])
#
#        send_message(destination, message.dump_data_json(), get_local_number(channel))


    def _is_hangup_clearing(self, event):
        # TODO: Ignore hangup cause for now
        # if event[Asterisk10.HEADER_CAUSE] == Asterisk10.CAUSE_NORMAL_CLEARING:
        return True

        # return False

    def _is_newstate_ringing(self, event):
        if event[Asterisk11.HEADER_CHANNEL_STATE_DESC] == Asterisk11.STATE_RINGING:
            return True

        return False
