import tornado.websocket as websocket
import pika
import uuid
from stompy.frame import Frame

class AgentChannelWebSocket(websocket.WebSocketHandler):
    def open(self):
        pika.log.info('PikaClient: WebSocket opened, Declaring Queue')

        self.queue_name = str(uuid.uuid1()) 

    def parse_headers(self, headers_str):
        """Parse headers received from the servers and convert
        to a :class:`dict`.i

        :param headers_str: String to parse headers from

        """
        # george:constanza\nelaine:benes
        # -> {"george": "constanza", "elaine": "benes"}
	
	headers = {}
	message_raw = headers_str.split("\n")
	for line in message_raw[1:]:
	    tokens = line.split(":")
	    if len(tokens) == 2 and tokens[0]:
		headers[tokens[0].strip()] = tokens[1].strip()

	return headers

    def on_message(self, message):
        pika.log.info('PikaClient: WebSocket got message, TODO send it to somebody?')

        request = Frame()
        c = request.parse_command(message)
	h = self.parse_headers(message)
        
        response = Frame()
        if c == 'CONNECT':
	    response.build_frame({"command": 'CONNECTED', "headers": {}})
	
	elif c == 'SUBSCRIBE':
    	    self.agent_id = str(h['destination'])
    	    pika.log.info(self.agent_id)
    	    self.application.pika.channel.queue_declare(exclusive=True, queue=self.queue_name, callback=self.on_queue_declared)

	    response.build_frame({"command": 'OK', "headers": {}})

	elif c == 'UNSUBSCRIBE':
	    #TODO same as on_close() but not delete queueu????
	    response.build_frame({"command": 'OK', "headers": {}})
	    
        self.write_message(response.as_string())

    def on_close(self):
        pika.log.info('PikaClient: WebSocket closed, TODO cancel consumming stuff')
        
	self.application.pika.channel.queue_unbind(
	    callback=self.on_queue_unbound, 
	    queue=self.queue_name, 
	    exchange=self.application.pika.exchange_name, 
	    routing_key=self.agent_id
	)
	
    def on_queue_unbound(self, method):
	self.application.pika.channel.queue_delete(callback=None, queue=self.queue_name)

    def on_queue_declared(self, frame):
        pika.log.info('PikaClient: Queue Declared, Binding Queue')
        
        self.application.pika.channel.queue_bind(exchange=self.application.pika.exchange_name,
                                queue=self.queue_name,
                                routing_key=self.agent_id,
                                callback=self.on_queue_bound)

    def on_queue_bound(self, frame):
        pika.log.info('PikaClient: Queue Bound, Issuing Basic Consume')

        self.application.pika.channel.basic_consume(consumer_callback=self.on_pika_message,
                                   queue=self.queue_name,
                                   no_ack=True)


    def on_pika_message(self, channel, method, header, body):
	pika.log.info('PikaCient: Message receive, delivery tag #%i' % method.delivery_tag)

        self.write_stomp_message(body)

    def write_stomp_message(self, message):
        self.write_message(self.get_stomp_frame('MESSAGE', body=message).as_string())

    def get_stomp_frame(self, command, headers={}, body=None):
	assert command 
    
        f = Frame()
	f.build_frame({"command": command, "headers": headers, "body": body})

	return f    
