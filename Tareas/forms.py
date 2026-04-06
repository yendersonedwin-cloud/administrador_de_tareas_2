from django import forms
from .models import Tareas

class TareaForm(forms.ModelForm):
    class Meta:
        model  = Tareas
        # Campos que coinciden exactamente con Tareas/models.py
        fields = ['titulo', 'descripcion', 'prioridad', 'fecha_vencimiento', 'categoria']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Opcionales — el quick-add solo necesita el título
        self.fields['descripcion'].required       = False
        self.fields['prioridad'].required         = False
        self.fields['fecha_vencimiento'].required = False
        self.fields['categoria'].required         = False