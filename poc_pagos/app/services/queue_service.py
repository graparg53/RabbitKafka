import pika
import json

class RabbitMQPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='payments_approved')

    def publish(self, document: str, amount: float):
        message = json.dumps({"document": document, "amount": amount})
        self.channel.basic_publish(
            exchange='',
            routing_key='payments_approved',
            body=message
        )
        self.connection.close()