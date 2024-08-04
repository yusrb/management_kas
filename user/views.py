from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from typing import Any

class UserRegisterView(CreateView):
  form_class = CustomUserCreationForm
  template_name = 'user/register.html'
  success_url = reverse_lazy('user:login')

  def get_context_data(self, **kwargs) -> dict[str, Any]:
      context = super().get_context_data(**kwargs)
      context["judul"] = "Register Form"
      return context

class LoginView(LoginView):
   template_name = 'user/login.html'

   def get_success_url(self):
    return reverse_lazy('base:daftar')

   def form_valid(self, form):
        messages.success(self.request, 'Login berhasil! Selamat datang kembali!')
        return super().form_valid(form)
