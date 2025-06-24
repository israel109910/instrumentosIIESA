from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # ✅ Import necesario para usar messages
from django.http import HttpResponse, FileResponse, HttpResponseForbidden
from django.db.models import Q
from .models import Instrumento, Laboratorio
from .forms import InstrumentoForm, InstrumentoFormLab
from io import BytesIO
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

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
# Vista principal (inicio)
# --------------------------
@login_required
@user_passes_test_with_message(es_lab_o_admin)
def inicio(request):
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

    # Filtro por rol de usuario
    if request.user.rol == 'LAB':
        instrumentos = instrumentos.filter(laboratorio=request.user.laboratorio)

    # Filtro por búsqueda
    if q:
        instrumentos = instrumentos.filter(
            Q(nombre__icontains=q) |
            Q(tag__icontains=q) |
            Q(folio__icontains=q) |  # ✅ Se agregó búsqueda por folio
            Q(serie__icontains=q)
        )

    # Filtro por laboratorio
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
from django import forms  # ⚠️ Asegúrate de tener esto también

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
        form = InstrumentoForm(request.POST, request.FILES, instance=instrumento)
        if form.is_valid():
            instrumento = form.save(commit=False)
            if request.user.rol == 'LAB':
                instrumento.laboratorio = request.user.laboratorio
            instrumento.save()
            messages.success(request, "Instrumento actualizado correctamente.")
            return redirect('lista_instrumentos')
    else:
        form = InstrumentoForm(instance=instrumento)

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
def qr_pdf(request, instrumento_id):
    instrumento = get_object_or_404(Instrumento, id=instrumento_id)
    url = request.build_absolute_uri(f"/validar/{instrumento.uuid}/")

    qr_img = qrcode.make(url)
    qr_io = BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_io.seek(0)

    qr_image = ImageReader(qr_io)
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    p.drawImage(qr_image, x=200, y=600, width=200, height=200)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 550, f"Instrumento: {instrumento.nombre}")
    p.setFont("Helvetica", 11)
    p.drawString(100, 530, f"Tag: {instrumento.tag}")
    p.drawString(100, 510, f"Modelo: {instrumento.modelo}")
    p.drawString(100, 490, f"Serie: {instrumento.serie}")
    p.drawString(100, 470, f"Fecha de calibración: {instrumento.fecha_calibracion.strftime('%d/%m/%Y')}")
    p.drawString(100, 450, f"UUID: {instrumento.uuid}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f"{instrumento.tag}_qr.pdf")

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
