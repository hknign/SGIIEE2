from django.contrib import admin
from .models import Categoria, Evento


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'hora', 'lugar', 'capacidad', 'categoria')
    search_fields = ('nombre', 'lugar')
    list_filter = ('fecha', 'categoria')
