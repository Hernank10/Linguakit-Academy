from django.db import models
from apps.core.models import Programa

class Leccion(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    orden = models.PositiveIntegerField(default=0)
    contenido_teorico = models.TextField()

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Lecciones"

    def __str__(self):
        return f"{self.programa.nombre} - {self.titulo}"

class Ejercicio(models.Model):
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name='ejercicios')
    pregunta = models.TextField()
    codigo_inicial = models.TextField(blank=True, help_text="Para cursos de programación")
    solucion = models.TextField()

    def __str__(self):
        return f"Ejercicio de: {self.leccion.titulo}"
