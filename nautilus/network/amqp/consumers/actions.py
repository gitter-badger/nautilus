import time
from .amqp import AMQPConsumer


class ActionHandler(AMQPConsumer):
    EXCHANGE = 'events'
    EXCHANGE_TYPE = 'topic'
    ROUTING_KEY = '*.*.pending'
    DURABLE = True

    def __init__(self, callback, routing_key, **kwds):
        # save a reference to the callback we were provided
        self._callback = callback
        self.ROUTING_KEY = routing_key
        super().__init__(**kwds)


    def handle_event(self, channel, method, properties, body):
        self._callback(self, channel, method, properties, body)
