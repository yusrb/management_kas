from django.urls import path
from .views import (
  UserRegisterView,
  LoginView,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/' , UserRegisterView.as_view() , name="register"),
    path('login/' , LoginView.as_view() , name="login"),
    path('logout/' , LogoutView.as_view(next_page="user:login") , name="logout")
]
