# Generated by Django 5.1.1 on 2024-11-04 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='apellido',
        ),
        migrations.AddField(
            model_name='persona',
            name='correoelectronico',
            field=models.EmailField(default='correo@jemplo.com', max_length=254),
        ),
        migrations.AddField(
            model_name='persona',
            name='documento',
            field=models.IntegerField(default=0, max_length=15),
        ),
        migrations.AddField(
            model_name='persona',
            name='fechadegrado',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AddField(
            model_name='persona',
            name='participacion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='persona',
            name='programa',
            field=models.CharField(default='PROGRAMAS', max_length=100),
        ),
        migrations.AddField(
            model_name='persona',
            name='telefono',
            field=models.IntegerField(default=0, max_length=20),
        ),
        migrations.AddField(
            model_name='persona',
            name='ubicacion_laboral',
            field=models.CharField(default='lugar', max_length=200),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
    ]
