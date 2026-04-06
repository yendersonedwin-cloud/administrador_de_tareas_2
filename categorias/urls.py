"""
categorias/urls.py — TaskFlow

Rutas de la app de categorías.
Prefijo en el urls.py raíz: /categorias/
Por lo tanto las rutas reales son:
  POST /categorias/crear/
  POST /categorias/actualizar/<pk>/
  POST /categorias/eliminar/<pk>/
"""

from django.urls import path
from . import views

urlpatterns = [
    path('crear/',                   views.crear_categoria,     name='crear_categoria'),
    path('actualizar/<int:pk>/',     views.actualizar_categoria, name='actualizar_categoria'),
    path('eliminar/<int:pk>/',       views.eliminar_categoria,   name='eliminar_categoria'),
]