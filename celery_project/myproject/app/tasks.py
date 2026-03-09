from time import sleep
from celery import shared_task

@shared_task
def sub(a,b):
    sleep(10)
    return a-b

    