from django.urls import path
from . import views

app_name = "carrito"

urlpatterns = [
    path("", views.ver_carrito, name="ver_carrito"),
    path("pagar/", views.pagar_carrito, name="pagar_carrito"),
    path("api/agregar/", views.api_agregar_asientos_carrito, name="api_agregar_asientos_carrito"),
    path("quitar/<int:item_id>/", views.quitar_del_carrito, name="quitar_del_carrito"),
]
