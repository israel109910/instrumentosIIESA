from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.db.models import Q
from .models import Instrumento, Laboratorio, Sitio, ParametrosGlobales, Estado, Seccion
from .forms import InstrumentoForm, InstrumentoFormLab
from io import BytesIO
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os
from django.conf import settings
import json

# ==========================
# Validadores de roles
# ==========================

def es_laboratorio(user):
    return user.is_authenticated and user.rol == 'LAB'

def es_admin(user):
    return user.is_authenticated and user.rol == 'ADMIN'

def es_verificador(user):
    return user.is_authenticated and user.rol == 'VALIDADOR'

def es_lab_o_admin(user):
    return user.is_authenticated and user.rol in ['LAB', 'ADMIN']

def es_autorizado(user):
    return user.is_authenticated and user.rol in ['LAB', 'ADMIN', 'VALIDADOR']

# ==========================
# Decorador personalizado
# ==========================

def user_passes_test_with_message(test_func, login_url=None, message="No tienes permiso para acceder a esta página."):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            if login_url:
                return redirect(login_url)
            return redirect('unauthorized')
        return _wrapped_view
    return decorator

# --------------------------
# Vista principal instrumentos(inicio)
# --------------------------

@login_required
@user_passes_test_with_message(es_lab_o_admin)
def inicio(request):
    return render(request, 'main.html')

@login_required
@user_passes_test_with_message(es_lab_o_admin)
def inicio_instrumentos(request):
    return render(request, 'inicio.html')

# --------------------------
# Lista de instrumentos
# --------------------------
@login_required
@user_passes_test_with_message(es_lab_o_admin)
def lista_instrumentos(request):
    q = request.GET.get('q', '')
    laboratorio_id = request.GET.get('laboratorio')
    instrumentos = Instrumento.objects.all()

    # FILTRO por rol: si es LAB, solo ve los instrumentos de su laboratorio
    if request.user.rol == 'LAB':
        instrumentos = instrumentos.filter(laboratorio=request.user.laboratorio)

    # FILTRO por búsqueda (nombre, tag, folio, serie)
    if q:
        instrumentos = instrumentos.filter(
            Q(nombre__icontains=q) |
            Q(tag__icontains=q) |
            Q(folio__icontains=q) |
            Q(serie__icontains=q)
        )

    # FILTRO por laboratorio solo si es ADMIN
    if laboratorio_id and request.user.rol != 'LAB':
        instrumentos = instrumentos.filter(laboratorio_id=laboratorio_id)

    laboratorios = Laboratorio.objects.all()

    context = {
        'instrumentos': instrumentos,
        'laboratorios': laboratorios,
    }
    return render(request, 'instrumentos/lista.html', context)

# --------------------------
# Crear nuevo instrumento
# --------------------------
from django import forms

@login_required
@user_passes_test_with_message(es_lab_o_admin)
def crear_instrumento(request):
    if request.user.rol == 'ADMIN':
        form = InstrumentoForm(request.POST or None, request.FILES or None)
    else:
        form = InstrumentoFormLab(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        instrumento = form.save(commit=False)
        if request.user.rol == 'LAB':
            instrumento.laboratorio = request.user.laboratorio
        instrumento.save()
        messages.success(request, "Instrumento creado correctamente.")
        return redirect('lista_instrumentos')

    return render(request, 'instrumentos/formulario.html', {'form': form})

# --------------------------
# Editar instrumento
# --------------------------
@login_required
@user_passes_test_with_message(es_lab_o_admin)
def editar_instrumento(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, id=instrumento_id)

    if request.user.rol == 'LAB' and instrumento.laboratorio != request.user.laboratorio:
        messages.error(request, "No tienes permiso para editar este instrumento.")
        return redirect('lista_instrumentos')

    if request.method == 'POST':
        if request.user.rol == 'ADMIN':
            form = InstrumentoForm(request.POST, request.FILES, instance=instrumento)
        else:
            form = InstrumentoFormLab(request.POST, request.FILES, instance=instrumento)
        if form.is_valid():
            instrumento = form.save(commit=False)
            if request.user.rol == 'LAB':
                instrumento.laboratorio = request.user.laboratorio
            instrumento.save()
            messages.success(request, "Instrumento actualizado correctamente.")
            return redirect('lista_instrumentos')
    else:
        if request.user.rol == 'ADMIN':
            form = InstrumentoForm(instance=instrumento)
        else:
            form = InstrumentoFormLab(instance=instrumento)

    return render(request, 'instrumentos/formulario.html', {'form': form})

# --------------------------
# Detalle de instrumento
# --------------------------
@login_required
@user_passes_test_with_message(es_lab_o_admin)
def detalle_instrumento(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, id=instrumento_id)
    return render(request, 'instrumentos/detalle.html', {'instrumento': instrumento})


# --------------------------
# Validación por UUID (QR)
# --------------------------
@login_required
@user_passes_test_with_message(es_autorizado)
def validar_certificado(request, uuid):
    instrumento = get_object_or_404(Instrumento, uuid=uuid)
    return render(request, 'instrumentos/validacion.html', {'instrumento': instrumento})

# --------------------------
# Generar QR (PNG)
# --------------------------
@login_required
@user_passes_test_with_message(es_lab_o_admin)
def generar_qr(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, id=instrumento_id)
    url = request.build_absolute_uri(f"/validar/{instrumento.uuid}/")
    qr_img = qrcode.make(url)
    buffer = BytesIO()
    qr_img.save(buffer)
    buffer.seek(0)
    return HttpResponse(buffer.read(), content_type="image/png")

# --------------------------
# Descargar QR como PDF
# --------------------------
@login_required
@user_passes_test_with_message(es_lab_o_admin)
def qr_pdf(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, id=instrumento_id)
    url = request.build_absolute_uri(f"/validar/{instrumento.uuid}/")

    # Generar código QR
    qr_img = qrcode.make(url)
    qr_io = BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_io.seek(0)
    qr_image = ImageReader(qr_io)

    # Ruta del logotipo local
    logo_path = os.path.join(settings.BASE_DIR, 'imagenes', 'LOGO.png')
    logo_image = ImageReader(logo_path)

    # Crear PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Dibujar logo
    p.drawImage(logo_image, x=50, y=height - 100, width=200, height=60, preserveAspectRatio=True)

    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(220, height - 80, "Certificado de Instrumento")

    # Código QR
    p.drawImage(qr_image, x=200, y=height - 350, width=200, height=200)

    # Información del instrumento
    y_start = height - 370
    spacing = 20
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y_start, f"Instrumento: {instrumento.nombre}")

    p.setFont("Helvetica", 11)
    p.drawString(100, y_start - spacing, f"Tag: {instrumento.tag}")
    p.drawString(100, y_start - 2 * spacing, f"Modelo: {instrumento.modelo}")
    p.drawString(100, y_start - 3 * spacing, f"Serie: {instrumento.serie}")
    p.drawString(100, y_start - 4 * spacing, f"Folio: {instrumento.folio}")
    p.drawString(100, y_start - 5 * spacing, f"Fecha de calibración: {instrumento.fecha_calibracion.strftime('%d/%m/%Y')}")
    p.drawString(100, y_start - 6 * spacing, f"UUID: {instrumento.uuid}")

    # Finalizar PDF
    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"{instrumento.tag}_qr.pdf")

def calcular_viaticos(request):
    estados = Estado.objects.all()
    secciones = Seccion.objects.all()
    sitios = Sitio.objects.all()
    resultado = None

    if request.method == 'POST':
        sitio_id = request.POST.get('sitio')
        personas = request.POST.get('personas')
        dias = request.POST.get('dias')
        herramientas = request.POST.get('herramientas') == 'on'

        if sitio_id and personas and dias:
            try:
                personas = int(personas)
                dias = int(dias)
                sitio = Sitio.objects.get(id=sitio_id)
                parametros = ParametrosGlobales.objects.first()

                km_totales = float(sitio.distancia_km)
                peso_prom_persona = float(parametros.peso_prom_persona)
                peso_herramienta = float(parametros.peso_herramienta)
                rendimiento_km_l = float(parametros.rendimiento_km_l)
                precio_gasolina = float(parametros.precio_gasolina)
                factor_penalizacion = float(parametros.factor_penalizacion)
                costo_peaje = float(sitio.costo_peaje) if sitio.requiere_tag else 0.0

                peso_personal = personas * peso_prom_persona
                peso_herramientas = peso_herramienta if herramientas else 0.0
                peso_total = peso_personal + peso_herramientas
                peso_relativo = peso_total / 100

                rendimiento_ajustado = rendimiento_km_l - (peso_relativo / factor_penalizacion)
                if rendimiento_ajustado <= 0:
                    costo_gasolina = 0
                else:
                    costo_gasolina = ((km_totales / rendimiento_ajustado) * precio_gasolina) * dias

                resultado = {
                    'sitio': sitio.nombre,
                    'requiere_tag': sitio.requiere_tag,
                    'costo_peaje': costo_peaje,
                    'costo_gasolina': round(costo_gasolina, 2),
                    'costo_total': round(costo_gasolina + costo_peaje, 2)
                }
            except Exception as e:
                resultado = {'error': 'Datos inválidos o incompletos.'}

    secciones_dict = {s.id: {'nombre': s.nombre, 'estado_id': s.estado.id} for s in secciones}
    sitios_dict = {s.id: {'nombre': s.nombre, 'seccion_id': s.seccion.id} for s in sitios}

    return render(request, 'viaticos.html', {
        'estados': estados,
        'resultado': resultado,
        'secciones_json': json.dumps(secciones_dict),
        'sitios_json': json.dumps(sitios_dict),
    })

# --------------------------
# Logout success
# --------------------------
def logout_success(request):
    return render(request, 'logout.html')

# --------------------------
# Página no autorizada
# --------------------------
def unauthorized(request, message="No tienes permiso para acceder a esta página."):
    return render(request, 'unauthorized.html', {'message': message})
