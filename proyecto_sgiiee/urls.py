from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("", include("core.urls")),
    path("eventos/", include("eventos.urls")),
    path("asientos/", include("asientos.urls")),
    path("carrito/", include("carrito.urls")),
    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
