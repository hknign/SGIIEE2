from django.db import models
from decimal import Decimal
from eventos.models import Evento


class Asiento(models.Model):
    ESTADOS = [
        ('disponible','Disponible'),
        ('apartado','Apartado'),
        ('vendido','Vendido'),
    ]

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    fila = models.CharField(max_length=5)
    numero = models.PositiveIntegerField()

    estado = models.CharField(max_length=15, choices=ESTADOS, default='disponible')

    pos_x = models.FloatField(default=0)
    pos_y = models.FloatField(default=0)

    zona = models.CharField(max_length=20, default='normal')  
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    class Meta:
        unique_together = ('evento','fila','numero')
        ordering = ['fila','numero']

    def codigo(self):
        return f"{self.fila}{self.numero}"

    def __str__(self):
        return f"{self.codigo()} - {self.estado} - {self.zona}"
