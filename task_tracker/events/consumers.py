from confluent_kafka import Consumer
from django.conf import settings

consumer_conf = {
    'bootstrap.servers': settings.KAFKA_HOST,
    'group.id': 'tasks_consumer_group',
    'auto.offset.reset': "earliest",
    'enable.auto.offset.store': False,
}

consumer = Consumer(consumer_conf)
