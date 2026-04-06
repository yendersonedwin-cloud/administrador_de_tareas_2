"""
tareas/urls.py — TaskFlow

Rutas de la app de tareas.
Todas las rutas de categorías están en categorias/urls.py con prefijo /categorias/
"""

from django.urls import path
from . import views

urlpatterns = [
    # Dashboard principal (con filtros vía ?view=)
    path('', views.lista_tareas, name='dashboard'),

    # CRUD de tareas
    path('crear/',             views.crear_tarea,    name='crear_tarea'),
    path('editar/<int:tarea_id>/',   views.editar_tarea,   name='editar_tarea'),
    path('eliminar/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),

    # Toggle completar (fetch desde JS)
    path('completar/<int:tarea_id>/', views.completar_tarea, name='completar_tarea'),
]