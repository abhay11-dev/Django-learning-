from django.urls import path
from .views import LoginView, RegisterUserView

urlpatterns = [
    path("register/", RegisterUserView.as_view()),
    path("login/", LoginView.as_view()),
]