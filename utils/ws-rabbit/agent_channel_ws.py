import tornado.websocket as websocket
import pika
import uuid
from stomp import StompFrame

class AgentChannelWebSocket(websocket.WebSocketHandler):
    def open(self):
        pika.log.info('Websocket: Connection established')

        self.queue_name = str(uuid.uuid1()) 

        self.agent_id = None
        self.subscription_id = None

    def on_message(self, message):
        pika.log.info('Websocket: Got message from browser')

        request = StompFrame()
        request.from_string(message)

        pika.log.info('Websocket: Stomp ' + request.command)

        if request.is_connect():
            response = StompFrame.connected()

        elif request.is_subscribe():

            self.agent_id = '/'.join(request.get_header('destination').split('/')[1:])
            self.subscription_id = request.get_header('id')

            pika.log.debug(self.agent_id)
            self.application.pika.channel.queue_declare(exclusive=True, queue=self.queue_name, callback=self.on_queue_declared)

            response = StompFrame.ok()

        elif request.is_unsubscribe():
            #TODO same as on_close() but not delete queueu????
            response = StompFrame.ok()

        elif request.is_send():
            pika.log.info('Websocket: Not implemented')
            pika.log.debug(request.body)

            response = StompFrame.ok()

        else:
            pika.log.info('Websocket: Unknown command')
            response = StompFrame.error()

        self.write_message(response.as_string())

    def on_close(self):
        pika.log.info('Websocket: WebSocket closed, Canceling consumming stuff')
        
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
        pika.log.info('PikaCient: Got message from brocker, delivery tag #%i' % method.delivery_tag)

        response = StompFrame.message(
            message=body,
            headers = {'subscription': self.subscription_id}
        )

        self.write_message(response.as_string())
