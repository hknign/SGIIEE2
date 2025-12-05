from django.shortcuts import render
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Evento, Categoria
from .forms import FormularioEvento
from asientos.models import Asiento
from asientos.utils.generar_asientos import generar_asientos, generar_escenario

# Create your views here.

# eventos/views.py


# Listar eventos
def listar_eventos(request):
    q = request.GET.get("q", "")
    eventos = Evento.objects.all()
    if q:
        eventos = eventos.filter(nombre__icontains=q)

    return render(request, "eventos/listar_eventos.html", {"eventos": eventos})


# Crear evento
@staff_member_required
def crear_evento(request):
    if request.method == "POST":
        form = FormularioEvento(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save()

            generar_asientos(evento)

            messages.success(request, "Evento creado con asientos generados.")
            return redirect("eventos:detalle_evento", pk=evento.pk)

        messages.error(request, "El formulario contiene errores.")
    else:
        form = FormularioEvento()

    return render(request, "eventos/formulario_evento.html", {"form": form})


# Editar evento
@staff_member_required
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == "POST":
        form = FormularioEvento(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento actualizado.")
            return redirect("eventos:detalle_evento", pk=evento.pk)

    else:
        form = FormularioEvento(instance=evento)

    return render(
        request, "eventos/formulario_evento.html",
        {"form": form, "evento": evento}
    )


# Eliminar evento
@staff_member_required
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    if request.method == "POST":
        evento.delete()
        messages.success(request, "Evento eliminado.")
        return redirect("eventos:listar_eventos")

    return render(request, "eventos/confirmar_eliminacion.html", {"evento": evento})


# Detalle del evento
def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)

    # Si el evento no tiene asientos generados, los generamos
    if not Asiento.objects.filter(evento=evento).exists():
        generar_asientos(evento)

    asientos = Asiento.objects.filter(evento=evento).order_by("fila", "numero")

    # (el template actual no usa 'escenario', pero no estorba)
    return render(
        request,
        "eventos/detalle_evento.html",
        {
            "evento": evento,
            "asientos": asientos,
        },
    )


# Panel administrador
@staff_member_required
def panel_administrador(request):
    eventos = Evento.objects.all()
    total_asientos = Asiento.objects.count()
    disponibles = Asiento.objects.filter(estado="disponible").count()

    return render(request, "eventos/panel_administrador.html", {
        "eventos": eventos,
        "total_asientos": total_asientos,
        "asientos_disponibles": disponibles
    })


# Crear categoría (AJAX)
@require_POST
def crear_categoria_ajax(request):
    nombre = (request.POST.get("nombre") or "").strip()

    if not nombre:
        return JsonResponse({"ok": False, "error": "Debes ingresar un nombre"}, status=400)
    if len(nombre) < 3:
        return JsonResponse({"ok": False, "error": "Debe tener al menos 3 caracteres"}, status=400)
    if not re.match(r"^[A-Za-zÀ-ÿ0-9 ]+$", nombre):
        return JsonResponse({"ok": False, "error": "Nombre inválido"}, status=400)
    if Categoria.objects.filter(nombre__iexact=nombre).exists():
        return JsonResponse({"ok": False, "error": "La categoría ya existe"}, status=400)

    categoria = Categoria.objects.create(nombre=nombre)
    return JsonResponse({"ok": True, "id": categoria.id, "nombre": categoria.nombre})
