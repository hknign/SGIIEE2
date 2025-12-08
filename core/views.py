from django.shortcuts import render 
from django.utils import timezone
from eventos.models import Evento
from asientos.models import Asiento
from django.db.models import Sum, Count
from datetime import date
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def home(request):

    hoy = timezone.now().date()

    proximos = Evento.objects.filter(fecha__gte=hoy).order_by('fecha')[:3]

    return render(request, 'core/home.html', {
        'proximos': proximos,
    })

from django.db.models import Sum, Count
from datetime import date

@staff_member_required
def dashboard(request):
    eventos = Evento.objects.all()
    total_eventos = eventos.count()

    total_asientos = Asiento.objects.count()
    vendidos = Asiento.objects.filter(estado="vendido").count()
    disponibles = Asiento.objects.filter(estado="disponible").count()

    # Ganancia total (sumando precio solo de asientos vendidos)
    ganancia_total = Asiento.objects.filter(
        estado="vendido"
    ).aggregate(total=Sum("precio"))["total"] or 0

    # Próximos 5 eventos
    proximos = Evento.objects.filter(fecha__gte=date.today()).order_by("fecha")[:5]

    return render(request, "sgiiee/dashboard.html", {
        "total_eventos": total_eventos,
        "total_asientos": total_asientos,
        "vendidos": vendidos,
        "disponibles": disponibles,
        "ganancia_total": ganancia_total,
        "proximos": proximos,
    })
