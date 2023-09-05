from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    token = models.CharField( null = True, max_length=50)  # Redefinir el campo password
  # Redefinir el campo password
    def __str__(self):
        return self.username

class Jugador(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    simbolo = models.CharField(max_length=1, choices=[('X', 'X'), ('O', 'O')])
    puntuacion = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Partida(models.Model):
    jugador_1 = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='partidas_jugador_1')
    jugador_2 = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='partidas_jugador_2')
    turno = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='partidas_turno')
    ganador = models.ForeignKey(Jugador, on_delete=models.SET_NULL, null=True, blank=True, related_name='partidas_ganadas')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    log = models.CharField( null = True, max_length=150) 
    def __str__(self):
        return f"Partida entre {self.jugador_1} y {self.jugador_2}"

class Movimiento(models.Model):
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    fila = models.IntegerField()
    columna = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movimiento de {self.jugador} en ({self.fila}, {self.columna})"
