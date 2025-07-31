from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Sitio, User, Laboratorio, Instrumento
from .models import ParametrosGlobales  
from .models import Estado, Seccion  # Asegúrate de importar los modelos adicionales

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'laboratorio', 'is_staff', 'is_active')

    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('rol', 'laboratorio')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('rol', 'laboratorio')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Laboratorio)
admin.site.register(Instrumento)
admin.site.register(Sitio)
admin.site.register(ParametrosGlobales)     
admin.site.register(Estado) 
admin.site.register(Seccion) 
