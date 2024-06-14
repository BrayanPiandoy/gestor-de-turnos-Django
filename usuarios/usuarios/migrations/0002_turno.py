# Generated by Django 4.0.4 on 2024-06-11 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('numero_cedula', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('tipo_turno', models.CharField(choices=[('documentos', 'Documentos'), ('caja', 'Caja'), ('asesorias', 'Asesorías'), ('servicios', 'Servicios')], max_length=20)),
                ('numero_turno', models.CharField(max_length=10, unique=True)),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]