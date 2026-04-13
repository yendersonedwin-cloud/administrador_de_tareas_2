# Register your models here.
from django.contrib import admin
from .models import Workspace

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display  = ['nombre', 'admin', 'codigo', 'creado_en']
    readonly_fields = ['codigo']