# Generated by Django 4.2.4 on 2023-08-29 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe_game', '0003_partida_estado_tablero_partida_partida_iniciada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='estado_tablero',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='partida_iniciada',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
