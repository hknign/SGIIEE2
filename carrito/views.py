from django.shortcuts import render, redirect
from decimal import Decimal
from collections import defaultdict
from django.http import JsonResponse
from django.db import transaction
import json

from asientos.models import Asiento
from .models import ItemCarrito

# Ver carrito
def ver_carrito(request):
    if request.user.is_authenticated:
        items = ItemCarrito.objects.filter(usuario=request.user).select_related("asiento__evento")
    else:
        items = []

    grupos = defaultdict(list)
    for item in items:
        grupos[item.asiento.evento].append(item.asiento)

    bloques = []
    total_global = Decimal("0.00")

    for evento, lista in grupos.items():
        subtotal = sum((a.precio or Decimal("0.00")) for a in lista)
        bloques.append({
            "evento": evento,
            "asientos": lista,
            "cantidad": len(lista),
            "total": subtotal,
        })
        total_global += subtotal

    return render(request, "carritos/carrito.html", {
        "bloques": bloques,
        "total_global": total_global
    })


# API agregar asientos al carrito
def api_agregar_asientos_carrito(request):
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Método no permitido"})

    try:
        data = json.loads(request.body)
        ids = data.get("asientos", [])
    except Exception:
        return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)

    if not ids:
        return JsonResponse({"ok": False, "error": "No se enviaron asientos"}, status=400)

    añadidos, errores = [], []

    with transaction.atomic():
        for asiento_id in ids:
            asiento = Asiento.objects.select_for_update().filter(pk=asiento_id).first()
            if not asiento:
                errores.append({"id": asiento_id, "error": "Asiento inexistente"})
                continue

            if asiento.estado != "disponible":
                errores.append({"id": asiento_id, "error": "No disponible"})
                continue

            asiento.estado = "apartado"
            asiento.save()

            ItemCarrito.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                asiento=asiento
            )

            añadidos.append({
                "id": asiento.id,
                "codigo": asiento.fila + str(asiento.numero),
                "precio": str(asiento.precio)
            })

    return JsonResponse({
        "ok": len(añadidos) > 0,
        "añadidos": añadidos,
        "errores": errores
    }, status=200 if añadidos else 400)


# Quitar asiento del carrito
def quitar_del_carrito(request, item_id):
    try:
        with transaction.atomic():
            item = ItemCarrito.objects.select_related("asiento").get(pk=item_id, usuario=request.user)
            asiento = item.asiento
            asiento.estado = "disponible"
            asiento.save()
            item.delete()
    except ItemCarrito.DoesNotExist:
        pass

    return redirect("carrito:ver_carrito")


# Pagar carrito
def pagar_carrito(request):
    if request.user.is_authenticated:
        items = ItemCarrito.objects.filter(usuario=request.user).select_related("asiento")
    else:
        items = []

    total = sum((item.asiento.precio or Decimal("0.00")) for item in items)

    # Liberar asientos y vaciar carrito
    with transaction.atomic():
        for item in items:
            asiento = item.asiento
            asiento.estado = "vendido"
            asiento.save()
            item.delete()

    return render(request, "carritos/pagar.html", {
        "asientos": [item.asiento for item in items],
        "total": total,
        "mensaje": "Gracias por tu compra."
    })