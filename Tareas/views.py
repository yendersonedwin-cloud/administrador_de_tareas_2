"""
Tareas/views.py — TaskFlow
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import date, timedelta

from .models import Tareas
from .forms import TareaForm

try:
    from categorias.models import Categorias
except ImportError:
    Categorias = None


@login_required
def lista_tareas(request):
    view_mode = request.GET.get('view', 'day')
    cat_id    = request.GET.get('cat')

    # ✅ hoy siempre definida aquí arriba — no dentro de un if
    hoy = date.today()

    tareas_qs = Tareas.objects.filter(usuario=request.user).select_related('categoria')

    if view_mode == 'completed':
        tareas = tareas_qs.filter(completada=True).order_by('-updated_at')

    elif view_mode == 'upcoming':
        proximos = hoy + timedelta(days=7)
        tareas = tareas_qs.filter(
            completada=False,
            fecha_vencimiento__gte=hoy,
            fecha_vencimiento__lte=proximos,
        ).order_by('fecha_vencimiento')

    elif view_mode == 'category' and cat_id:
        tareas = tareas_qs.filter(completada=False, categoria_id=cat_id)

    else:
        view_mode = 'day'
        tareas = (
            tareas_qs.filter(completada=False, fecha_vencimiento=hoy) |
            tareas_qs.filter(completada=False, fecha_vencimiento__isnull=True)
        ).distinct().order_by('prioridad', 'creado_en')

    # Categorías para el sidebar con conteo
    categorias = []
    if Categorias:
        for cat in Categorias.objects.all():
            cat.tareas_count = Tareas.objects.filter(
                usuario=request.user,
                categoria=cat,
                completada=False
            ).count()
            categorias.append(cat)

    # Categoría activa (para header)
    categoria_activa = None
    if view_mode == 'category' and cat_id and Categorias:
        try:
            categoria_activa = Categorias.objects.get(pk=cat_id)
        except Categorias.DoesNotExist:
            pass

    # ✅ Fecha compatible con Windows (sin %-d)
    fecha = timezone.now()
    fecha_hoy = fecha.strftime('%A, %B ') + str(fecha.day) + ', ' + str(fecha.year)

    context = {
        'tareas':           tareas,
        'categorias':       categorias,
        'view_mode':        view_mode,
        'cat_activa':       int(cat_id) if cat_id else None,
        'categoria_activa': categoria_activa,
        'fecha_hoy':        fecha_hoy,
    }
    return render(request, 'dashboard.html', context)


@login_required
def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea         = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()
        else:
            print("Error al crear tarea:", form.errors)
    return redirect('dashboard')


@login_required
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
        else:
            print("Error al editar:", form.errors)
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def completar_tarea(request, tarea_id):
    """Toggle completada — llamado por fetch() desde dashboard.js"""
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.completada = not tarea.completada
        tarea.save(update_fields=['completada', 'updated_at'])
        return JsonResponse({'ok': True, 'completada': tarea.completada})
    return JsonResponse({'ok': False}, status=405)