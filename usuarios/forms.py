from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
 
 
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Tu usuario',
        'class': 'input-login',
        'id': 'id_username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '••••••••',
        'id': 'id_password',
        'class': 'input-login',
    }))
 
 
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Correo electrónico')
 
    class Meta:
        model = User
        # CRÍTICO: password1 y password2 deben estar en fields
        fields = ['username', 'email', 'password1', 'password2']
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
 
        placeholders = {
            'username':  'Elige un usuario',
            'email':     'tu@correo.com (opcional)',
            'password1': 'Crea una contraseña',
            'password2': 'Repite la contraseña',
        }
 
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': placeholders.get(name, field.label),
                'class': 'input-registro',
            })
            # Sincronizamos IDs para el JS de toggle
            field.widget.attrs['id'] = f'id_{name}'
 
        # Quitamos los textos de ayuda verbosos de Django
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None