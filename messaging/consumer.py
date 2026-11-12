import json
from messaging.rabbitmq_connection import connection
from messaging.queues import TRACE_QUEUE

def consume(callback):
    conn = connection()
    channel = conn.channel()
    channel.queue_declare(queue=TRACE_QUEUE, durable=True)
    def handler(ch, method, props, body):
        try:
            callback(json.loads(body))
            ch.basic_ack(method.delivery_tag)
        except Exception:
            ch.basic_nack(method.delivery_tag, requeue=False)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=TRACE_QUEUE, on_message_callback=handler)
    channel.start_consuming()
