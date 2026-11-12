import json
from messaging.rabbitmq_connection import connection
from messaging.queues import TRACE_QUEUE

def publish_trace(payload):
    conn = connection()
    try:
        channel = conn.channel()
        channel.queue_declare(queue=TRACE_QUEUE, durable=True)
        channel.basic_publish(exchange="", routing_key=TRACE_QUEUE,
            body=json.dumps(payload), properties=__import__("pika").BasicProperties(delivery_mode=2))
    finally:
        conn.close()
