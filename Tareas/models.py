import uuid
from django.db import models
from django.contrib.auth.models import User

class EspacioTrabajo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Equipo")
    codigo = models.CharField(
        max_length=8, 
        unique=True, 
        default=uuid.uuid4().hex[:8].upper(),
        editable=False,
        verbose_name="Código de Acceso"
    )
    administrador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='mis_equipos', 
        null=True,
        verbose_name="Creador del Equipo"
    )

    class Meta:
        verbose_name = "Espacio de Trabajo"
        verbose_name_plural = "Espacios de Trabajo"

    def __str__(self):
        return self.nombre

class Tareas(models.Model):
    PRIORIDAD_CHOICES = [
        ('A', 'Alta'),
        ('M', 'Media'),
        ('B', 'Baja'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    prioridad = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='M')
    
    
    espacio_trabajo = models.ForeignKey(
        EspacioTrabajo, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='tareas_equipo',
        verbose_name="Equipo"
    )
    
    categoria = models.ForeignKey(
        'categorias.Categorias',   
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tareas'
    )
    fecha_vencimiento = models.DateField(null=True, blank=True)
    completada = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-creado_en']

    def __str__(self):
        return self.titulo