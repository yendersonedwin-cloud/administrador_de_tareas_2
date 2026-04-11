from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from .forms import RegistroForm, UserUpdateForm, ProfileUpdateForm # Importamos los nuevos forms
from .models import Perfil # Importamos el modelo Perfil
from Tareas.models import Tareas

# ── Login con mensaje de bienvenida ──────────────────────────────────────────
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form): # Corregido de 'response' a 'form' para que funcione el super()
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'¡Bienvenido de nuevo, {self.request.user.username}!'
        )
        return response

# ── Registro ──────────────────────────────────────────────────────────────────
def registro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Creamos el perfil automáticamente al registrarse
            Perfil.objects.create(usuario=user) 
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada.')
            return redirect('dashboard')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

# ── Perfil Actualizado ────────────────────────────────────────────────────────
@login_required
def profile_view(request):
    user = request.user

    # TRUCO DE SEGURIDAD: Crea el perfil si por alguna razón el usuario no lo tiene
    if not hasattr(user, 'perfil'):
        Perfil.objects.create(usuario=user)

    if request.method == 'POST':
        # Cargamos los datos que vienen del formulario (POST para texto, FILES para la imagen)
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.perfil)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('profile') # Redirige al nombre de tu URL de perfil
    else:
        # Si es un acceso normal (GET), mostramos los datos actuales
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.perfil)

    # Tus cálculos de estadísticas (se mantienen igual)
    total = Tareas.objects.filter(usuario=user).count()
    hechas = Tareas.objects.filter(usuario=user, completada=True).count()
    porcentaje = round((hechas / total * 100)) if total > 0 else 0

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'total_tareas': total,
        'tareas_hechas': hechas,
        'productividad': f'{porcentaje}%',
    }

    return render(request, 'profile.html', context)