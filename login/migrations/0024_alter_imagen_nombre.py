# Generated by Django 5.1.1 on 2024-12-14 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0023_alter_imagen_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='nombre',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
