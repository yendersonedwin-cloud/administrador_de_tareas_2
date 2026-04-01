from django.db import models
from django.contrib.auth.models import User

class Categorias(models.Model):
    nombre = models.CharField(max_length=100)
    # Guardamos el hex (ej: #ffffff)
    color = models.CharField(max_length=7, default='#3498db')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"

class Tareas(models.Model):
    # Opciones para Prioridad
    class Prioridad(models.TextChoices):
        BAJA = 'Baja', 'Baja'
        MEDIA = 'Media', 'Media'
        ALTA = 'Alta', 'Alta'

    # Opciones para Estado
    class Estado(models.TextChoices):
        PENDIENTE = 'Pendiente', 'Pendiente'
        EN_PROGRESO = 'Progreso', 'En Progreso'
        COMPLETADA = 'Completada', 'Completada'

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    prioridad = models.CharField(
        max_length=10, 
        choices=Prioridad.choices, 
        default=Prioridad.BAJA
    )
    estado = models.CharField(
        max_length=15, 
        choices=Estado.choices, 
        default=Estado.PENDIENTE
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField(null=True, blank=True)
    
    # Relaciones
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    categoria = models.ForeignKey(
        Categorias, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tareas'
    )

    def __str__(self):
        return self.titulo