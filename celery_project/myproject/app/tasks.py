from time import sleep
from celery import shared_task


@shared_task
def sub(a,b):
    sleep(10)
    return a-b

    
@shared_task
def clear_session_cache():
    print("Session cache cleared")




