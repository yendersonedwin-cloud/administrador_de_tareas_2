from django.shortcuts import render, redirect
from .models import Tareas
from .forms import TareaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required # Esto asegura que solo alguien logueado vea sus tareas

def lista_tareas(request):
    tareas = Tareas.objects.filter(usuario=request.user)
    return render(request, 'tareas/lista.html', {'tareas': tareas})

@login_required
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user 
            tarea.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm()
    return render(request, 'tareas/crear_tarea.html', {'form': form})

@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)
    
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm(instance=tarea)
    
    return render(request, 'tareas/editar_tarea.html', {'form': form, 'tarea': tarea})

@login_required
def eliminar_tarea(request, tarea_id):
    tarea= get_object_or_404(Tareas, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('lista_tareas')
    

    return render(request, 'tareas/confirmar_eliminacion.html', {'tarea': tarea})


