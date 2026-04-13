from django.urls import path
from . import views

urlpatterns = [
    # Acciones básicas
    path('crear/', views.crear_workspace, name='crear_workspace'),
    path('unirse/', views.unirse_workspace, name='unirse_workspace'),
    path('salir/<int:ws_id>/', views.salir_workspace, name='salir_workspace'),
    
    # Vista principal del workspace (¡IMPORTANTE! debe llamarse 'ver_workspace')
    path('<int:ws_id>/', views.ver_workspace, name='ver_workspace'),
    
    # Panel admin
    path('<int:ws_id>/admin/', views.panel_admin, name='panel_admin'),
    
    path('<int:workspace_id>/kanban/', views.kanban_workspace, name='kanban_workspace'),
    
    # Acciones sobre tareas
    path('tarea/<int:tarea_id>/completar/', views.completar_tarea_workspace, name='completar_tarea_workspace'),
    path('<int:ws_id>/tarea/<int:tarea_id>/eliminar/', views.eliminar_tarea_workspace, name='eliminar_tarea_workspace'),

    path('workspaces/<int:workspace_id>/kanban/',        views.kanban_workspace,    name='kanban_workspace'),
    path('workspaces/<int:workspace_id>/kanban/mover/',  views.mover_tarea_kanban,  name='mover_tarea_kanban'),
]