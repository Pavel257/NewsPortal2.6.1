import redis
from django.apps import AppConfig


red = redis.Redis(
    host='redis-14226.c51.ap-southeast-2-1.ec2.cloud.redislabs.com',
    port=14226,
    password='SQgQovYVrRQ85HmXfcqtVYH6wmdhSUar'
)


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    verbose_name = 'Новости'

    def ready(self):
        # noinspection PyUnresolvedReferences
        import news.signals






