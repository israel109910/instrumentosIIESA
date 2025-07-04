from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Instrumento, Laboratorio
from django.forms.widgets import DateInput


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'rol')

# forms.py

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ['nombre', 'tag', 'modelo', 'serie', 'folio', 'fecha_calibracion', 'quien_calibro', 'certificado', 'magnitud', 'laboratorio']
        labels = {
            'nombre': 'Nombre del Instrumento',
            'tag': 'Tag del Instrumento',
            'modelo': 'Modelo',
            'serie': 'Serie',
            'folio': 'Folio',
            'fecha_calibracion': 'Fecha de Calibración',
            'certificado': 'Certificado',
            'magnitud': 'Magnitud',
            'laboratorio': 'Laboratorio',
            'quien_calibro': 'Quién Calibró'
        }
        widgets = {
            'fecha_calibracion': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Solo si ya existe fecha_calibracion, establecerla como initial correctamente formateada
        if self.instance and self.instance.fecha_calibracion:
            self.fields['fecha_calibracion'].initial = self.instance.fecha_calibracion.strftime('%Y-%m-%d')


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