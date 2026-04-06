from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import RegistroForm


def registro(request):
    # Si ya está logueado, lo mandamos al dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login después del registro
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.username}! Tu cuenta fue creada.')
            return redirect('dashboard')
        # Si el form tiene errores, vuelve a renderizar con los errores
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})