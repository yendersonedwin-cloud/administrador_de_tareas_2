"""
config/urls.py — TaskFlow (urls.py RAÍZ)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth: login, logout, registro — con prefijo /accounts/
    # DEBE ir antes que Tareas para que login funcione
    path('accounts/', include('usuarios.urls')),
    path('workspace/', include('workspaces.urls')),
    path('categorias/', include('categorias.urls')),

    # Dashboard y CRUD de tareas — en la raíz /
    path('', include('Tareas.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)