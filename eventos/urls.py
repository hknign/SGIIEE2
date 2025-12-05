from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [

    path("", views.listar_eventos, name="listar_eventos"),

    # CRUD Evento
    path("evento/<int:pk>/", views.detalle_evento, name="detalle_evento"),
    path("evento/crear/", views.crear_evento, name="crear_evento"),
    path("evento/<int:pk>/editar/", views.editar_evento, name="editar_evento"),
    path("evento/<int:pk>/eliminar/", views.eliminar_evento, name="eliminar_evento"),

    # Categorías (Ajax)
    path("categoria/ajax/", views.crear_categoria_ajax, name="crear_categoria_ajax"),

    # Panel admin
    path("panel/", views.panel_administrador, name="panel_administrador"),
]