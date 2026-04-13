from django.contrib import admin
from .models import Tareas
from categorias.models import Categorias

@admin.register(Tareas)
class TareasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'workspace', 'prioridad', 'completada')
    list_filter  = ('prioridad', 'completada', 'workspace')

admin.site.register(Categorias)