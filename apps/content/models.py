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

# Modelos para cursos, lecciones, ejercicios y evaluaciones
class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    nivel = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo

class Leccion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class Ejercicio(models.Model):
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE, related_name='ejercicios')
    titulo = models.CharField(max_length=200)
    pregunta = models.TextField()
    opciones = models.JSONField(default=list)
    respuesta_correcta = models.TextField()
    explicacion = models.TextField(blank=True)
    puntos = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo

class Evaluacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='evaluaciones')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    preguntas = models.JSONField(default=list)
    puntaje_total = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

# === NUEVOS MODELOS PARA PROGRESO Y CERTIFICACIÓN ===

class ProgresoEstudiante(models.Model):
    """Progreso de un estudiante en un curso"""
    estudiante = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='progresos')
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='progresos')
    lecciones_completadas = models.IntegerField(default=0)
    ejercicios_completados = models.IntegerField(default=0)
    ejercicios_correctos = models.IntegerField(default=0)
    puntaje_total = models.IntegerField(default=0)
    porcentaje_completado = models.FloatField(default=0.0)
    ultimo_acceso = models.DateTimeField(auto_now=True)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['estudiante', 'curso']
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.titulo} ({self.porcentaje_completado}%)"

class RespuestaEjercicio(models.Model):
    """Respuesta de un estudiante a un ejercicio"""
    estudiante = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='respuestas')
    ejercicio = models.ForeignKey('Ejercicio', on_delete=models.CASCADE, related_name='respuestas')
    respuesta_dada = models.TextField()
    es_correcta = models.BooleanField(default=False)
    puntaje_obtenido = models.IntegerField(default=0)
    intentos = models.IntegerField(default=1)
    tiempo_segundos = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['estudiante', 'ejercicio']

class Certificado(models.Model):
    """Certificado de finalización de curso"""
    estudiante = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE, related_name='certificados')
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='certificados')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=100, unique=True)
    puntaje_final = models.FloatField()
    url_pdf = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"Certificado de {self.estudiante.username} - {self.curso.titulo}"

# === CAMPOS ADICIONALES PARA EJERCICIOS ===
# Añadir campos a Ejercicio (si no existen)
from django.db import models

# Si los campos no existen, los agregamos dinámicamente
# Pero mejor los definimos en una migración nueva

class TipoEjercicio(models.TextChoices):
    MULTIPLE = 'multiple', 'Opción Múltiple'
    VF = 'vf', 'Verdadero/Falso'
    COMPLETAR = 'completar', 'Completar'
    EMPAREJAR = 'emparejar', 'Emparejar'
    ORDENAR = 'ordenar', 'Ordenar'
    RELACIONAR = 'relacionar', 'Relacionar Columnas'
    ANALISIS = 'analisis', 'Análisis'

# Agregar campos a Ejercicio (usamos una migración separada)
# Por ahora, los añadimos como propiedades del JSON 'content'
# pero para simplificar, los añadimos directamente

# NOTA: Para evitar conflictos, ejecuta después:
# python manage.py makemigrations content --name add_exercise_fields
# python manage.py migrate content
