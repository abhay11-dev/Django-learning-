from celery import shared_task


@shared_task
def sub(x, y):
    return x - y