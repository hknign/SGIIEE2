from django.shortcuts import render 
from django.utils import timezone
from eventos.models import Evento
from asientos.models import Asiento
from django.db.models import Sum, Count
from datetime import date, datetime
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def home(request):

    hoy = timezone.now().date()

    proximos = Evento.objects.filter(fecha__gte=hoy).order_by('fecha')[:3]

    return render(request, 'core/home.html', {
        'proximos': proximos,
    })

@staff_member_required
def dashboard(request):

    # Datos de ejemplo (luego los reemplazamos con queries reales)
    total_eventos_mes = 8
    asistencia_promedio = 62
    ingresos_mes = 1250000
    rating_promedio = 4.2

    kpis = [
        {"texto": "Eventos del mes", "valor": total_eventos_mes},
        {"texto": "Asistencia promedio", "valor": f"{asistencia_promedio}%"},
        {"texto": "Ingresos del mes", "valor": f"${ingresos_mes:,}".replace(",", ".")},
        {"texto": "Calificación promedio", "valor": rating_promedio},
    ]


    context = {
        "kpis": kpis,
    }
    
    print("KPIS →", kpis)

    return render(request, "core/dashboard.html", context)

#Descomentar cuando se usen datos reales para el dashboard, adjunto comando Ctrl+K + Ctrl+C

#from carrito.models import ItemCarrito

# @staff_member_required
# def dashboard(request):

#     hoy = datetime.today()

#     # 1) Total eventos del mes actual
#     total_eventos_mes = Evento.objects.filter(
#         fecha__month=hoy.month,
#         fecha__year=hoy.year
#     ).count()

#     # 2) Asistencia promedio (ejemplo sencillo)
#     asistencia_total = Asiento.objects.filter(estado="ocupado").count()
#     total_asientos = Asiento.objects.all().count()

#     asistencia_promedio = (
#         round((asistencia_total / total_asientos) * 100, 1)
#         if total_asientos > 0 else 0
#     )

#     # 3) Ingresos totales (solo ejemplo)
#     ingresos_mes = ItemCarrito.objects.filter(
#         fecha_compra__month=hoy.month,
#         fecha_compra__year=hoy.year
#     ).aggregate(total=Sum("precio_total"))["total"] or 0

#     # 4) Rating promedio simulado (agregaremos reseñas después)
#     rating_promedio = 4.2

#     kpis = [
#         {"texto": "Eventos del mes", "valor": total_eventos_mes},
#         {"texto": "Asistencia promedio", "valor": f"{asistencia_promedio}%"},
#         {"texto": "Ingresos del mes", "valor": f"${int(ingresos_mes):,}".replace(",", ".")},
#         {"texto": "Calificación promedio", "valor": rating_promedio},
#     ]

#     context = {
#         "kpis": kpis,
#     }

#     return render(request, "core/dashboard.html", context)




