# Generated by Django 5.1.1 on 2024-12-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0028_remove_egresado_imagen_egre_egresado_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='egresado',
            name='Imagen',
            field=models.ImageField(upload_to='egresado/'),
        ),
    ]
