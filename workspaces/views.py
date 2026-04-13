"""
workspaces/views.py - VERSIÓN CORREGIDA CON ESTADOS PERSISTENTES
========================================
Eliminada duplicación de ver_workspace.
Todos los miembros ven todas las tareas, solo editan las suyas.
Los estados de Kanban se mantienen entre sesiones.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Case, When, Value, IntegerField

from .models import Workspace
from Tareas.models import Tareas
from Tareas.forms import TareaForm

import json
from django.views.decorators.http import require_POST


# ============================================================
# ACCIONES BÁSICAS
# ============================================================
@login_required
def kanban_workspace(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
 
    # Verifica que el usuario es miembro
    if request.user not in workspace.miembros.all():
        return redirect('dashboard')
 
    tareas = Tareas.objects.filter(workspace=workspace)

    # Workspaces del usuario para el sidebar
    user_workspaces = Workspace.objects.filter(miembros=request.user)
 
    context = {
        'workspace': workspace,
        'es_admin': request.user == workspace.admin,
        'tareas_pendientes':  tareas.filter(completada=False, en_progreso=False),
        'tareas_progreso':    tareas.filter(en_progreso=True, completada=False),
        'tareas_completadas': tareas.filter(completada=True),
        'user_workspaces': user_workspaces,
    }
    return render(request, 'kanban.html', context)


@login_required
def crear_workspace(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        
        if nombre:
            ws = Workspace.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                admin=request.user
            )
            ws.miembros.add(request.user)
            messages.success(request, f'✅ ¡Workspace "{ws.nombre}" creado! Código: {ws.codigo}')
        else:
            messages.error(request, '❌ El nombre es obligatorio.')
    
    return redirect('dashboard')


@login_required
def unirse_workspace(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip().upper()
        
        try:
            ws = Workspace.objects.get(codigo=codigo)
            if request.user in ws.miembros.all():
                messages.info(request, f'ℹ️ Ya eres miembro de "{ws.nombre}".')
            else:
                ws.miembros.add(request.user)
                messages.success(request, f'🎉 ¡Te uniste a "{ws.nombre}"!')
        except Workspace.DoesNotExist:
            messages.error(request, '❌ Código incorrecto.')
    
    return redirect('dashboard')


@login_required
def salir_workspace(request, ws_id):
    ws = get_object_or_404(Workspace, pk=ws_id)
    
    if request.method == 'POST':
        if ws.admin == request.user:
            messages.error(request, '⚠️ El administrador no puede salir.')
        else:
            ws.miembros.remove(request.user)
            messages.success(request, f'👋 Saliste de "{ws.nombre}".')
    
    return redirect('dashboard')


# ============================================================
# VISTA PRINCIPAL DEL WORKSPACE (UNIFICADA)
# ============================================================

@login_required
def ver_workspace(request, ws_id):
    """
    Vista ÚNICA y principal del workspace.
    - Verifica que el usuario sea miembro
    - Muestra TODAS las tareas del workspace ordenadas por estado
    - Cada usuario SOLO puede editar/eliminar las suyas
    - Formulario para crear nuevas tareas
    """
    ws = get_object_or_404(Workspace, pk=ws_id)
    
    # 🔒 Verificar acceso
    if request.user not in ws.miembros.all():
        messages.error(request, 'No tienes acceso a este workspace.')
        return redirect('dashboard')
    
    # Obtener todas las tareas del workspace ordenadas por estado
    # Primero las pendientes, luego en progreso, luego completadas
    tareas = Tareas.objects.filter(workspace=ws).select_related('usuario', 'categoria').annotate(
        estado_order=Case(
            When(completada=True, then=Value(3)),
            When(en_progreso=True, then=Value(2)),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by('estado_order', '-creado_en')
    
    # 📝 Crear o editar tarea (POST)
    if request.method == 'POST':
        if request.POST.get('editar_tarea') == '1':
            tarea_id = request.POST.get('tarea_id')
            tarea = get_object_or_404(Tareas, pk=tarea_id, usuario=request.user, workspace=ws)
            form = TareaForm(request.POST, instance=tarea)
            if form.is_valid():
                form.save()
                messages.success(request, f'✅ Tarea "{tarea.titulo}" actualizada.')
                return redirect('ver_workspace', ws_id=ws_id)
            else:
                messages.error(request, '❌ Error al actualizar la tarea. Revisa los datos e inténtalo de nuevo.')
        else:
            form = TareaForm(request.POST)
            if form.is_valid():
                tarea = form.save(commit=False)
                tarea.usuario = request.user
                tarea.workspace = ws
                # Asegurar estado inicial correcto
                tarea.completada = False
                tarea.en_progreso = False
                tarea.save()
                messages.success(request, f'✅ Tarea "{tarea.titulo}" creada.')
                return redirect('ver_workspace', ws_id=ws_id)
            else:
                messages.error(request, '❌ Error al crear la tarea. Revisa los datos.')
    else:
        form = TareaForm()
    
    # Contexto para el sidebar
    user_workspaces = Workspace.objects.filter(miembros=request.user)
    
    context = {
        'workspace': ws,
        'tareas': tareas,
        'form': form,
        'es_admin': (ws.admin == request.user),
        'user_workspaces': user_workspaces,
        'view_mode': 'workspace',
        'categorias': [],
        'fecha_hoy': None,
    }
    
    return render(request, 'workspaces/workspace.html', context)


# ============================================================
# COMPLETAR TAREA (AJAX)
# ============================================================

@login_required
def completar_tarea_workspace(request, tarea_id):
    """Cambia el estado de una tarea (solo el dueño). Soporta AJAX y formularios normales."""
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user)
    
    if request.method == 'POST':
        # Si estaba completada, vuelve a pendiente
        # Si no estaba completada, se completa y quita en_progreso
        if tarea.completada:
            tarea.completada = False
            tarea.en_progreso = False
        else:
            tarea.completada = True
            tarea.en_progreso = False
        tarea.save(update_fields=['completada', 'en_progreso', 'updated_at'])
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept', '').startswith('application/json'):
            return JsonResponse({'ok': True, 'completada': tarea.completada})
        return redirect('ver_workspace', ws_id=tarea.workspace.id)
    
    return JsonResponse({'ok': False}, status=405)


# ============================================================
# ELIMINAR TAREA
# ============================================================

@login_required
def eliminar_tarea_workspace(request, ws_id, tarea_id):
    """Elimina una tarea (solo el dueño)"""
    ws = get_object_or_404(Workspace, pk=ws_id)
    tarea = get_object_or_404(Tareas, id=tarea_id, usuario=request.user, workspace=ws)
    
    if request.method == 'POST':
        titulo = tarea.titulo
        tarea.delete()
        messages.success(request, f'🗑️ Tarea "{titulo}" eliminada.')
    
    return redirect('ver_workspace', ws_id=ws_id)


# ============================================================
# PANEL ADMIN (MÉTRICAS)
# ============================================================

@login_required
def panel_admin(request, ws_id):
    """Panel de métricas - SOLO ADMIN"""
    ws = get_object_or_404(Workspace, pk=ws_id)
    
    if ws.admin != request.user:
        messages.error(request, 'Solo el administrador puede ver métricas.')
        return redirect('ver_workspace', ws_id=ws_id)
    
    # Calcular métricas
    miembros_data = []
    total_grupo = 0
    hechas_grupo = 0
    
    for miembro in ws.miembros.all():
        total = Tareas.objects.filter(usuario=miembro, workspace=ws).count()
        hechas = Tareas.objects.filter(usuario=miembro, workspace=ws, completada=True).count()
        pct = round((hechas / total * 100)) if total > 0 else 0
        
        total_grupo += total
        hechas_grupo += hechas
        
        miembros_data.append({
            'usuario': miembro,
            'total_tareas': total,
            'tareas_hechas': hechas,
            'pendientes': total - hechas,
            'productividad': pct,
        })
    
    productividad_grupo = round((hechas_grupo / total_grupo * 100)) if total_grupo > 0 else 0
    historial = Tareas.objects.filter(workspace=ws).order_by('-updated_at')[:10]
    
    context = {
        'workspace': ws,
        'miembros_data': miembros_data,
        'total_grupo': total_grupo,
        'hechas_grupo': hechas_grupo,
        'productividad_grupo': productividad_grupo,
        'historial': historial,
        'user_workspaces': Workspace.objects.filter(miembros=request.user),
        'view_mode': 'workspace',
        'categorias': [],
    }
    
    return render(request, 'workspaces/panel_admin.html', context)


# ============================================================
# MOVER TAREA EN KANBAN (AJAX)
# ============================================================

@login_required
@require_POST
def mover_tarea_kanban(request, workspace_id):
    workspace = get_object_or_404(Workspace, id=workspace_id)
 
    # Solo el admin puede mover tareas
    if request.user != workspace.admin:
        return JsonResponse({'ok': False, 'error': 'Solo el administrador puede mover tareas.'}, status=403)
 
    try:
        data = json.loads(request.body)
        tarea_id = data.get('tarea_id')
        columna  = data.get('columna')
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'ok': False, 'error': 'Datos inválidos.'}, status=400)
 
    if columna not in ('todo', 'progreso', 'done'):
        return JsonResponse({'ok': False, 'error': 'Columna inválida.'}, status=400)
 
    tarea = get_object_or_404(Tareas, id=tarea_id, workspace=workspace)
 
    if columna == 'todo':
        tarea.en_progreso = False
        tarea.completada  = False
    elif columna == 'progreso':
        tarea.en_progreso = True
        tarea.completada  = False
    elif columna == 'done':
        tarea.en_progreso = False
        tarea.completada  = True
 
    tarea.save()
    return JsonResponse({'ok': True})




@login_required
def eliminar_workspace(request, ws_id):
    """Elimina el workspace completo (SOLO el administrador)"""
    ws = get_object_or_404(Workspace, pk=ws_id)
    
    # Seguridad: Solo el que creó el workspace (admin) puede borrarlo
    if ws.admin != request.user:
        messages.error(request, '❌ Solo el administrador puede eliminar este workspace.')
        return redirect('ver_workspace', ws_id=ws_id)
    
    if request.method == 'POST':
        nombre_ws = ws.nombre
        ws.delete()
        messages.success(request, f'🗑️ El workspace "{nombre_ws}" ha sido eliminado permanentemente.')
        return redirect('dashboard')
    
    return redirect('ver_workspace', ws_id=ws_id)