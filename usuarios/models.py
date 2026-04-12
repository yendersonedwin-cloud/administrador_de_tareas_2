
from django.db import models
from django.contrib.auth.models import User # Importamos el usuario de Django

class Perfil(models.Model):
    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)
    
    # El campo para la foto. 'default.jpg' es la que sale si no suben nada.
    imagen = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    # Otros datos que quieras guardar
    bio = models.TextField(max_length=500, blank=True)

    
    def __str__(self):
        return f'Perfil de {self.usuario.username}'
    