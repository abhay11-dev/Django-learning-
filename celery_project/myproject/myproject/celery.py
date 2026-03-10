import os
from time import sleep
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def add(x, y):
    sleep(20)
    return x + y


app.conf.beat_schedule = {
    'clear-session-cache-every-10-seconds': {
        'task': 'app.tasks.clear_session_cache',
        'schedule': 10.0,
    }
}