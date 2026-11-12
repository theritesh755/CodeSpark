import pika
from config.settings import settings

def connection():
    return pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
