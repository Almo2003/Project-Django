# Generated by Django 5.1.1 on 2024-11-14 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_alter_persona_fechagrado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='fechagrado',
            field=models.DateField(default='00-00-0000'),
        ),
    ]
