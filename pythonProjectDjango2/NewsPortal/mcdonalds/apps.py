from django.apps import AppConfig
import redis


class McdonaldsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mcdonalds'
    verbose_name = 'Макдак'


red = redis.Redis(
    host='redis-14226.c51.ap-southeast-2-1.ec2.cloud.redislabs.com',
    port=14226,
    password='SQgQovYVrRQ85HmXfcqtVYH6wmdhSUar'
)
