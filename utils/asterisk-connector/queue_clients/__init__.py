class QueueClient(object):

    def __init__(self):
	pass

    def put(self, message, destination='', persistent=False, conf={}):
	print 'Sending message', type(self), destination, message  

class RabbitMqClient(QueueClient):

    def __init__(self, host='127.0.0.1', username=None, password=None, exchange=None):
	#TODO asserts
    
        super(RabbitMqClient, self).__init__()

	import pika

	self.agent_channel = ''
	self.exchange = exchange

	connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = connection.channel()

	
	self.channel.exchange_declare(exchange=self.exchange, type='direct')

    def put(self, message, destination='', persistent=False, conf={}):
        super(RabbitMqClient, self).put(message, destination, persistent, conf)

	self.channel.basic_publish(exchange=self.exchange,
                      routing_key=destination,
                      body=message)

class StompClient(QueueClient):
    
    def __init__(self, host='127.0.0.1', username=None, password=None, exchange=None):
	#TODO asserts

        super(StompClient, self).__init__()

	from stompy.simple import Client

	self.client = Client(host)
	self.client.connect(username, password)
	self.agent_channel = 'jms.queue.msg.'

    def put(self, message, destination='', persistent=False, conf={}):
        super(StompClient, self).put(message, destination, persistent, conf)

	self.client.put(message, destination=destination, persistent=persistent, conf=conf)

    
