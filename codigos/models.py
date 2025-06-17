from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid

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
    fecha_calibracion = models.DateField()
    certificado = models.FileField(upload_to='certificados/', null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    magnitud = models.CharField(max_length=20, choices=MAGNITUD_CHOICES, default='temperatura')
    laboratorio = models.ForeignKey('Laboratorio', on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.nombre} - {self.tag}"

