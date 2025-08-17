import pika
from kafka import KafkaProducer
import json

# Configura Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Configura RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='payments_approved')

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"[RabbitMQ] Procesando pago: {data}")
    
    # Envía a Kafka
    producer.send('pedidos', value=data)
    print(f"[Kafka] Enviado pedido: {data}")

channel.basic_consume(
    queue='payments_approved',
    on_message_callback=callback,
    auto_ack=True
)

print("Esperando mensajes de RabbitMQ...")
channel.start_consuming()