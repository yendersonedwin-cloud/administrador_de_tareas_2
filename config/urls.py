"""
config/urls.py — TaskFlow (urls.py RAÍZ)
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth: login, logout, registro — con prefijo /accounts/
    # DEBE ir antes que Tareas para que login funcione
    path('accounts/', include('usuarios.urls')),

    # Dashboard y CRUD de tareas — en la raíz /
    path('', include('Tareas.urls')),

    # CRUD de categorías
    path('categorias/', include('categorias.urls')),
]