from django.shortcuts import render
from django.utils import timezone
from eventos.models import Evento

def index(request):

    hoy = timezone.now().date()

    proximos = Evento.objects.filter(fecha__gte=hoy).order_by('fecha')[:3]

    return render(request, 'sgiiee/index.html', {
        'proximos': proximos,
    })