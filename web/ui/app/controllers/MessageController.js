/**
 * Route incoming messages
 *
 * @class uCall.controllers.MessageController
 * @extends Ext.util.Observable
 *
 * Message controller.
 */

Ext.define('uCall.controllers.MessageController', {
    requires: ['uCall.constants.MessageEvent'],
    extend: 'Ext.util.Observable',
    singleton: true,

    mappedEvents: channelEventSchema,

    config: {
        onEventLinkCallback: Ext.emptyFn
    },

    handleMessage: function(eventData) {
        var message = Ext.JSON.decode(eventData.message.data.body);

        switch(message.t) {
            
            case this.mappedEvents.EVENT_RINGING:
		        that = this;

                console.log('RINGING');

                UserInfo.getUserInfo(message.c, message.e, function(crm_user_details) {

                    if (crm_user_details.success) {
			            message.content = 'User ' + crm_user_details.user + ' is waiting ... <br> Notes: ' + crm_user_details.title;
		            } else {
			            message.content = 'User ' + message.c + ' is waiting ...';
                	    //message.content = value.msg;
		            }

		            that.fireMappedEvent(message);
		        });

                break;

            case this.mappedEvents.EVENT_LINK:

		        this.fireMappedEvent(message); // show dialog
		        this.fireMappedEvent(message, this.mappedEvents.EVENT_HANGUP_CLEANUP); // hide growl

                break;

            default:
                this.fireMappedEvent(message);
        }
    },

    fireMappedEvent: function(message, override_event_type) {
        if (override_event_type) {
	        event_type = override_event_type;
        } else {
            event_type = message.t;
	    }
	
        event = this.eventsMap[event_type];

        if (event) {
            result = this.fireEvent(event, message);
            console.log('Fired event ' + event + ' - ' + result);
        }
    },

    constructor: function(config) {
        // Merge configs
        Ext.apply(this.config, config);
        Ext.apply(this, this.config);

        // Parent
        this.callParent(arguments);

        this.eventsMap = {};

        this.eventsMap[this.mappedEvents.EVENT_RINGING] =
            uCall.constants.MessageEvent.INCOMING_CALL_RINGING;

        this.eventsMap[this.mappedEvents.EVENT_HANGUP_CLEANUP] =
            uCall.constants.MessageEvent.INCOMING_CALL_HANGUP;

        this.eventsMap[this.mappedEvents.EVENT_LINK] =
            uCall.constants.MessageEvent.INCOMING_CALL_LINK;

        this.eventsMap[this.mappedEvents.EVENT_QUEUE_MEMBER_ADDED] =
            uCall.constants.MessageEvent.STATUS_ONLINE;

        this.eventsMap[this.mappedEvents.EVENT_QUEUE_MEMBER_REMOVED] =
            uCall.constants.MessageEvent.STATUS_OFFLINE;

        this.eventsMap[this.mappedEvents.EVENT_QUEUE_MEMBER_PAUSED] =
            uCall.constants.MessageEvent.STATUS_AWAY;

        // Register events
        this.addEvents(
            uCall.constants.MessageEvent.INCOMING_CALL_RINGING,
            uCall.constants.MessageEvent.INCOMING_CALL_HANGUP,
            uCall.constants.MessageEvent.INCOMING_CALL_LINK
        );
    }
});
