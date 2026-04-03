from django.shortcuts import redirect, get_object_or_404
from .models import Categorias
from django.contrib.auth.decorators import login_required


# ⚠️ Esta app ya NO renderiza el dashboard.
# El dashboard lo maneja tareas/views.py que ya incluye las categorías en su contexto.

@login_required
def crear_categoria(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        color = request.POST.get('color')
        Categorias.objects.create(nombre=nombre, color=color)
        return redirect('dashboard')
    return redirect('dashboard')


@login_required
def actualizar_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    if request.method == "POST":
        categoria.nombre = request.POST.get('nombre')
        categoria.color = request.POST.get('color')
        categoria.save()
    return redirect('dashboard')


@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    if request.method == "POST":
        categoria.delete()
    return redirect('dashboard')