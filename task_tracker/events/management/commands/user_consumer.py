import json

from confluent_kafka import KafkaException
from django.core.management.base import BaseCommand

from events.consumers import consumer
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        consumer.subscribe(['users'])
        try:
            while True:
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    raise KafkaException(msg.error())
                else:
                    print(
                        f'received event from topic {msg.topic()} partition {msg.partition()} offset {msg.offset()} with data {msg.value()}')
                    data = json.loads(msg.value())
                    match data['event']:
                        case 'created':
                            # TODO: replace get_or_create with create, for debug purposes only
                            User.objects.get_or_create(**data['data'])
                            print('user created!')
                        case 'updated':
                            User.objects.get_or_create(**data['data'])
                            print('user updated!')
                        case _:
                            print(f'unknown event: {data['event']}')

                    # consumer.store_offsets(msg)
        except KeyboardInterrupt:
            print('goodbye!')
        finally:
            # Close down consumer to commit final offsets.
            consumer.close()
