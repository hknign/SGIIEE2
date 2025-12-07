from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Evento

@receiver(post_delete, sender=Evento)
def eliminar_imagen_evento(sender, instance, **kwargs):
    if instance.imagen:
        instance.imagen.delete(False)

@receiver(pre_save, sender=Evento)
def reemplazar_imagen_anterior(sender, instance, **kwargs):
    if not instance.pk:
        return  # es creación, no hace falta comparar

    try:
        imagen_anterior = Evento.objects.get(pk=instance.pk).imagen
    except Evento.DoesNotExist:
        return

    imagen_nueva = instance.imagen
    if imagen_anterior and imagen_anterior != imagen_nueva:
        imagen_anterior.delete(save=False)