from django.apps import AppConfig

# Se activa las signals para el manejo de imágenes de eventos

class EventosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eventos'

    def ready(self):
        import eventos.signals