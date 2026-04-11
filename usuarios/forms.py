from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil
 
 
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

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Correo electrónico')

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'input-profile'})

# En tu forms.py
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['imagen', 'bio']
        widgets = {
            # Esto es lo que falta para que aparezca el cuadro de escritura
            'bio': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Cuéntanos a qué te dedicas...',
                'class': 'form-control' # Opcional si usas clases globales
            }),
        }