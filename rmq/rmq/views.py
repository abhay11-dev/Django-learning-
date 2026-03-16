from django.shortcuts import render
from django.http import HttpResponse
from .rabbitmq import publish_message

def index(request):
    publish_message("Hello, RabbitMQ!")
    return HttpResponse("Hello, world. You're at the RMQ index.")

