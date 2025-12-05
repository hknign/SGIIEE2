from django.db import models
from decimal import Decimal


class Categoria(models.Model):
    nombre = models.CharField(max_length=120)

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    FORMAS = [
        ("triangulo","Triángulo"),
        ("cuadrado","Cuadrado"),
        ("rectangulo","Rectángulo"),
        ("circulo","Círculo"),
        ("hexagono","Hexágono"),
        ("octagono","Octágono"),
    ]

    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(blank=True)

    fecha = models.DateField()
    hora = models.TimeField()

    lugar = models.CharField(max_length=250)
    capacidad = models.PositiveIntegerField()
    forma_recinto = models.CharField(max_length=20, choices=FORMAS, default="cuadrado")

    categoria = models.ForeignKey("Categoria", null=True, blank=True, on_delete=models.SET_NULL)
    imagen = models.ImageField(upload_to='eventos/', null=True, blank=True)

    precio_vip = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("300.00"))
    precio_avanzado = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("180.00"))
    precio_normal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("100.00"))

    def __str__(self):
        return self.nombre
