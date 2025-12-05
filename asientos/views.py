from django.shortcuts import render

import json
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.shortcuts import redirect

from .models import Asiento
# Create your views here.

# API obtener asientos de un evento
def api_asientos_evento(request, evento_id):
    asientos = Asiento.objects.filter(evento_id=evento_id)

    data = [{
        "id": a.id,
        "fila": a.fila,
        "numero": a.numero,
        "estado": a.estado,
        "pos_x": float(a.pos_x),
        "pos_y": float(a.pos_y),
        "zona": a.zona,
        "precio": float(a.precio),
    } for a in asientos]

    return JsonResponse({"asientos": data})