"""
categorias/models.py — TaskFlow

Modelo de Categorías.
"""

from django.db import models


class Categorias(models.Model):
    nombre = models.CharField(max_length=100)
    color  = models.CharField(max_length=7, default='#10b981')  # Hex color

    class Meta:
        verbose_name        = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering            = ['nombre']

    def __str__(self):
        return self.nombre