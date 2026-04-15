from django import forms
from .models import Tareas
from django.contrib.auth.models import User

class TareaForm(forms.ModelForm):
    class Meta:
        model  = Tareas
        # Campos que coinciden exactamente con Tareas/models.py
        fields = ['titulo', 'descripcion', 'prioridad', 'fecha_vencimiento', 'categoria','asignado_a']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '¿Qué hay que hacer?'}),
            'asignado_a': forms.Select(attrs={'class': 'form-control'}), # Widget para el responsable
        }

    def __init__(self, *args, **kwargs):
        # Extraemos el workspace si viene desde la vista
        workspace = kwargs.pop('workspace', None)
        super().__init__(*args, **kwargs)
        
        # Opcionales
        self.fields['descripcion'].required       = False
        self.fields['prioridad'].required         = False
        self.fields['fecha_vencimiento'].required = False
        self.fields['categoria'].required         = False
        self.fields['asignado_a'].required        = False # Opcional por si es tarea personal

        # SI hay un workspace, filtramos para que solo aparezcan sus miembros
        if workspace:
            self.fields['asignado_a'].queryset = workspace.miembros.all()
        else:
            # Si no hay workspace, ocultamos el campo o lo dejamos vacío
            self.fields['asignado_a'].queryset = User.objects.none()