from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from .models import Evento
import os

# Eliminar la imagen del evento cuando se elimina el evento

@receiver(post_delete, sender=Evento)
def eliminar_imagen_evento(sender, instance, **kwargs):
    if instance.imagen:
        instance.imagen.delete(False)

# Reemplazar la imagen anterior si se actualiza la imagen del evento

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

# Renombrar la imagen del evento después de guardar el evento para incluir su ID en el nombre del archivo

@receiver(post_save, sender=Evento)
def renombrar_imagen_evento(sender, instance, created, **kwargs):
    if instance.imagen:
        path_original = instance.imagen.path
        dir_base = os.path.dirname(path_original)

        # Nueva ruta final
        extension = instance.imagen.name.split('.')[-1]
        nombre_final = f"evento_{instance.id}.{extension}"
        nueva_ruta = os.path.join(dir_base, nombre_final)

        if not os.path.exists(nueva_ruta):
            os.rename(path_original, nueva_ruta)

            # actualizar el campo en DB
            instance.imagen.name = f"eventos/{nombre_final}"
            instance.save()