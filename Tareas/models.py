from django.db import models
from django.contrib.auth.models import User
from categorias.models import Categorias

class Tareas(models.Model):
    class Prioridad(models.TextChoices):
        BAJA= 'Baja', 'Baja'
        #Mayuscula nombre interno para el programador= El primero es el que se guarda en la BD y ek segundo es el que ve el usuario
        MEDIA= 'Media', 'Media'
        ALTA='Alta', 'Alta'

    class Estado(models.TextChoices):
        PENDIENTE='Pendiente', 'Pendiente'
        EN_PROGRESO='Progreso', 'En progreso'
        COMPLETADA='Completada', 'Completada'

    titulo=models.CharField(max_length=200)
    descripcion=models.TextField(blank=True, null=True)
    prioridad=models.CharField(max_length=10, choices=Prioridad.choices, default=Prioridad.BAJA)
    estado=models.CharField(max_length=15, choices=Estado.choices, default=Estado.PENDIENTE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField(null=True, blank=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    categoria = models.ForeignKey(Categorias, on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas')

    def __str__(self):
        return self.titulo