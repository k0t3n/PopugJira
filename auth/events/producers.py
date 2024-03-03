import json
from typing import TYPE_CHECKING

from confluent_kafka import Producer
from django.conf import settings

if TYPE_CHECKING:
    from users.models import User

producer = Producer({'bootstrap.servers': settings.KAFKA_HOST})


class AbstractEventProducer:
    topic_name: str

    def __init__(self, *args, **kwargs):
        self._producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def _produce_message(self, event_type: str, data: dict):
        value = json.dumps({'event': event_type, 'data': data})
        self._producer.produce(self.topic_name, value=value)
        self._producer.flush()


class UserEventProducer(AbstractEventProducer):
    topic_name = 'users'

    @staticmethod
    def _serialize_user(user: 'User'):
        return {
            'id': user.id,
            'username': user.username,
            'role': user.role,
        }

    def user_created(self, user: 'User'):
        self._produce_message('created', self._serialize_user(user))

    def user_updated(self, user: 'User'):
        self._produce_message('updated', self._serialize_user(user))

    def user_role_changed(self, user: 'User'):
        # TODO
        ...


user_producer = UserEventProducer()
