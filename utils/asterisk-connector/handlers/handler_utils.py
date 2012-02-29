def send_message(stomp, message, agent):
    destination = stomp.agent_channel + agent
    conf = {}
    #TODO: add message expiration
    #conf={"expires":(int(time()) + int(connect(config.get('GENERAL', 'message_ttl'))) * 1000}  
    stomp.put(message, destination=destination, persistent=False, conf=conf)

def get_local_number(channel):
    return channel.split('-')[0]

def check_event(f):
    """Decorator to check wether even is a dict or object"""

    def wrap_f(*args, **kwargs):
        event = None

        if 'event' in kwargs:
            event = kwargs['event']
        elif len(args) > 1:
            event = args[1]

        if event != None and not isinstance(event, dict):
            event = event.headers

        if 'event' in kwargs:
            kwargs['event'] = event
        elif len(args) > 1:
            arglist = list(args)
            arglist[1] = event
            args = tuple(arglist)

        f(*args, **kwargs)

    return wrap_f
