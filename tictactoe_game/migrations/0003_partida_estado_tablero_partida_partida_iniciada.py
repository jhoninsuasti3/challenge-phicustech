# Generated by Django 4.2.4 on 2023-08-28 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tictactoe_game', '0002_jugador_partida_movimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='estado_tablero',
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name='partida',
            name='partida_iniciada',
            field=models.BooleanField(default=False),
        ),
    ]
