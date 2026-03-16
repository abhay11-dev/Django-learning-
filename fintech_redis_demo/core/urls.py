from django.contrib import admin
from django.urls import path
from wallet.views import redis_test, get_balance

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redis-test/', redis_test),
    path('balance/<int:user_id>/', get_balance),
]