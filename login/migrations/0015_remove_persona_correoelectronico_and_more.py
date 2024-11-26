# Generated by Django 5.1.1 on 2024-11-17 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0014_alter_persona_fechagrado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='correoelectronico',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='oferta',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='telefono',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='ubicacion_laboral',
        ),
        migrations.AlterField(
            model_name='persona',
            name='documento',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='fechagrado',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='persona',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='persona',
            name='programa',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trazabilidad',
            name='correoelectronico',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='trazabilidad',
            name='oferta',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='trazabilidad',
            name='telefono',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='trazabilidad',
            name='ubicacion_laboral',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]