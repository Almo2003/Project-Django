# Generated by Django 5.1.1 on 2024-11-11 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_remove_persona_correoelectronico_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='correoelectronico',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='persona',
            name='oferta',
            field=models.CharField(default='oferta academica', max_length=500),
        ),
        migrations.AddField(
            model_name='persona',
            name='telefono',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='persona',
            name='ubicacion_laboral',
            field=models.CharField(default='lugar', max_length=200),
        ),
        migrations.AlterField(
            model_name='persona',
            name='documento',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='persona',
            name='fechagrado',
            field=models.DateField(default='2000-01-01'),
        ),
        migrations.AlterField(
            model_name='persona',
            name='programa',
            field=models.CharField(default='PROGRAMAS', max_length=100),
        ),
        migrations.DeleteModel(
            name='Trasabilidad',
        ),
    ]
