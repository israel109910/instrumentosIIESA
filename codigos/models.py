from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid
import os
from django.utils.text import slugify


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('LAB', 'Laboratorio'),
        ('VALIDADOR', 'Validador'),
    )
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES)
    laboratorio = models.ForeignKey('Laboratorio', on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='codigos_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='codigos_user_permissions_set',
        blank=True,
    )

class Laboratorio(models.Model):
    nombre = models.CharField(max_length=100)
    identificador = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


# Función para guardar el certificado con nombre personalizado
def ruta_certificado(instance, filename):
    nombre = slugify(instance.nombre)  # Ej: "termometro-uno"
    folio = slugify(instance.folio or "sin-folio")  # Evita errores si folio es None

    # Obtener extensión del archivo original
    extension = os.path.splitext(filename)[1]  # por ejemplo: '.pdf'
    nuevo_nombre = f"certificado_{folio}{extension}"  # certificado_f-001.pdf

    carpeta = f"{nombre}-{folio}"  # certificados/termometro-uno-f-001/
    return os.path.join('certificados', carpeta, nuevo_nombre)


class Instrumento(models.Model):
    MAGNITUD_CHOICES = [
        ('temperatura', 'Temperatura'),
        ('presion', 'Presión'),
        ('flujo', 'Flujo'),
        ('densidad', 'Densidad'),
    ]

    nombre = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serie = models.CharField(max_length=100)
    folio = models.CharField(max_length=100, null=True, blank=True)
    fecha_calibracion = models.DateField()
    quien_calibro = models.CharField(max_length=100, null=True, blank=True)
    certificado = models.FileField(upload_to=ruta_certificado, null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    magnitud = models.CharField(max_length=20, choices=MAGNITUD_CHOICES, default='temperatura')
    laboratorio = models.ForeignKey('Laboratorio', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.tag}"

class Sitio(models.Model):
    nombre = models.CharField(max_length=100)
    distancia_km = models.DecimalField(max_digits=6, decimal_places=2)  # ida y vuelta
    requiere_tag = models.BooleanField(default=False)  # Si requiere tag del instrumento
    costo_peaje = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Costo de peaje
    seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE, related_name='sitios')

    class Meta:
        verbose_name_plural = "Viaticos - Sitios"

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Viaticos - Estados"

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='secciones')

    class Meta:
        verbose_name_plural = "Viaticos - Secciones"

    def __str__(self):
        return self.nombre

class ParametrosGlobales(models.Model):
    precio_gasolina = models.DecimalField(max_digits=5, decimal_places=2)  # Precio por litro
    rendimiento_km_l = models.DecimalField(max_digits=5, decimal_places=2)  # km/l base
    peso_herramienta = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)  # en kg
    peso_prom_persona = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)  # en kg
    factor_penalizacion = models.DecimalField(max_digits=5, decimal_places=2, default=0.5) 
    herramientas = models.BooleanField(default=False)  # Factor de penalización
    cantidad_personas = models.IntegerField(default=1)  # Cantidad de personas por sitio
    dias_trabajo = models.IntegerField(default=1)  # Días de trabajo por semana

    class Meta:
        verbose_name_plural = "Viaticos - Parámetros Globales"
        
    def __str__(self):
        return "Parámetros Globales"