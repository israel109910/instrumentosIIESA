from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Instrumento, Laboratorio

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'rol')

# forms.py

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ['nombre', 'tag', 'modelo', 'serie', 'folio', 'fecha_calibracion', 'certificado', 'magnitud', 'laboratorio']
        widgets = {
            'fecha_calibracion': forms.DateInput(attrs={'type': 'date'}),
        }

class InstrumentoFormLab(forms.ModelForm):
    class Meta:
        model = Instrumento
        exclude = ['laboratorio']
        widgets = {
            'fecha_calibracion': forms.DateInput(attrs={'type': 'date'}),
        }
class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'identificador', 'descripcion']