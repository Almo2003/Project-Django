# Generated by Django 5.1.1 on 2024-12-12 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_imagenprincipal'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='egresado',
            name='imagen',
        ),
        migrations.AddField(
            model_name='egresado',
            name='imagen_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
