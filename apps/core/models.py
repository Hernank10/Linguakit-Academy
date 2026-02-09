from django.db import models

class Programa(models.Model):
    TIPO_CHOICES = [
        ('CPP', 'C++'),
        ('PY', 'Python'),
        ('JS', 'JavaScript'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
