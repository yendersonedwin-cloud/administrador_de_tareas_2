from django.shortcuts import render, redirect, get_object_or_404
from .models import Tareas
from .forms import TareaForm
from django.contrib.auth.decorators import login_required


# Importamos Categorias desde la otra app para pasarlas al contexto
try:
    from categorias.models import Categorias
except ImportError:
    Categorias = None


@login_required
def lista_tareas(request):
    tareas = Tareas.objects.filter(usuario=request.user)
    categorias = Categorias.objects.all() if Categorias else []
    return render(request, 'dashboard.html', {
        'tareas': tareas,
        'categorias': categorias,
    })


@login_required
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()
        else:
            print(form.errors)
    return redirect('dashboard')


@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
    return redirect('dashboard')


@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
    return redirect('dashboard')