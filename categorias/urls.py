from django.urls import path
from . import views

urlpatterns = [
    
    path('lista/', views.lista_categorias, name='lista_categorias'),
    
    
    path('crear/', views.crear_categoria, name='crear_categoria'),
    
    
    path('actualizar/<int:pk>/', views.actualizar_categoria, name='actualizar_categoria'),
    
    
    path('eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
]