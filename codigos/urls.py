from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [

    path('', views.inicio, name='inicio'),
    path('inicio_instrumentos/', views.inicio_instrumentos, name='inicio_instrumentos'),
    path('instrumentos/', views.lista_instrumentos, name='lista_instrumentos'),
    path('instrumento/nuevo/', views.crear_instrumento, name='crear_instrumento'),
    path('instrumento/<int:instrumento_id>/editar/', views.editar_instrumento, name='editar_instrumento'),
    path('instrumento/<int:instrumento_id>/', views.detalle_instrumento, name='detalle_instrumento'),
    path('instrumento/<int:instrumento_id>/qr/', views.generar_qr, name='generar_qr'),
    path('instrumento/<int:instrumento_id>/qr_pdf/', views.qr_pdf, name='qr_pdf'),
    path('validar/<uuid:uuid>/', views.validar_certificado, name='validar_certificado'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('viaticos/', views.calcular_viaticos, name='viaticos'),
    path('debug-env/', views.debug_env, name='debug_env'),



]
