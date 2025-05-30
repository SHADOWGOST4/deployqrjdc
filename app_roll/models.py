from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

class Mesa(models.Model):
    nombre = models.CharField(max_length=45)
    tematica_choices = [
        ('FANTASIA', 'Fantasía'),
        ('CIENCIA_FICCION', 'Ciencia Ficción'),
        # Agrega otros según sea necesario
    ]
    tematica = models.CharField(max_length=20, choices=tematica_choices)
    descripcion = models.CharField(max_length=450)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class MesaHasUsuario(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    rol_choices = [
        ('GAMEMASTER', 'Gamemaster'),
        ('JUGADOR', 'Jugador'),
    ]
    rol = models.CharField(max_length=10, choices=rol_choices)
    fecha_rol = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('mesa', 'usuario')

class Personaje(models.Model):
    nombre = models.CharField(max_length=45, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True, default=0)
    altura = models.FloatField(null=True, blank=True, default=0.0)
    apodo = models.CharField(max_length=45, null=True, blank=True)
    nivel = models.IntegerField(default=1)
    hp_base = models.IntegerField(default=100)
    hp_actuales = models.IntegerField(default=100)
    bloqueo = models.IntegerField(default=0)
    esquivar = models.IntegerField(default=0)
    ataque = models.IntegerField(default=0)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('mesa', 'usuario')

class PjConocido(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)
    historia = models.CharField(max_length=250)
    afinidad = models.CharField(max_length=45)

class Atributo(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)
    p_base = models.IntegerField()
    bonificador = models.IntegerField()
    bon_competencia = models.IntegerField()
    bon_equipo = models.IntegerField()
    suma_dado = models.IntegerField()

class Equipamiento(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)
    tipo = models.CharField(max_length=45)
    bonificador = models.IntegerField()

class Habilidad(models.Model):
    personaje = models.ForeignKey(Personaje, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)
    nivel = models.IntegerField()
    descripcion = models.CharField(max_length=250)
