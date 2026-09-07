from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class LinguisticTechnique(models.Model):
    """Modelo para técnicas lingüísticas"""
    CATEGORY_CHOICES = [
        ('morfosintaxis', 'Morfosintaxis'),
        ('sintaxis', 'Sintaxis'),
        ('semantica', 'Semántica'),
        ('morfologia', 'Morfología'),
        ('ortografia', 'Ortografía'),
        ('fonetica', 'Fonética'),
        ('fonologia', 'Fonología'),
        ('gramatica', 'Gramática'),
        ('retorica', 'Retórica'),
        ('literatura', 'Literatura'),
        ('redaccion', 'Redacción'),
        ('etimologia', 'Etimología'),
        ('puntuacion', 'Puntuación'),
    ]
    
    LEVEL_CHOICES = [
        ('A1', 'A1 - Principiante'),
        ('A2', 'A2 - Básico'),
        ('B1', 'B1 - Intermedio'),
        ('B2', 'B2 - Intermedio Alto'),
        ('C1', 'C1 - Avanzado'),
        ('C2', 'C2 - Experto'),
    ]
    
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True)
    subcategory = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    technique_type = models.CharField(max_length=50, blank=True)
    content = models.JSONField(default=dict)
    theory = models.TextField(blank=True)
    example = models.TextField(blank=True)
    exercise_text = models.TextField(blank=True, verbose_name="Ejercicio")
    correct_answer = models.TextField(blank=True)
    difficulty = models.IntegerField(default=1)
    points = models.IntegerField(default=10)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title[:100]
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'level']),
            models.Index(fields=['technique_type']),
        ]
