from django.urls import path
from . import views

urlpatterns = [
    # ⚠️ Esta app ya NO tiene una ruta 'dashboard' propia.
    # Solo maneja las acciones CRUD de categorías.
    path('crear/', views.crear_categoria, name='crear_categoria'),
    path('actualizar/<int:pk>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
]