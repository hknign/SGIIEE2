from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('lugar', models.CharField(max_length=250)),
                ('capacidad', models.PositiveIntegerField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='eventos/')),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eventos.categoria')),
            ],
        ),
    ]
