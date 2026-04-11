"""
usuarios/urls.py — TaskFlow
Rutas bajo el prefijo /accounts/
"""

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .forms import LoginForm

urlpatterns = [
    # Ahora usa CustomLoginView para el mensaje de bienvenida
    path('login/',    views.CustomLoginView.as_view(
                          authentication_form=LoginForm,
                          redirect_authenticated_user=True,
                      ), name='login'),

    path('logout/',   LogoutView.as_view(next_page='login'), name='logout'),

    path('registro/', views.registro,      name='registro'),
    path('profile/',  views.profile_view,  name='profile'),   # ← nueva
]