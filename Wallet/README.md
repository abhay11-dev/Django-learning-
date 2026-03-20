Client
   |
DRF API (Django)
   |
   |--- PostgreSQL (wallet, ledger)
   |
   |--- Redis (cache, idempotency, rate limit)
   |
   |--- RabbitMQ (message broker)
             |
           Celery
             |
       Celery Workers
             |
      Async Tasks





A Digital Wallet Service with async processing.

Features:
User Registration
Wallet Creation (automatic)
Add Money
Transfer Money
Ledger Entries
Transaction Status Tracking
Async Tasks using Celery
Notifications (email / webhook)
Fraud Check simulation
Periodic Reconciliation Jobs





RabbitMQ is a message broker implementing AMQP protocol.
We deploy it as a Docker container exposing port 5672 for messaging and 15672 for management UI.
Celery uses RabbitMQ as a broker to enqueue asynchronous tasks which are consumed by Celery workers, enabling scalable background job processing.





Complete Steps to Integrate Celery in a Django Project
Step 1 — Install Dependencies:
First install required packages: pip install celery redis django-celery-results
You already installed Redis and RabbitMQ, which is good.



Step 2 — Create Celery Configuration
Create this file: config/celery.py

Example:
import os
from celery import Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
app = Celery("wallet_service")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

This file:
Creates Celery application
Loads Django settings
Discovers tasks automatically



Step 3 — Load Celery When Django Starts
Edit: config/__init__.py
Add:
from .celery import app as celery_app
__all__ = ("celery_app",)

This ensures:
Celery loads when Django starts
Step 4 — Configure Celery in Django Settings

In:
config/settings.py

Add:
CELERY_BROKER_URL = "amqp://guest:guest@localhost:5672//"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

Meaning:
RabbitMQ → task broker
Redis → result storage
Step 5 — Run Infrastructure Services

Start Redis:
docker run -d -p 6379:6379 redis

Start RabbitMQ:
docker run -d \
--hostname rabbit \
--name rabbitmq \
-p 5672:5672 \
-p 15672:15672 \
rabbitmq:3-management

Now your infrastructure is ready.

Step 6 — Create Tasks
Inside any Django app create:
tasks.py

Example:
apps/wallet/tasks.py

Example task:
from celery import shared_task
@shared_task
def add(x, y):
    return x + y

Celery will automatically detect this because of:
app.autodiscover_tasks()

Step 7 — Start Celery Worker
Run worker in a new terminal:
celery -A config worker -l info

Worker will show registered tasks like:
[tasks]
 . apps.wallet.tasks.add
Step 8 — Trigger Task

From Django shell:
python manage.py shell

Then:
from apps.wallet.tasks import add
add.delay(4,6)
This sends the task to RabbitMQ.



Step 9 — Task Execution Flow
Complete runtime flow:

Django API / Shell
       │
       │ add.delay()
       ▼
RabbitMQ (Broker)
       │
       ▼
Celery Worker
       │
       │ executes task
       ▼
Redis (Result Backend)
       │
       ▼
Django retrieves result



Step 10 — Optional Result Retrieval

Example:
result = add.delay(4,6)
result.get()

Celery will fetch result from Redis.
Terminals Needed During Development

Usually you run 3 terminals:

Terminal 1 — Django Server
python manage.py runserver
Terminal 2 — Celery Worker
celery -A config worker -l info
Terminal 3 — Infrastructure (Docker)

Redis + RabbitMQ running.









Create celery.py
↓
Configure Celery + Redis + RabbitMQ in settings
↓
Run Redis and RabbitMQ (docker)
↓
Create tasks.py inside apps
↓
Start Celery worker
↓
Call tasks using .delay()
↓
Worker picks task from RabbitMQ
↓
Executes task
↓
Stores result in Redis






#Channels:

Install channels: pip install channels channels_redis
config settings.py : Installed apps, asgi, channel layers
