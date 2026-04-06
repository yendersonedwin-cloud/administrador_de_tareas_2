# Tareas/admin.py
# Categorias está en su propia app — se importa desde allí

from django.contrib import admin
from .models import Tareas
from categorias.models import Categorias   # ← importar desde la app correcta

admin.site.register(Tareas)
admin.site.register(Categorias)