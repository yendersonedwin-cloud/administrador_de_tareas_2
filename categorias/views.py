"""
categorias/views.py — TaskFlow

Vistas de categorías.
IMPORTANTE: Esta app ya NO renderiza el dashboard.
            Solo maneja el CRUD de categorías.
            El dashboard lo renderiza tareas/views.py
"""

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Categorias


@login_required
def crear_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        color  = request.POST.get('color', '#10b981')
        if nombre:
            Categorias.objects.create(nombre=nombre, color=color)
    return redirect('dashboard')


@login_required
def actualizar_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre', categoria.nombre).strip()
        categoria.color  = request.POST.get('color', categoria.color)
        categoria.save()
    return redirect('dashboard')


@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    if request.method == 'POST':
        categoria.delete()
    return redirect('dashboard')