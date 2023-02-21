import os

from celery import Celery

broker = os.environ.get('BROKER_URL')
app = Celery(
    'module_celery',
    broker=broker,
    include=['module_celery.tasks'],
    backend='db+sqlite:///results.db',
)
