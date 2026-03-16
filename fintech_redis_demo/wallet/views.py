from django.http import JsonResponse
from .redis_client import redis_client
import uuid


def redis_test(request):
    redis_client.set("message", "Redis is working")

    value = redis_client.get("message")

    return JsonResponse({
        "redis_value": value
    })


def get_balance(request, user_id):

    key = f"balance:{user_id}"

    balance = redis_client.get(key)

    if balance:
        return JsonResponse({
            "source": "redis_cache",
            "balance": balance
        })

    balance = 5000

    redis_client.setex(key, 60, balance) #set with expiration time of 60 seconds

    return JsonResponse({
        "source": "database",
        "balance": balance
    })

