from django.db import models
from django.contrib.auth import get_user_model
from asientos.models import Asiento

Usuario = get_user_model()


class ItemCarrito(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="items_carrito"
    )
    asiento = models.ForeignKey(
        Asiento,
        on_delete=models.CASCADE,
        related_name="items_carrito"
    )
    agregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Item de Carrito"
        verbose_name_plural = "Items de Carrito"
        ordering = ["-agregado_en"]

    def __str__(self):
        return f"Asiento {self.asiento.fila}{self.asiento.numero} - {self.usuario or 'anónimo'}"
