from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('asientos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCarrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agregado_en', models.DateTimeField(auto_now_add=True)),
                ('asiento', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items_carrito',
                    to='asientos.asiento'
                )),
                ('usuario', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items_carrito',
                    to=settings.AUTH_USER_MODEL
                )),
            ],
            options={
                'verbose_name': 'Item de Carrito',
                'verbose_name_plural': 'Items de Carrito',
                'ordering': ['-agregado_en'],
            },
        ),
    ]
