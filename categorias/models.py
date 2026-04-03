from django.db import models

class Categorias(models.Model):
    PRIORIDAD_CHOICES = [
        ('A', 'Alta'),
        ('M', 'Media'),
        ('B', 'Baja'),
    ]

    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#3498db') 
    prioridad = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='M')

    def get_prioridad_color(self):
        if self.prioridad == 'A':
            return "#FF0000" 
        elif self.prioridad == 'M':
            return "#FFC107" 
        else:
            return "#28A745" 

    def __str__(self):
        # Aquí también usamos el display para que se vea "Alta" en lugar de "A"
        return f"{self.nombre} ({self.get_prioridad_display()})"

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"