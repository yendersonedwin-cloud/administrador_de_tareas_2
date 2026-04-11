"""
tareas/models.py — TaskFlow

Modelo principal de tareas.
Incluye: prioridad, categoría, fecha de vencimiento, completada, timestamps.
"""

from django.db import models
from django.contrib.auth.models import User


class Tareas(models.Model):
    PRIORIDAD_CHOICES = [
        ('A', 'Alta'),
        ('M', 'Media'),
        ('B', 'Baja'),
    ]

    usuario           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    titulo            = models.CharField(max_length=255)
    descripcion       = models.TextField(blank=True, null=True)
    prioridad         = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='M')
    categoria         = models.ForeignKey(
                            'categorias.Categorias',   # Referencia a la otra app
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='tareas'
                        )
    fecha_vencimiento = models.DateField(null=True, blank=True)
    completada        = models.BooleanField(default=False)
    creado_en         = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering            = ['-creado_en']

    def __str__(self):
        return self.titulo