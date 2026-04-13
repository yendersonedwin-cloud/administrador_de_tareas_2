
# Create your models here.
"""
workspaces/models.py — TaskFlow

Modelo Workspace: espacio de trabajo compartido por un equipo.
- El admin crea el workspace y comparte el código.
- Los miembros se unen con ese código.
- Las tareas se vinculan al workspace mediante FK en Tareas/models.py
"""

import uuid
from django.db import models
from django.contrib.auth.models import User


class Workspace(models.Model):
    nombre      = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    admin       = models.ForeignKey(
                      User,
                      on_delete=models.CASCADE,
                      related_name='workspaces_admin'
                  )
    miembros    = models.ManyToManyField(
                      User,
                      related_name='workspaces_miembro',
                      blank=True
                  )
    # Código único de 8 caracteres — se genera automáticamente
    codigo      = models.CharField(max_length=8, unique=True, blank=True)
    creado_en   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Espacio de Trabajo'
        verbose_name_plural = 'Espacios de Trabajo'
        ordering            = ['-creado_en']

    def save(self, *args, **kwargs):
        # Solo genera el código la primera vez
        if not self.codigo:
            self.codigo = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre