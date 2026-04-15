
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

    # --- LO NUEVO PARA EL EQUIPO ---
    # Quien crea la tarea
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas_creadas')
    
    # A QUIÉN SE LE ASIGNA (Para que salga en el Kanban y Métricas)
    asignado_a = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tareas_asignadas'
    )

    # --- LO QUE YA TENÍAS (Mantenemos los booleanos para el Kanban de Yenderson) ---
    estado = models.CharField(max_length=4, choices=ESTADO_CHOICES, default='TODO')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    prioridad = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='M')
    
    categoria = models.ForeignKey(
        'categorias.Categorias',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tareas'
    )
    
    workspace = models.ForeignKey(
        'workspaces.Workspace',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tareas'
    )
    
    fecha_vencimiento = models.DateField(null=True, blank=True)
    
    # NO TOCAR: Estos los usa el Kanban para mover las tarjetas
    completada = models.BooleanField(default=False)
    en_progreso = models.BooleanField(default=False)
    
    creado_en = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-creado_en']

    def __str__(self):
        return self.titulo