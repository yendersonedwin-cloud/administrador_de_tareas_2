from django import forms
from .models import Tareas
#El forms es el puente entre la BD y el usuario     
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['titulo', 'descripcion', 'prioridad', 'estado', 'fecha_limite', 'categoria']
        # fields son llos camplos que el usuario va ver y a editar
        

        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Estudiar para el parcial'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prioridad': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
        }