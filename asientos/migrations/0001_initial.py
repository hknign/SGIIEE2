from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eventos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fila', models.CharField(max_length=5)),
                ('numero', models.PositiveIntegerField()),
                ('estado', models.CharField(
                    choices=[
                        ('disponible', 'Disponible'),
                        ('apartado', 'Apartado'),
                        ('vendido', 'Vendido'),
                    ],
                    default='disponible',
                    max_length=15
                )),
                ('pos_x', models.FloatField(default=0)),
                ('pos_y', models.FloatField(default=0)),
                ('zona', models.CharField(default='normal', max_length=20)),
                ('precio', models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))),

                # ← ← ←   ESTA ES LA PARTE QUE FALTABA
                ('evento', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='eventos.evento'
                )),
            ],
            options={
                'ordering': ['fila', 'numero'],
            },
        ),
    ]
