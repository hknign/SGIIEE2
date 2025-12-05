from django.contrib import admin
from .models import ItemCarrito


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('asiento', 'usuario', 'agregado_en')
