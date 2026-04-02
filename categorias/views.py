from django.shortcuts import render, redirect, get_object_or_404
from .models import Categorias
from django.contrib.auth.decorators import login_required


@login_required
def lista_categorias(request):
    categorias = Categorias.objects.all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})


@login_required
def crear_categoria(request):
    if request.method == "POST":
        # Recibimos los datos del formulario que haremos luego
        nombre = request.POST.get('nombre')
        color = request.POST.get('color')
        prioridad = request.POST.get('prioridad')
        
        Categorias.objects.create(
            nombre=nombre, 
            color=color, 
            prioridad=prioridad
        )
        return redirect('lista_categorias')
    return render(request, 'categorias/form.html')


@login_required
def actualizar_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    if request.method == "POST":
        categoria.nombre = request.POST.get('nombre')
        categoria.color = request.POST.get('color')
        categoria.prioridad = request.POST.get('prioridad')
        categoria.save()
        return redirect('lista_categorias')
    return render(request, 'categorias/form.html', {'categoria': categoria})


@login_required
def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categorias, pk=pk)
    if request.method == "POST":
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'categorias/confirmar_eliminar.html', {'categoria': categoria})