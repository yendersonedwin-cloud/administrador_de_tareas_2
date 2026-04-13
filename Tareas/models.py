
from django.db import models
from django.contrib.auth.models import User

"""
Tareas/models.py — TaskFlow

Cambios respecto a la versión anterior:
- workspace: FK opcional al modelo Workspace.
             Si es null, la tarea es personal.
             Si tiene workspace, pertenece al equipo.
"""

class Tareas(models.Model):
    PRIORIDAD_CHOICES = [
        ('A', 'Alta'),
        ('M', 'Media'),
        ('B', 'Baja'),
    ]
    ESTADO_CHOICES = [
        ('TODO', 'Por Hacer'),
        ('PROG', 'En Progreso'),
        ('DONE', 'Completada'),
    ]
    estado = models.CharField(max_length=4, choices=ESTADO_CHOICES, default='TODO')
    usuario           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    titulo            = models.CharField(max_length=255)
    descripcion       = models.TextField(blank=True, null=True)
    prioridad         = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='M')
    categoria         = models.ForeignKey(
                            'categorias.Categorias',
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='tareas'
                        )
    # null=True significa que la tarea puede ser personal (sin workspace)
    workspace         = models.ForeignKey(
                            'workspaces.Workspace',
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='tareas'
                        )
    fecha_vencimiento = models.DateField(null=True, blank=True)
    completada        = models.BooleanField(default=False)
    en_progreso   = models.BooleanField(default=False)
    creado_en         = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering            = ['-creado_en']

    def __str__(self):
        return self.titulo