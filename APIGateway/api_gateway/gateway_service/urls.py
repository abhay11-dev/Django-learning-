from django.urls import path
from .views import GatewayView

urlpatterns = [
    path("<str:service>/<path:path>", GatewayView.as_view()),
]
