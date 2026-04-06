"""
usuarios/urls.py — TaskFlow

Estas rutas quedan bajo el prefijo /accounts/ (definido en config/urls.py)
Entonces las URLs reales son:
  /accounts/login/
  /accounts/logout/
  /accounts/registro/
"""

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from .forms import LoginForm

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name='login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name='login'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('registro/', views.registro, name='registro'),
]