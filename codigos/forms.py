from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Instrumento, Laboratorio

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'rol')

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ['nombre', 'tag', 'modelo', 'serie', 'fecha_calibracion', 'certificado', 'magnitud']
        widgets = {
            'fecha_calibracion': forms.DateInput(attrs={'type': 'date'}),
        }


class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'identificador', 'descripcion']