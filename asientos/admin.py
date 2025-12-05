from django.contrib import admin
from .models import Asiento


@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    list_display = ('evento', 'fila', 'numero', 'estado')
    list_filter = ('evento', 'estado')
