# Generated by Django 4.0.4 on 2024-06-18 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_turno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='numero_turno',
            field=models.CharField(max_length=10),
        ),
    ]
