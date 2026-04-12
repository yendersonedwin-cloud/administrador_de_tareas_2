from django.contrib import admin
from .models import Tareas, EspacioTrabajo
from categorias.models import Categorias

@admin.register(EspacioTrabajo)
class EspacioTrabajoAdmin(admin.ModelAdmin):
    
    list_display = ('nombre', 'codigo', 'administrador')
    search_fields = ('nombre', 'codigo')

@admin.register(Tareas)
class TareasAdmin(admin.ModelAdmin):
    
    list_display = ('titulo', 'usuario', 'espacio_trabajo', 'prioridad', 'completada')
    list_filter = ('prioridad', 'completada', 'espacio_trabajo') # Filtros rápidos a la derecha

admin.site.register(Categorias)