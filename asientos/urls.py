from django.urls import path
from . import views

app_name = "asientos"

urlpatterns = [
    path("api/<int:evento_id>/", views.api_asientos_evento, name="api_asientos_evento"),
]
